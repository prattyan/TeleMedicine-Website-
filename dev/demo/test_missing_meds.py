#!/usr/bin/env python3
"""
Test script to identify cases where no medications are provided
"""

import requests
import json

def test_missing_medications():
    base_url = "http://127.0.0.1:5000"
    
    print("="*70)
    print("TESTING FOR MISSING MEDICATION RECOMMENDATIONS")
    print("="*70)
    
    # Test various symptom combinations that might not get medicine recommendations
    test_cases = [
        {
            "name": "Digestive Issues",
            "symptoms": "nausea, vomiting, stomach pain, indigestion, bloating"
        },
        {
            "name": "Respiratory Issues",
            "symptoms": "wheezing, shortness of breath, chest tightness, asthma"
        },
        {
            "name": "Skin Problems",
            "symptoms": "rash, itching, skin irritation, dry skin, eczema"
        },
        {
            "name": "Mental Health Symptoms",
            "symptoms": "depression, anxiety, mood swings, irritability, stress"
        },
        {
            "name": "Diabetic Symptoms",
            "symptoms": "high blood sugar, excessive thirst, frequent urination, diabetes"
        },
        {
            "name": "Fungal Symptoms",
            "symptoms": "fungal infection, athlete's foot, yeast infection, skin fungus"
        },
        {
            "name": "Wound Care",
            "symptoms": "cut, wound, scrape, minor injury, bleeding"
        },
        {
            "name": "Eye/Ear Problems",
            "symptoms": "ear pain, eye irritation, dry eyes, ear infection"
        },
        {
            "name": "Single Symptom Cases",
            "symptoms": "headache"
        },
        {
            "name": "Very Mild Symptoms",
            "symptoms": "slight tiredness, minor discomfort"
        }
    ]
    
    no_medication_cases = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 50)
        print(f"Symptoms: {test_case['symptoms']}")
        
        # Prepare test data
        test_data = {
            "patientName": f"Test Patient {i}",
            "age": 35,
            "sex": "Male",
            "weight": 70,
            "height": 1.75,
            "symptoms": test_case['symptoms'],
            "allergies": [],
            "current_meds": [],
            "pregnant": False
        }
        
        try:
            # Make request to the assessment endpoint
            response = requests.post(f"{base_url}/assess", json=test_data)
            
            if response.status_code == 200:
                result = response.json()
                severity_info = result.get("severity_classification", {})
                
                print(f"Severity: {severity_info.get('case_severity', 'unknown').upper()}")
                print(f"Severity Score: {severity_info.get('severity_score', 0):.1f}/10")
                
                # Check treatment options
                options = result.get('options', [])
                medicine_options = [opt for opt in options if opt.get('drugs')]
                
                if not medicine_options:
                    print("❌ NO MEDICATIONS RECOMMENDED")
                    no_medication_cases.append(test_case['name'])
                    
                    print("Available options:")
                    if options:
                        for j, option in enumerate(options, 1):
                            print(f"  {j}. {option.get('title', 'Unknown')} (no medicines)")
                    else:
                        print("  No treatment options available")
                else:
                    print(f"✅ {len(medicine_options)} medication option(s) provided")
                    for j, option in enumerate(medicine_options, 1):
                        drugs = option.get('drugs', [])
                        print(f"  {j}. {option.get('title')} - {len(drugs)} medicine(s): {', '.join(drugs)}")
                
            else:
                print(f"Error: HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the Flask application")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("\n" + "="*70)
    print("SUMMARY OF MISSING MEDICATION CASES")
    print("="*70)
    
    if no_medication_cases:
        print(f"❌ Cases with no medication recommendations: {len(no_medication_cases)}")
        for case in no_medication_cases:
            print(f"  - {case}")
        print(f"\nSuccess rate: {((len(test_cases) - len(no_medication_cases))/len(test_cases))*100:.1f}%")
    else:
        print("✅ All test cases received medication recommendations!")
        print("Success rate: 100%")

if __name__ == "__main__":
    test_missing_medications()