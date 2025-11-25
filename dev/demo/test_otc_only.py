#!/usr/bin/env python3
"""
Test script to verify that only Over-the-Counter medicines are recommended
"""

import requests
import json
import pandas as pd

def test_otc_only_recommendations():
    base_url = "http://127.0.0.1:5000"
    
    # Load the medicine dataset and create the same MEDS list as the app
    df = pd.read_csv('main_data.csv')
    
    # Create MEDS list with only OTC medicines (same as in app.py)
    MEDS = []
    for _, row in df.iterrows():
        # Only include Over-the-Counter medicines
        if row['Classification'].lower() == 'over-the-counter':
            med_data = {
                "id": row['Name'].lower().replace(' ', '_'),
                "name": row['Name'],
                "category": row['Category'],
                "classification": row['Classification'],
            }
            MEDS.append(med_data)
    
    print("="*70)
    print("OVER-THE-COUNTER MEDICINES ONLY TEST")
    print("="*70)
    
    # Test various symptom combinations
    test_cases = [
        {"name": "Pain Symptoms", "symptoms": "headache, body aches, joint pain"},
        {"name": "Fever Symptoms", "symptoms": "fever, high fever, chills"},
        {"name": "Viral Symptoms", "symptoms": "sore throat, fever, body aches, viral infection"},
        {"name": "Fungal Symptoms", "symptoms": "skin rash, fungal infection, itching"},
        {"name": "Infection Symptoms", "symptoms": "minor infection, wound, cuts"}
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 50)
        print(f"Symptoms: {test_case['symptoms']}")
        
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
                
                print(f"Medicine Policy: {result.get('medicine_policy', 'Not specified')}")
                
                # Check all recommended medicines
                options = result.get('options', [])
                total_medicines = 0
                otc_medicines = 0
                prescription_medicines = 0
                
                print("\nRecommended Treatments:")
                for j, option in enumerate(options, 1):
                    print(f"  {j}. {option.get('title', 'Unknown')}")
                    
                    # Check if there's a medicine note
                    if option.get('medicine_note'):
                        print(f"     Note: {option.get('medicine_note')}")
                    
                    drugs = option.get('drugs', [])
                    if drugs:
                        print(f"     Medicines: {len(drugs)}")
                        for drug_id in drugs:
                            total_medicines += 1
                            # Find the medicine in the OTC MEDS list (same as app uses)
                            med = next((m for m in MEDS if m['id'] == drug_id), None)
                            if med:
                                med_name = med['name']
                                classification = med['classification']
                                category = med['category']
                                
                                if classification == 'Over-the-Counter':
                                    otc_medicines += 1
                                    status = "✓ OTC"
                                else:
                                    prescription_medicines += 1
                                    status = "✗ PRESCRIPTION"
                                
                                print(f"       - {med_name} ({category}) - {status}")
                            else:
                                print(f"       - {drug_id} - Medicine not found in OTC MEDS list")
                
                print(f"\nMedicine Summary:")
                print(f"  Total recommended medicines: {total_medicines}")
                print(f"  Over-the-Counter: {otc_medicines}")
                print(f"  Prescription: {prescription_medicines}")
                
                if prescription_medicines == 0:
                    print("  ✅ PASS: Only OTC medicines recommended")
                else:
                    print("  ❌ FAIL: Prescription medicines found")
                
                # Check system note
                note = result.get('note', '')
                if 'Over-the-Counter' in note or 'OTC' in note:
                    print("  ✅ PASS: System note mentions OTC policy")
                else:
                    print("  ❌ FAIL: System note doesn't mention OTC policy")
                
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
    print("OTC-ONLY TEST COMPLETED")
    print("="*70)
    
    # Summary statistics
    print("\nDataset Summary:")
    otc_total = len(MEDS)  # MEDS now only contains OTC medicines
    prescription_total = len(df[df['Classification'] == 'Prescription'])
    print(f"Available OTC medicines in MEDS: {otc_total:,}")
    print(f"Available Prescription medicines in original dataset: {prescription_total:,}")
    print(f"OTC categories: {len(set(m['category'] for m in MEDS))}")

if __name__ == "__main__":
    test_otc_only_recommendations()