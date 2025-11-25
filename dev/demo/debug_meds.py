import pandas as pd

# Load the dataset
df = pd.read_csv('main_data.csv')

# Convert CSV data to structured format for compatibility (same as in app.py)
MEDS = []
for _, row in df.iterrows():
    med_data = {
        "id": row['Name'].lower().replace(' ', '_'),
        "name": row['Name'],
        "category": row['Category'],
        "dosage_form": row['Dosage Form'],
        "strength": row['Strength'],
        "manufacturer": row['Manufacturer'],
        "indication": row['Indication'],
        "classification": row['Classification'],
    }
    MEDS.append(med_data)

print("Checking MEDS structure...")
print(f"Total MEDS entries: {len(MEDS)}")

# Check Acetomycin entries
acetomycin_meds = [m for m in MEDS if m['name'] == 'Acetomycin']
print(f"\nAcetomycin entries: {len(acetomycin_meds)}")
for i, m in enumerate(acetomycin_meds[:5]):
    print(f"  {i+1}. {m['name']}: {m['classification']} ({m['category']}) - {m['indication']}")

# Test the helper function logic
def find_medicines_by_category_and_indication(category, indication=None):
    matches = []
    print(f"\nSearching for: Category='{category}', Indication='{indication}'")
    for med in MEDS:
        # Only include Over-the-Counter medicines
        if (med['category'].lower() == category.lower() and 
            med['classification'].lower() == 'over-the-counter'):
            if indication is None or med['indication'].lower() == indication.lower():
                matches.append(med)
                print(f"  Found: {med['name']} - {med['classification']}")
                if len(matches) >= 2:  # Limit to 2 medicines per category
                    break
    return matches

# Test analgesic pain medicines
print("\n" + "="*50)
print("Testing Analgesic + Pain search:")
analgesic_pain_meds = find_medicines_by_category_and_indication("analgesic", "pain")
print(f"Found {len(analgesic_pain_meds)} medicines")

# Test analgesic medicines (any indication)
print("\n" + "="*50)
print("Testing Analgesic (any indication) search:")
analgesic_any_meds = find_medicines_by_category_and_indication("analgesic")
print(f"Found {len(analgesic_any_meds)} medicines")