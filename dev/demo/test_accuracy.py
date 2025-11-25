#!/usr/bin/env python3
"""
Test script to verify improved accuracy - fewer medicines for normal symptoms
"""

import requests
import json

def test_improved_accuracy():
    base_url = "http://127.0.0.1:5000"
    
    print("="*70)
    print("IMPROVED ACCURACY TEST")
    print("Testing that 5-6 normal symptoms don't result in 6-7 medicines")
    print("="*70)
    
    # Test various normal symptom combinations (5-6 symptoms each)
    test_cases = [
        {
            "name": "Common Cold Symptoms (6 symptoms)",
            "symptoms": "headache, mild fever, sore throat, runny nose, fatigue, cough",
            "expected_max_treatments": 3,
            "expected_max_medicines": 3
        },
        {
            "name": "Mild Flu Symptoms (5 symptoms)", 
            "symptoms": "body aches, headache, tiredness, mild fever, congestion",
            "expected_max_treatments": 3,
            "expected_max_medicines": 3
        },
        {
            "name": "General Pain Symptoms (6 symptoms)",
            "symptoms": "headache, back pain, muscle aches, joint pain, neck pain, fatigue",
            "expected_max_treatments": 2,
            "expected_max_medicines": 2
        },
        {
            "name": "Allergy-like Symptoms (5 symptoms)",
            "symptoms": "sneezing, runny nose, watery eyes, nasal congestion, itchy throat",
            "expected_max_treatments": 2,
            "expected_max_medicines": 2
        },
        {
            "name": "Mixed Mild Symptoms (6 symptoms)",
            "symptoms": "mild headache, slight fever, tiredness, minor aches, dry throat, light cough",
            "expected_max_treatments": 3,
            "expected_max_medicines": 3
        }
    ]
    
    total_tests = len(test_cases)
    passed_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 60)
        print(f"Symptoms ({len(test_case['symptoms'].split(','))}): {test_case['symptoms']}")
        
        # Prepare test data
        test_data = {
            "patientName": f"Test Patient {i}",
            "age": 30,
            "sex": "Female",
            "weight": 65,
            "height": 1.65,
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
                
                # Analyze treatment options
                options = result.get('options', [])
                total_treatments = len(options)
                total_medicines = 0
                
                print(f"\nTreatment Options ({total_treatments}):")
                for j, option in enumerate(options, 1):
                    drugs = option.get('drugs', [])
                    medicine_count = len(drugs)
                    total_medicines += medicine_count
                    
                    print(f"  {j}. {option.get('title', 'Unknown')}")
                    print(f"     Medicines: {medicine_count}")
                    if drugs:
                        print(f"     Drugs: {', '.join(drugs)}")
                    print(f"     Rationale: {option.get('rationale', 'No rationale')}")
                
                # Check accuracy
                treatments_pass = total_treatments <= test_case['expected_max_treatments']
                medicines_pass = total_medicines <= test_case['expected_max_medicines']
                
                print(f"\nAccuracy Analysis:")
                print(f"  Total Treatments: {total_treatments} (max expected: {test_case['expected_max_treatments']}) {'✅' if treatments_pass else '❌'}")
                print(f"  Total Medicines: {total_medicines} (max expected: {test_case['expected_max_medicines']}) {'✅' if medicines_pass else '❌'}")
                
                if treatments_pass and medicines_pass:
                    print(f"  Result: ✅ PASS - Improved accuracy achieved")
                    passed_tests += 1
                else:
                    print(f"  Result: ❌ FAIL - Too many recommendations")
                
                # Show medicine efficiency ratio
                if total_treatments > 0:
                    medicine_ratio = total_medicines / total_treatments
                    print(f"  Medicine Efficiency: {medicine_ratio:.1f} medicines per treatment")
                    
            else:
                print(f"Error: HTTP {response.status_code}")
                print(response.text)
                
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to the Flask application")
            print("Please make sure the app is running on http://127.0.0.1:5000")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("\n" + "="*70)
    print("ACCURACY TEST SUMMARY")
    print("="*70)
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED - Accuracy significantly improved!")
        print("✅ System now provides focused, relevant recommendations")
    elif passed_tests > total_tests * 0.7:
        print("✅ Most tests passed - Good improvement in accuracy")
    else:
        print("⚠️  Some tests failed - Further accuracy improvements needed")
    
    print(f"\nKey Improvements:")
    print(f"- Limited to maximum 3 treatment options")
    print(f"- Only 1 medicine per category (reduced from 2)")
    print(f"- Higher thresholds for symptom matching")
    print(f"- Prioritized treatment recommendations")
    print(f"- More selective pain and fever matching")

if __name__ == "__main__":
    test_improved_accuracy()