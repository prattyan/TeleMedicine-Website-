# Symptom Severity Classification System

## Overview
The Clinical Decision Support system now includes an intelligent symptom severity classification that automatically categorizes patient symptoms into three main categories:

## Severity Categories

### 1. **MILD CASE** (Score: 0-3.9)
- **Urgency**: Self-care monitoring
- **Recommendation**: Monitor symptoms and consider over-the-counter treatments
- **Triage Level**: Primary care
- **Examples**: 
  - Sneezing, mild headache, tiredness
  - Minor aches, dry throat, light cough
  - Slight fever, minor congestion

### 2. **POSSIBLE RISK CASE** (Score: 4.0-7.9)
- **Urgency**: Medical consultation recommended
- **Recommendation**: Consult with healthcare provider within 24-48 hours
- **Triage Level**: Urgent care
- **Examples**:
  - Fever, persistent cough, body aches, fatigue
  - Moderate pain, nausea, headache
  - Joint pain, muscle pain, stomach pain

### 3. **SEVERE CASE** (Score: 8.0+)
- **Urgency**: Immediate medical attention required
- **Recommendation**: Seek immediate medical attention or emergency care
- **Triage Level**: Emergency
- **Examples**:
  - Difficulty breathing, chest pain
  - Severe headache, high fever
  - Blood in urine/stool, severe abdominal pain
  - Loss of consciousness, severe allergic reaction

## Scoring System

### Severe Symptoms (Score: 2-3 points each)
- Difficulty breathing/shortness of breath: 3 points
- Chest pain: 3 points
- Severe headache: 3 points
- Persistent vomiting: 3 points
- High fever: 3 points
- Blood in urine/stool: 3 points
- Severe abdominal pain: 3 points
- Loss of consciousness: 3 points
- Severe allergic reaction: 3 points
- Difficulty swallowing: 3 points
- Severe dehydration: 3 points
- Rapid heart rate: 2 points
- Dizziness: 2 points
- Confusion: 2 points
- Severe fatigue: 2 points
- Persistent fever: 2 points
- Severe pain: 2 points

### Moderate Symptoms (Score: 1-2 points each)
- Fever: 2 points
- Persistent cough: 2 points
- Vomiting: 2 points
- Moderate pain: 2 points
- Nausea: 1 point
- Headache: 1 point
- Body aches: 1 point
- Fatigue: 1 point
- Sore throat: 1 point
- Congestion: 1 point
- Runny nose: 1 point
- Mild fever: 1 point
- Stomach pain: 1 point
- Joint pain: 1 point
- Muscle pain: 1 point

### Mild Symptoms (Score: 0.5 points each)
- Sneezing: 0.5 points
- Itchy eyes: 0.5 points
- Mild headache: 0.5 points
- Slight fever: 0.5 points
- Minor aches: 0.5 points
- Tiredness: 0.5 points
- Dry throat: 0.5 points
- Light cough: 0.5 points
- Minor congestion: 0.5 points

## Features

### 1. **Automatic Classification**
- Analyzes all entered symptoms
- Calculates weighted severity score
- Assigns appropriate severity level
- Provides urgency recommendations

### 2. **Treatment Modifications**
- **Severe cases**: Adds emergency referral option at the top of treatment list
- **Possible risk cases**: Adds monitoring requirements to all treatments
- **Mild cases**: Standard treatment options

### 3. **Enhanced Reporting**
- Detailed symptom breakdown with individual scores
- Color-coded severity indicators in PDFs
- Comprehensive severity analysis in JSON responses
- Triage level recommendations

### 4. **PDF Enhancements**
- Symptoms grouped by severity level
- Color-coded presentation (red for severe, orange for moderate, black for mild)
- Individual symptom scores
- Overall severity assessment
- Clear recommendations

## API Response Structure

```json
{
  "severity_classification": {
    "case_severity": "possible_risk",
    "severity_score": 6.0,
    "urgency": "medical_consultation_recommended",
    "recommendation": "Consult with healthcare provider within 24-48 hours",
    "symptom_breakdown": [
      ["fever", "moderate", 2],
      ["persistent cough", "moderate", 2],
      ["body aches", "moderate", 1],
      ["fatigue", "moderate", 1]
    ],
    "total_symptoms": 4
  },
  "triage": "urgent_care",
  "options": [...],
  ...
}
```

## Benefits

1. **Improved Patient Safety**: Early identification of severe symptoms requiring immediate attention
2. **Appropriate Resource Allocation**: Directs patients to the right level of care
3. **Clinical Decision Support**: Helps healthcare providers prioritize cases
4. **Patient Education**: Clear severity explanations help patients understand their condition
5. **Comprehensive Documentation**: Detailed severity analysis for medical records

## Testing

The system has been thoroughly tested with various symptom combinations to ensure accurate classification:

- ✅ Mild symptoms correctly classified as "mild"
- ✅ Moderate symptoms correctly classified as "possible_risk"  
- ✅ Severe symptoms correctly classified as "severe"
- ✅ Emergency referral automatically added for severe cases
- ✅ Monitoring requirements added for possible risk cases
- ✅ Appropriate triage levels assigned