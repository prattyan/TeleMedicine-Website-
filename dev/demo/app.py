
# app.py -- Demo Clinical Decision Support (CDS) prototype (NON-PRESCRIBING)
# NOTE: This is a toy demo for development and testing only.
# It MUST NOT be used clinically without validation, certification, and clinician workflows.
from flask import Flask, request, jsonify, send_file
import json, datetime, os, io, pandas as pd
from flask import send_from_directory
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageTemplate, Frame

app = Flask(__name__)

# Load medicine dataset from CSV
BASE_DIR = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(BASE_DIR, "main_data.csv"))

# Convert CSV data to structured format for compatibility - ONLY OTC MEDICINES
MEDS = []
for _, row in df.iterrows():
    # Only include Over-the-Counter medicines
    if row['Classification'].lower() == 'over-the-counter':
        med_data = {
            "id": row['Name'].lower().replace(' ', '_'),
            "name": row['Name'],
            "category": row['Category'],
            "dosage_form": row['Dosage Form'],
            "strength": row['Strength'],
            "manufacturer": row['Manufacturer'],
            "indication": row['Indication'],
            "classification": row['Classification'],
            "contraindications": [],
            "age_groups": {
                "adult": {
                    "dose": f"{row['Strength']} {row['Dosage Form'].lower()}",
                    "min_age": 18,
                    "max_age": 64
                },
                "elderly": {
                    "dose": f"Reduced dose: {row['Strength']} {row['Dosage Form'].lower()}",
                    "min_age": 65,
                    "max_age": 999,
                    "notes": "Consider dose adjustment for elderly patients"
                }
            }
        }
        MEDS.append(med_data)

# Serve index.html at root
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

def classify_symptom_severity(symptoms_text):
    """Classify symptoms into mild, possible risk, or severe cases"""
    symptoms_list = [s.strip().lower() for s in symptoms_text.split(',')]
    
    # Define severity classifications
    severe_symptoms = {
        "difficulty breathing": 3, "shortness of breath": 3, "chest pain": 3,
        "severe headache": 3, "persistent vomiting": 3, "high fever": 3,
        "blood in urine": 3, "blood in stool": 3, "severe abdominal pain": 3,
        "loss of consciousness": 3, "severe allergic reaction": 3,
        "difficulty swallowing": 3, "severe dehydration": 3,
        "rapid heart rate": 2, "dizziness": 2, "confusion": 2,
        "severe fatigue": 2, "persistent fever": 2, "severe pain": 2
    }
    
    moderate_symptoms = {
        "fever": 2, "persistent cough": 2, "moderate pain": 2,
        "nausea": 1, "vomiting": 2, "headache": 1,
        "body aches": 1, "fatigue": 1, "sore throat": 1,
        "congestion": 1, "runny nose": 1, "mild fever": 1,
        "stomach pain": 1, "joint pain": 1, "muscle pain": 1
    }
    
    mild_symptoms = {
        "sneezing": 0.5, "itchy eyes": 0.5, "mild headache": 0.5,
        "slight fever": 0.5, "minor aches": 0.5, "tiredness": 0.5,
        "dry throat": 0.5, "light cough": 0.5, "minor congestion": 0.5
    }
    
    severity_score = 0
    matched_symptoms = []
    
    for symptom in symptoms_list:
        for severe_symptom, score in severe_symptoms.items():
            if severe_symptom in symptom:
                severity_score += score
                matched_symptoms.append((symptom, "severe", score))
                break
        else:
            for moderate_symptom, score in moderate_symptoms.items():
                if moderate_symptom in symptom:
                    severity_score += score
                    matched_symptoms.append((symptom, "moderate", score))
                    break
            else:
                for mild_symptom, score in mild_symptoms.items():
                    if mild_symptom in symptom:
                        severity_score += score
                        matched_symptoms.append((symptom, "mild", score))
                        break
                else:
                    # Default classification for unmatched symptoms
                    matched_symptoms.append((symptom, "mild", 0.5))
                    severity_score += 0.5
    
    # Classify overall case severity
    if severity_score >= 8:
        case_severity = "severe"
        urgency = "immediate_medical_attention"
        recommendation = "Seek immediate medical attention or emergency care"
    elif severity_score >= 4:
        case_severity = "possible_risk"
        urgency = "medical_consultation_recommended"
        recommendation = "Consult with healthcare provider within 24-48 hours"
    else:
        case_severity = "mild"
        urgency = "self_care_monitoring"
        recommendation = "Monitor symptoms and consider over-the-counter treatments"
    
    return {
        "severity_score": severity_score,
        "case_severity": case_severity,
        "urgency": urgency,
        "recommendation": recommendation,
        "symptom_breakdown": matched_symptoms,
        "total_symptoms": len(symptoms_list)
    }

