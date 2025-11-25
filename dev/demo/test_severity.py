#!/usr/bin/env python3
"""
Test script to demonstrate the symptom severity classification system
"""

import requests
import json

# Test different symptom combinations
test_cases = [
    {
        "name": "Mild Case",
        "symptoms": "sneezing, mild headache, tiredness",
        "expected_severity": "mild"
    },
    {
        "name": "Moderate/Possible Risk Case", 
        "symptoms": "fever, persistent cough, body aches, fatigue",
        "expected_severity": "possible_risk"
    },
    {
        "name": "Severe Case",
        "symptoms": "difficulty breathing, severe headache, high fever, chest pain",
        "expected_severity": "severe"
    }
]

def test_severity_classification():
    base_url = "http://127.0.0.1:5000"
    
    print("="*60)
    print("SYMPTOM SEVERITY CLASSIFICATION TEST")
    print("="*60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 40)
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
                
                print(f"Detected Severity: {severity_info.get('case_severity', 'unknown').upper()}")
                print(f"Severity Score: {severity_info.get('severity_score', 0):.1f}/10")
                print(f"Urgency Level: {severity_info.get('urgency', 'unknown')}")
                print(f"Recommendation: {severity_info.get('recommendation', 'No recommendation')}")
                print(f"Triage Level: {result.get('triage', 'unknown')}")
                
                # Show symptom breakdown
                symptom_breakdown = severity_info.get('symptom_breakdown', [])
                if symptom_breakdown:
                    print("\nSymptom Breakdown:")
                    for symptom, severity, score in symptom_breakdown:
                        print(f"  • {symptom.title()}: {severity} (score: {score})")
                
                # Check if expected severity matches
                detected_severity = severity_info.get('case_severity', '')
                expected_severity = test_case['expected_severity']
                match_status = "✓ MATCH" if detected_severity == expected_severity else "✗ MISMATCH"
                print(f"\nExpected: {expected_severity.upper()}")
                print(f"Result: {match_status}")
                
                # Show treatment options
                options = result.get('options', [])
                if options:
                    print(f"\nTreatment Options ({len(options)}):")
                    for j, option in enumerate(options, 1):
                        print(f"  {j}. {option.get('title', 'Unknown')}")
                        if option.get('priority') == 'urgent':
                            print("     ⚠️  URGENT PRIORITY")
                
            else:
                print(f"Error: HTTP {response.status_code}")
                print(response.text)
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the Flask application")
            print("Please make sure the app is running on http://127.0.0.1:5000")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("\n" + "="*60)
    print("TEST COMPLETED")
    print("="*60)

if __name__ == "__main__":
    test_severity_classification()