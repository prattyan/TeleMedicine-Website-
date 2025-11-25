import pandas as pd

# Load the dataset
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

print(f"Total OTC medicines in MEDS: {len(MEDS)}")

# Check if Acetomycin is in MEDS
acetomycin_meds = [m for m in MEDS if 'acetomycin' in m['id']]
print(f"Acetomycin OTC entries in MEDS: {len(acetomycin_meds)}")
print("First 3 Acetomycin entries:")
for m in acetomycin_meds[:3]:
    print(f"  {m['name']}: {m['classification']} ({m['category']})")

# Check if the test medicine lookup would work
def lookup_medicine_in_original_csv(drug_id):
    """This simulates what the test script does"""
    med_row = df[df['Name'].str.lower().str.replace(' ', '_') == drug_id]
    if not med_row.empty:
        return med_row.iloc[0]['Name'], med_row.iloc[0]['Classification']
    return None, None

# Test lookup for acetomycin
name, classification = lookup_medicine_in_original_csv('acetomycin')
print(f"\nTest lookup for 'acetomycin' in original CSV:")
print(f"  Found: {name} - {classification}")
print("  ^ This is the issue! Test finds first match in original CSV, not filtered MEDS")

# Show what the MEDS lookup would return
acetomycin_in_meds = next((m for m in MEDS if m['id'] == 'acetomycin'), None)
if acetomycin_in_meds:
    print(f"\nMEDS lookup for 'acetomycin':")
    print(f"  Found: {acetomycin_in_meds['name']} - {acetomycin_in_meds['classification']}")
else:
    print("\nNo acetomycin found in MEDS (this would be correct if no OTC acetomycin exists)")