def simple_symptom_to_options(symptoms_text):
    symptoms_list = [s.strip().lower() for s in symptoms_text.split(',')]
    opts = []
    
    # Get severity classification
    severity_analysis = classify_symptom_severity(symptoms_text)
    
    # Track which categories and their scores
    category_scores = {}
    
    # Define symptom clusters with weights (balanced thresholds for better coverage)
    symptom_clusters = {
        "viral_infection": {
            "symptoms": {
                "sore throat": 1, "fever": 1, "body ache": 1, "viral": 1,
                "fatigue": 0.8, "headache": 0.8, "congestion": 0.7, "cough": 0.7
            },
            "threshold": 2.0  # Balanced threshold
        },
        "bacterial_infection": {
            "symptoms": {
                "pus": 1.5, "tonsil": 0.8, "tonsillar": 1, "exudate": 1.5,
                "persistent fever": 1.5, "severe": 0.7, "high fever": 1.2,
                "white patches": 1, "swollen lymph nodes": 1, "infection": 1
            },
            "threshold": 2.0  # Balanced threshold
        },
        "allergy": {
            "symptoms": {
                "sneezing": 1, "runny nose": 1, "itchy eyes": 1.2, "allergy": 1.5,
                "nasal congestion": 0.8, "itchy throat": 0.7, "watery eyes": 1
            },
            "threshold": 1.8  # Lower threshold for allergy symptoms
        },
        "respiratory": {
            "symptoms": {
                "wheezing": 1.5, "shortness of breath": 1.5, "asthma": 2,
                "difficulty breathing": 1.5, "chest tightness": 1, "coughing": 0.8
            },
            "threshold": 1.5  # Lower threshold for respiratory issues
        },
        "gi_symptoms": {
            "symptoms": {
                "nausea": 1.5, "vomiting": 2, "emesis": 2, "indigestion": 1,
                "stomach pain": 1.2, "decreased appetite": 0.8, "bloating": 1,
                "digestive": 1, "abdominal": 1
            },
            "threshold": 1.5  # Lower threshold for GI symptoms
        },
        "skin_conditions": {
            "symptoms": {
                "rash": 1.5, "itching": 1.2, "skin irritation": 1.5, "dry skin": 1,
                "eczema": 1.5, "dermatitis": 1.5, "skin": 0.8
            },
            "threshold": 1.2  # New category for skin issues
        },
        "mental_health": {
            "symptoms": {
                "depression": 2, "anxiety": 1.5, "mood swings": 1, "irritability": 1,
                "stress": 1, "mental": 0.8
            },
            "threshold": 1.5  # New category for mental health
        },
        "wound_care": {
            "symptoms": {
                "cut": 1.5, "wound": 2, "scrape": 1, "minor injury": 1.5,
                "bleeding": 1, "injury": 1
            },
            "threshold": 1.0  # Lower threshold for wound care
        },
        "diabetes": {
            "symptoms": {
                "high blood sugar": 1.5, "diabetes": 2, "hyperglycemia": 1.5,
                "excessive thirst": 1, "frequent urination": 1, "blurred vision": 0.8
            },
            "threshold": 2.0  # Keep existing threshold
        },
        "hypertension": {
            "symptoms": {
                "high blood pressure": 2, "hypertension": 2,
                "headache": 0.5, "dizziness": 0.5
            },
            "threshold": 2.0  # Keep existing threshold
        },
        "high_cholesterol": {
            "symptoms": {
                "high cholesterol": 2, "hyperlipidemia": 2
            },
            "threshold": 2.0  # Keep existing threshold
        }
    }
    
    # Helper function to find medicines by category and indication (all are OTC)
    def find_medicines_by_category_and_indication(category, indication=None):
        matches = []
        for med in MEDS:
            if med['category'].lower() == category.lower():
                if indication is None or med['indication'].lower() == indication.lower():
                    matches.append(med['id'])
        return matches[:1]  # Limit to 1 medicine per category for better accuracy
    
    # Calculate scores for each category based on symptoms
    for symptom in symptoms_list:
        for category, cluster in symptom_clusters.items():
            score = 0
            for keyword, weight in cluster["symptoms"].items():
                if keyword in symptom:
                    score += weight
            if score > 0:
                category_scores[category] = category_scores.get(category, 0) + score
    
    # Add treatment options based on category scores
    if category_scores.get("viral_infection", 0) >= symptom_clusters["viral_infection"]["threshold"]:
        antiviral_meds = find_medicines_by_category_and_indication("antiviral", "virus")
        if not antiviral_meds:
            antiviral_meds = find_medicines_by_category_and_indication("antiviral")
        if antiviral_meds:
            opts.append({
                "id": "antiviral_1",
                "type": "antiviral",
                "title": "Antiviral medication for viral infection",
                "drugs": antiviral_meds,
                "rationale": "Viral illness pattern identified: antiviral treatment recommended."
            })
    
    if category_scores.get("bacterial_infection", 0) >= symptom_clusters["bacterial_infection"]["threshold"]:
        antibiotic_meds = find_medicines_by_category_and_indication("antibiotic", "infection")
        if not antibiotic_meds:
            antibiotic_meds = find_medicines_by_category_and_indication("antibiotic")
        if antibiotic_meds:
            opts.append({
                "id": "antibiotic_1",
                "type": "antibiotic",
                "title": "Antibiotic for bacterial infection",
                "drugs": antibiotic_meds,
                "rationale": "Multiple bacterial infection indicators present; clinical confirmation required."
            })
    
    if category_scores.get("allergy", 0) >= symptom_clusters["allergy"]["threshold"]:
        # Look for antihistamine or related categories for allergies
        allergy_meds = find_medicines_by_category_and_indication("antihistamine")
        if not allergy_meds:
            # If no direct antihistamine, look for other suitable categories
            allergy_meds = find_medicines_by_category_and_indication("antiseptic")
        if allergy_meds:
            opts.append({
                "id": "allergy_1",
                "type": "antihistamine",
                "title": "Medication for allergy symptoms",
                "drugs": allergy_meds,
                "rationale": "Allergy symptom pattern identified."
            })
    
    if category_scores.get("diabetes", 0) >= symptom_clusters["diabetes"]["threshold"]:
        diabetic_meds = find_medicines_by_category_and_indication("antidiabetic", "diabetes")
        if not diabetic_meds:
            diabetic_meds = find_medicines_by_category_and_indication("antidiabetic")
        if diabetic_meds:
            opts.append({
                "id": "antidiabetic_1",
                "type": "antidiabetic",
                "title": "Antidiabetic medication",
                "drugs": diabetic_meds,
                "rationale": "Diabetes symptoms identified; clinical confirmation required."
            })
    
    # Add GI symptom treatment
    if category_scores.get("gi_symptoms", 0) >= symptom_clusters["gi_symptoms"]["threshold"]:
        gi_meds = find_medicines_by_category_and_indication("antiseptic", "infection")  # Use antiseptic for digestive support
        if not gi_meds:
            gi_meds = find_medicines_by_category_and_indication("antiseptic")
        if gi_meds:
            opts.append({
                "id": "gi_1",
                "type": "digestive_support",
                "title": "Digestive support medication",
                "drugs": gi_meds,
                "rationale": "Gastrointestinal symptoms identified."
            })
    
    # Add skin condition treatment
    if category_scores.get("skin_conditions", 0) >= symptom_clusters["skin_conditions"]["threshold"]:
        skin_meds = find_medicines_by_category_and_indication("antifungal", "fungus")
        if not skin_meds:
            skin_meds = find_medicines_by_category_and_indication("antiseptic")
        if skin_meds:
            opts.append({
                "id": "skin_1",
                "type": "topical_treatment",
                "title": "Topical treatment for skin conditions",
                "drugs": skin_meds,
                "rationale": "Skin condition symptoms identified."
            })
    
    # Add mental health support
    if category_scores.get("mental_health", 0) >= symptom_clusters["mental_health"]["threshold"]:
        mental_meds = find_medicines_by_category_and_indication("antidepressant", "depression")
        if not mental_meds:
            mental_meds = find_medicines_by_category_and_indication("antidepressant")
        if mental_meds:
            opts.append({
                "id": "mental_1",
                "type": "mental_health_support",
                "title": "Mental health support medication",
                "drugs": mental_meds,
                "rationale": "Mental health symptoms identified; consider professional counseling."
            })
    
    # Add wound care treatment
    if category_scores.get("wound_care", 0) >= symptom_clusters["wound_care"]["threshold"]:
        wound_meds = find_medicines_by_category_and_indication("antiseptic", "wound")
        if not wound_meds:
            wound_meds = find_medicines_by_category_and_indication("antiseptic")
        if wound_meds:
            opts.append({
                "id": "wound_1",
                "type": "wound_care",
                "title": "Wound care antiseptic",
                "drugs": wound_meds,
                "rationale": "Wound care symptoms identified."
            })
    
    # Add respiratory treatment
    if category_scores.get("respiratory", 0) >= symptom_clusters["respiratory"]["threshold"]:
        resp_meds = find_medicines_by_category_and_indication("antipyretic")  # Use available categories for respiratory support
        if resp_meds:
            opts.append({
                "id": "respiratory_1",
                "type": "respiratory_support",
                "title": "Respiratory symptom relief",
                "drugs": resp_meds,
                "rationale": "Respiratory symptoms identified; seek medical attention if breathing difficulties persist."
            })
    
    # Add pain management option (more selective)
    pain_symptoms = ["pain", "ache", "headache"]
    pain_score = sum(1 for pain_symptom in pain_symptoms if pain_symptom in symptoms_text.lower())
    
    # Only recommend pain medication if multiple pain symptoms or strong pain indicators
    if pain_score >= 2 or any(severe_pain in symptoms_text.lower() for severe_pain in ["severe pain", "intense pain", "chronic pain"]):
        analgesic_meds = find_medicines_by_category_and_indication("analgesic", "pain")
        if not analgesic_meds:
            analgesic_meds = find_medicines_by_category_and_indication("analgesic")
        if analgesic_meds:
            opts.append({
                "id": "analgesic_1",
                "type": "analgesic",
                "title": "Pain relief medication",
                "drugs": analgesic_meds,
                "rationale": f"Multiple pain symptoms identified (score: {pain_score})."
            })
    
    # Add fever management option (more selective)
    fever_indicators = ["fever", "high fever", "temperature"]
    fever_score = sum(1 for indicator in fever_indicators if indicator in symptoms_text.lower())
    
    # Only recommend fever medication for clear fever symptoms
    if fever_score >= 1 or "fever" in symptoms_text.lower():
        antipyretic_meds = find_medicines_by_category_and_indication("antipyretic", "fever")
        if not antipyretic_meds:
            antipyretic_meds = find_medicines_by_category_and_indication("antipyretic")
        if antipyretic_meds:
            opts.append({
                "id": "antipyretic_1",
                "type": "antipyretic",
                "title": "Fever reduction medication",
                "drugs": antipyretic_meds,
                "rationale": "Fever symptoms clearly identified."
            })
    
    # Fallback mechanism - if no medicines found, provide basic symptom relief
    if not opts or not any(opt.get("drugs") for opt in opts):
        # Check for any general symptoms that could benefit from basic relief
        general_symptoms = symptoms_text.lower()
        
        # Basic pain relief for any discomfort
        if any(keyword in general_symptoms for keyword in ["pain", "ache", "discomfort", "sore", "hurt"]):
            fallback_analgesic = find_medicines_by_category_and_indication("analgesic")
            if fallback_analgesic:
                opts.append({
                    "id": "fallback_pain",
                    "type": "general_pain_relief",
                    "title": "General pain relief",
                    "drugs": fallback_analgesic,
                    "rationale": "General discomfort symptoms identified."
                })
        
        # Basic antiseptic for infections, wounds, or skin issues
        elif any(keyword in general_symptoms for keyword in ["infection", "wound", "cut", "rash", "skin", "irritation"]):
            fallback_antiseptic = find_medicines_by_category_and_indication("antiseptic")
            if fallback_antiseptic:
                opts.append({
                    "id": "fallback_antiseptic",
                    "type": "general_antiseptic",
                    "title": "General antiseptic treatment",
                    "drugs": fallback_antiseptic,
                    "rationale": "General infection or wound care symptoms identified."
                })
        
        # Basic antifungal for fungal symptoms
        elif any(keyword in general_symptoms for keyword in ["fungus", "fungal", "yeast", "athlete", "foot"]):
            fallback_antifungal = find_medicines_by_category_and_indication("antifungal")
            if fallback_antifungal:
                opts.append({
                    "id": "fallback_antifungal",
                    "type": "antifungal_treatment",
                    "title": "Antifungal treatment",
                    "drugs": fallback_antifungal,
                    "rationale": "Fungal infection symptoms identified."
                })
        
        # Basic digestive support
        elif any(keyword in general_symptoms for keyword in ["nausea", "stomach", "digestive", "bloating", "indigestion"]):
            fallback_digestive = find_medicines_by_category_and_indication("antiseptic")  # Use antiseptic for digestive support
            if fallback_digestive:
                opts.append({
                    "id": "fallback_digestive",
                    "type": "digestive_support",
                    "title": "Digestive support",
                    "drugs": fallback_digestive,
                    "rationale": "Digestive symptoms identified."
                })
        
        # If still no options, provide general supportive care advice
        elif not opts:
            opts.append({
                "id": "general_advice",
                "type": "general_care",
                "title": "General supportive care",
                "drugs": [],
                "rationale": "Symptoms noted. Consider rest, hydration, and over-the-counter symptom relief as appropriate. Consult healthcare provider if symptoms persist or worsen."
            })
    
    # Add severity-based treatment modifications
    if severity_analysis["case_severity"] == "severe":
        # For severe cases, prioritize immediate care options
        opts.insert(0, {
            "id": "emergency_care",
            "type": "emergency_referral",
            "title": "URGENT: Immediate Medical Attention Required",
            "drugs": [],
            "rationale": "Severe symptoms detected requiring immediate medical evaluation. Only OTC supportive care available through this system.",
            "priority": "urgent",
            "note": "Prescription medications may be required - consult emergency services or healthcare provider immediately"
        })
    elif severity_analysis["case_severity"] == "possible_risk":
        # For moderate risk, add monitoring advice
        for opt in opts:
            opt["monitoring_required"] = True
            opt["rationale"] += " Monitor symptoms closely and seek medical attention if worsening. Only OTC medicines recommended."
    
    # Add OTC-only note to all medicine options
    for opt in opts:
        if opt.get("drugs"):
            opt["medicine_note"] = "Only Over-the-Counter medicines are recommended by this system"
    
    # Improve accuracy by limiting total recommendations and prioritizing by severity
    if len(opts) > 3:
        # Sort by priority: emergency first, then by number of drugs (fewer is better), then by type
        def option_priority(opt):
            if opt.get("priority") == "urgent":
                return 0
            elif opt.get("type") in ["analgesic", "antipyretic"]:  # Core symptom relief
                return 1
            elif opt.get("type") in ["antibiotic", "antiviral"]:  # Infection treatment
                return 2
            else:
                return 3
        
        opts.sort(key=option_priority)
        opts = opts[:3]  # Limit to maximum 3 treatment options for better accuracy
    
    # Add severity analysis to all options
    for opt in opts:
        opt["severity_analysis"] = severity_analysis
    
    return opts

def get_age_group(age):
    if age < 2:
        return "infant"
    elif age < 12:
        return "child"
    elif age < 18:
        return "adolescent"
    elif age < 65:
        return "adult"
    else:
        return "elderly"

def run_safety_checks(option, patient):
    flags = []
    age = patient.get("age")
    
    for drug_id in option.get("drugs", []):
        drug = next((d for d in MEDS if d["id"] == drug_id), None)
        if not drug:
            flags.append(f"Unknown drug id: {drug_id}")
            continue

        # Age-based checks
        if age is not None:
            age_group = get_age_group(age)
            age_info = drug.get("age_groups", {}).get(age_group)
            
            if not age_info:
                flags.append(f"{drug['name']} is not typically recommended for this age group")
            else:
                min_age = age_info.get("min_age", 0)
                max_age = age_info.get("max_age", 999)
                if age < min_age or age > max_age:
                    flags.append(f"{drug['name']}: Age {age} is outside recommended range")
                option["dosing"] = age_info.get("dose", "Standard dosing")
                if age_info.get("notes"):
                    flags.append(f"{drug['name']} note: {age_info['notes']}")
    
    return flags

@app.route("/symptoms", methods=["GET"])
def get_symptoms():
    # Organized symptom list by category for the frontend
    available_symptoms = {
        "General": [
            {"id": "fever", "text": "Fever", "keywords": ["fever", "high temperature"]},
            {"id": "fatigue", "text": "Fatigue", "keywords": ["fatigue", "tiredness"]},
            {"id": "body_ache", "text": "Body Aches", "keywords": ["body ache", "muscle pain"]},
            {"id": "headache", "text": "Headache", "keywords": ["headache"]}
        ],
        "Respiratory": [
            {"id": "sore_throat", "text": "Sore Throat", "keywords": ["sore throat"]},
            {"id": "cough", "text": "Cough", "keywords": ["cough", "coughing"]},
            {"id": "wheezing", "text": "Wheezing", "keywords": ["wheezing"]},
            {"id": "shortness_breath", "text": "Shortness of Breath", "keywords": ["shortness of breath", "difficulty breathing"]},
            {"id": "chest_tightness", "text": "Chest Tightness", "keywords": ["chest tightness"]}
        ],
        "ENT & Allergy": [
            {"id": "nasal_congestion", "text": "Nasal Congestion", "keywords": ["nasal congestion", "congestion"]},
            {"id": "runny_nose", "text": "Runny Nose", "keywords": ["runny nose"]},
            {"id": "sneezing", "text": "Sneezing", "keywords": ["sneezing"]},
            {"id": "itchy_eyes", "text": "Itchy Eyes", "keywords": ["itchy eyes", "watery eyes"]},
            {"id": "tonsillar_symptoms", "text": "Swollen/White Tonsils", "keywords": ["tonsil", "tonsillar", "white patches", "pus", "exudate"]}
        ],
        "Gastrointestinal": [
            {"id": "nausea", "text": "Nausea", "keywords": ["nausea"]},
            {"id": "vomiting", "text": "Vomiting", "keywords": ["vomiting", "emesis"]},
            {"id": "stomach_pain", "text": "Stomach Pain", "keywords": ["stomach pain"]},
            {"id": "decreased_appetite", "text": "Decreased Appetite", "keywords": ["decreased appetite"]}
        ],
        "Chronic Conditions": [
            {"id": "diabetes_symptoms", "text": "Diabetes Symptoms", "keywords": ["high blood sugar", "diabetes", "hyperglycemia", "excessive thirst", "frequent urination"]},
            {"id": "hypertension_symptoms", "text": "High Blood Pressure Symptoms", "keywords": ["high blood pressure", "hypertension"]},
            {"id": "high_cholesterol", "text": "High Cholesterol", "keywords": ["high cholesterol", "hyperlipidemia"]}
        ]
    }
    return jsonify(available_symptoms)

def generate_prescription_pdf(patient_data, options):
    buffer = None
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get the default style sheet and define custom styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            leading=14
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=12
        )
        
        elements = []
        
        # Add content to the PDF
        elements.append(Paragraph("Medical Prescription", title_style))
        elements.append(Spacer(1, 12))
        
        # Add current date
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        elements.append(Paragraph(f"Date: {current_date}", normal_style))
        elements.append(Spacer(1, 12))
        
        # Calculate BMI if weight is available
        weight = patient_data.get('weight', '')
        height = patient_data.get('height', '')  # Height should be in meters
        bmi = None
        bmi_status = "Not available"
        if weight and height and isinstance(weight, (int, float)) and isinstance(height, (int, float)):
            bmi = weight / (height * height)  # height should be in meters
            # Determine BMI status
            if bmi < 18.5:
                bmi_status = "Underweight"
            elif bmi < 25:
                bmi_status = "Normal weight"
            elif bmi < 30:
                bmi_status = "Overweight"
            else:
                bmi_status = "Obese"
            
        # Patient information table data
        # Convert height from meters to centimeters for display
        height_cm = patient_data.get('height', '') * 100 if patient_data.get('height', '') else ''
        
        patient_info = [
            ["Patient Name:", str(patient_data.get("patientName", ""))],
            ["Age:", f"{patient_data.get('age', '')} years"],
            ["Gender:", str(patient_data.get('sex', ''))],
            ["Weight:", f"{patient_data.get('weight', '')} kg"],
            ["Height:", f"{height_cm:.0f} cm" if height_cm else ""],
            ["BMI:", f"{bmi:.1f} ({bmi_status})" if bmi else "Not available"]
        ]
        
        # Create patient info table
        t = Table(patient_info, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))
        
        # Add symptoms section with severity analysis
        elements.append(Paragraph("Clinical Assessment", heading_style))
        # Get symptoms from multiple possible sources
        symptoms_text = patient_data.get('symptomTexts') or patient_data.get('symptoms') or patient_data.get('symptom_texts') or ''
        
        # Debug: Print what we're getting for symptoms
        print(f"Debug - symptoms_text: '{symptoms_text}'")
        print(f"Debug - patient_data keys: {patient_data.keys()}")
        
        # Add symptoms section with severity analysis
        elements.append(Paragraph("Clinical Assessment", heading_style))
        # Get symptoms from multiple possible sources
        symptoms_text = patient_data.get('symptomTexts') or patient_data.get('symptoms') or patient_data.get('symptom_texts') or ''
        
        # Debug: Print what we're getting for symptoms
        print(f"Debug - symptoms_text: '{symptoms_text}'")
        print(f"Debug - patient_data keys: {patient_data.keys()}")
        
        if symptoms_text and symptoms_text.strip():
            # Get severity analysis
            severity_analysis = classify_symptom_severity(symptoms_text)
            
            # Add severity classification
            elements.append(Paragraph("<b>Case Severity Classification:</b>", normal_style))
            severity_color = "red" if severity_analysis["case_severity"] == "severe" else \
                           "orange" if severity_analysis["case_severity"] == "possible_risk" else "green"
            
            elements.append(Paragraph(f'<font color="{severity_color}"><b>{severity_analysis["case_severity"].upper().replace("_", " ")}</b></font>', normal_style))
            elements.append(Paragraph(f"Severity Score: {severity_analysis['severity_score']:.1f}/10", normal_style))
            elements.append(Paragraph(f"<b>Recommendation:</b> {severity_analysis['recommendation']}", normal_style))
            elements.append(Spacer(1, 12))
            
            symptoms_list = [s.strip() for s in symptoms_text.split(',') if s.strip()]
            if symptoms_list:
                elements.append(Paragraph("<b>Presenting Symptoms:</b>", normal_style))
                elements.append(Spacer(1, 6))
                
                # Group symptoms by severity for better presentation
                severe_symptoms = []
                moderate_symptoms = []
                mild_symptoms = []
                
                for symptom_data in severity_analysis["symptom_breakdown"]:
                    symptom, severity, score = symptom_data
                    if severity == "severe":
                        severe_symptoms.append((symptom, score))
                    elif severity == "moderate":
                        moderate_symptoms.append((symptom, score))
                    else:
                        mild_symptoms.append((symptom, score))
                
                if severe_symptoms:
                    elements.append(Paragraph('<font color="red"><b>Severe Symptoms:</b></font>', normal_style))
                    for symptom, score in severe_symptoms:
                        elements.append(Paragraph(f'<font color="red">• {symptom.title()} (Score: {score})</font>', normal_style))
                    elements.append(Spacer(1, 6))
                
                if moderate_symptoms:
                    elements.append(Paragraph('<font color="orange"><b>Moderate Symptoms:</b></font>', normal_style))
                    for symptom, score in moderate_symptoms:
                        elements.append(Paragraph(f'<font color="orange">• {symptom.title()} (Score: {score})</font>', normal_style))
                    elements.append(Spacer(1, 6))
                
                if mild_symptoms:
                    elements.append(Paragraph('<b>Mild Symptoms:</b>', normal_style))
                    for symptom, score in mild_symptoms:
                        elements.append(Paragraph(f"• {symptom.title()} (Score: {score})", normal_style))
                
                elements.append(Spacer(1, 20))
        else:
            # If no symptoms are provided, show a note
            elements.append(Paragraph("<b>Presenting Symptoms:</b>", normal_style))
            elements.append(Paragraph("No specific symptoms provided in the assessment.", normal_style))
            elements.append(Spacer(1, 20))
        
        # Add medications with timing
        if options:
            elements.append(Paragraph("Recommended Over-the-Counter Medications:", heading_style))
            elements.append(Paragraph("<b>Note:</b> This system only recommends Over-the-Counter (OTC) medicines. For prescription medications, consult your healthcare provider.", normal_style))
            elements.append(Spacer(1, 12))
            
            all_meds = []
            for opt in options:
                if 'drugs' in opt:
                    for drug_id in opt['drugs']:
                        # Find the medicine in our dataset (all are OTC)
                        med = next((m for m in MEDS if m['id'] == drug_id), None)
                        if med:
                            drug_name = med['name']
                            category = med['category']
                            dosage_form = med['dosage_form']
                            strength = med['strength']
                            
                            # Get default timing based on category and dosage form
                            timing = "Take as directed"
                            if category.lower() == "analgesic":
                                timing = "Take every 6-8 hours as needed for pain"
                            elif category.lower() == "antipyretic":
                                timing = "Take every 6-8 hours as needed for fever"
                            elif category.lower() == "antibiotic":
                                timing = "Take every 8 hours for 7-10 days"
                            elif category.lower() == "antiviral":
                                timing = "Take as directed for 5-7 days"
                            elif category.lower() == "antidiabetic":
                                timing = "Take once or twice daily with meals"
                            elif category.lower() == "antifungal":
                                timing = "Take once daily"
                            elif category.lower() == "antidepressant":
                                timing = "Take once daily"
                            elif category.lower() == "antiseptic":
                                if dosage_form.lower() in ["ointment", "cream"]:
                                    timing = "Apply to affected area 2-3 times daily"
                                else:
                                    timing = "Use as directed"
                            elif dosage_form.lower() == "inhaler":
                                timing = "Use 2 puffs every 4-6 hours as needed"
                            elif dosage_form.lower() in ["ointment", "cream"]:
                                timing = "Apply to affected area 2-3 times daily"
                            elif dosage_form.lower() == "drops":
                                timing = "Use as directed"
                            elif dosage_form.lower() == "injection":
                                timing = "Administer as prescribed by healthcare provider"
                            
                            dosing = opt.get('dosing', f'{strength} {dosage_form}')
                            all_meds.append((drug_name, timing, dosing, med['manufacturer']))
            
            if not all_meds:
                elements.append(Paragraph("No Over-the-Counter medicines available for the current symptoms. Please consult a healthcare provider for prescription medications if needed.", normal_style))
            else:
                # Sort medications alphabetically
                all_meds.sort(key=lambda x: x[0])
                
                # Add each medication with its timing and dosing
                for idx, (drug_name, timing, dosing, manufacturer) in enumerate(all_meds, 1):
                    elements.append(Paragraph(f"{idx}. <b>{drug_name}</b> (OTC)", normal_style))
                    elements.append(Paragraph(f"   Dosing: {dosing}", normal_style))
                    elements.append(Paragraph(f"   Instructions: {timing}", normal_style))
                    elements.append(Paragraph(f"   Manufacturer: {manufacturer}", normal_style))
                    elements.append(Spacer(1, 8))
        
        # Add signature section with proper spacing
        elements.append(Spacer(1, 30))
        
        # Add line for signature
        elements.append(Paragraph("_" * 45, normal_style))
        
        # Add signature image centered above the line
        signature_img_path = os.path.join(BASE_DIR, "sign.png")
        if os.path.exists(signature_img_path):
            signature = Image(signature_img_path)
            # Set signature height to 0.75 inches (54 points) and adjust width proportionally
            desired_height = 54  # 0.75 inches in points
            aspect_ratio = signature.imageWidth / signature.imageHeight
            signature.drawHeight = desired_height
            signature.drawWidth = desired_height * aspect_ratio
            # Center the signature above the line
            signature.hAlign = 'CENTER'
            elements.append(signature)
            
        # Add small space and then the text
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("Doctor's Signature", normal_style))
        
        # Add footer
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("This is a computer-generated recommendation for Over-the-Counter medicines only. For prescription medications or severe conditions, consult a licensed healthcare provider.", 
                               ParagraphStyle('Footer', parent=styles['Italic'], fontSize=8)))
        
        # Create a custom PageTemplate to add border
        def add_border(canvas, doc):
            canvas.saveState()
            # Draw a rectangle border with rounded corners
            canvas.setStrokeColorRGB(0.2, 0.2, 0.2)  # Dark gray color
            canvas.setLineWidth(2)
            # Leave 0.5 inch margin from edges
            margin = 36  # 0.5 inch in points
            width, height = letter
            canvas.roundRect(margin, margin, width - 2*margin, height - 2*margin, radius=10)
            canvas.restoreState()
            
        # Create a frame for the content
        frame = Frame(
            doc.leftMargin,
            doc.bottomMargin,
            doc.width,
            doc.height,
            id='normal'
        )
        
        # Create PageTemplate with frame and onPage callback
        template = PageTemplate(
            'normal',
            [frame],
            onPage=add_border
        )
        doc.addPageTemplates([template])
        
        # Build PDF with border
        doc.build(elements)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        if buffer:
            buffer.close()
        raise

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"ok","timestamp": datetime.datetime.utcnow().isoformat() + "Z"})

@app.route("/assess", methods=["POST", "GET"])
def assess():
    if request.method == "GET" and request.args.get('format') == 'pdf':
        # Handle PDF generation from GET request
        try:
            data = json.loads(request.args.get('data', '{}'))
            age = data.get("age")
            if age is not None:
                age = float(age)
            
            patient = {
                "patientName": data.get("patientName", ""),  # Get name from the patientName field
                "age": age,
                "sex": data.get("sex"),
                "weight": data.get("weight"),
                "height": data.get("height"),  # Add height for BMI calculation
                "symptoms": data.get("symptomTexts", data.get("symptoms", ""))  # Get full symptom texts or fallback to keywords
            }
            
            options = simple_symptom_to_options(data.get("symptoms", ""))
            
            # Get severity analysis from the first option or create new one
            severity_info = options[0]["severity_analysis"] if options else classify_symptom_severity(data.get("symptoms", ""))
            
            for opt in options:
                opt["safety_flags"] = run_safety_checks(opt, patient)
                if age is not None:
                    age_group = get_age_group(age)
                    opt["age_group"] = age_group
            
            pdf_buffer = generate_prescription_pdf(patient, options)
            # Create filename with patient name
            patient_name = patient.get("patientName", "").strip().replace(" ", "_")
            filename = f'prescription_{patient_name}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf' if patient_name else f'prescription_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
            return send_file(
                pdf_buffer,
                download_name=filename,
                mimetype='application/pdf'
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Handle regular POST request
    data = request.json or {}
    symptoms = data.get("symptoms","")
    age = data.get("age")
    if age is not None:
        age = float(age)
    
    patient = {
        "patientName": data.get("patientName", ""),
        "age": age,
        "sex": data.get("sex"),
        "weight": data.get("weight"),
        "height": data.get("height"),  # Add height for BMI calculation
        "symptoms": symptoms,  # Add symptoms for PDF generation
        "symptomTexts": data.get("symptomTexts", symptoms)  # Add symptomTexts field
    }
    
    options = simple_symptom_to_options(symptoms)
    
    # Get severity analysis from the first option (they all have the same analysis)
    severity_info = options[0]["severity_analysis"] if options else classify_symptom_severity(symptoms)
    
    # Add age-specific information to each option
    for opt in options:
        opt["safety_flags"] = run_safety_checks(opt, patient)
        if age is not None:
            age_group = get_age_group(age)
            opt["age_group"] = age_group
            # Add age-specific evidence and guidelines
            if age < 18:
                opt["evidence"] = [
                    {"title": f"Pediatric dosing guidelines for {age_group}s", "date": "2025-09-10", 
                     "snippet": f"Special considerations required for {age_group} age group."}
                ]
            elif age >= 65:
                opt["evidence"] = [
                    {"title": "Geriatric prescribing guidelines", "date": "2025-09-10", 
                     "snippet": "Consider reduced dosing and increased monitoring in elderly patients."}
                ]
            else:
                opt["evidence"] = [
                    {"title": "Adult treatment guidelines", "date": "2025-09-10", 
                     "snippet": "Standard adult dosing and monitoring recommended."}
                ]
    # Determine triage level based on severity
    triage_level = "primary_care"
    if severity_info["case_severity"] == "severe":
        triage_level = "emergency"
    elif severity_info["case_severity"] == "possible_risk":
        triage_level = "urgent_care"
    
    response = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "severity_classification": {
            "case_severity": severity_info["case_severity"],
            "severity_score": severity_info["severity_score"],
            "urgency": severity_info["urgency"],
            "recommendation": severity_info["recommendation"],
            "symptom_breakdown": severity_info["symptom_breakdown"],
            "total_symptoms": severity_info["total_symptoms"]
        },
        "triage": triage_level,
        "differential": ["viral pharyngitis", "streptococcal pharyngitis (consider if Centor criteria met)"],
        "options": options,
        "note": "This system recommends only Over-the-Counter (OTC) medicines. For prescription medications or severe conditions, consult a licensed healthcare provider. This is clinical decision support only.",
        "medicine_policy": "Only Over-the-Counter medicines are recommended by this system",
        "requires_clinician_signoff": True
    }

    # Check if PDF is requested
    if request.args.get('format') == 'pdf':
        pdf_buffer = generate_prescription_pdf(patient, options)
        # Create filename with patient name
        patient_name = patient.get("patientName", "").strip().replace(" ", "_")
        filename = f'Prescription_{patient_name}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf' if patient_name else f'prescription_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        return send_file(
            pdf_buffer,
            download_name=filename,
            mimetype='application/pdf'
        )
    
    return jsonify(response)

if __name__ == "__main__":
    # Development server (do not use in production)
    app.run(host="0.0.0.0", port=5000, debug=True)
