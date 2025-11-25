import pandas as pd

# Load the dataset
df = pd.read_csv('main_data.csv')

# Filter OTC medicines
otc = df[df['Classification'] == 'Over-the-Counter']
prescription = df[df['Classification'] == 'Prescription']

print("OTC Medicines by Category:")
print("-" * 40)
otc_by_category = otc.groupby(['Category', 'Indication']).size().reset_index(name='Count')
for _, row in otc_by_category.iterrows():
    print(f"{row['Category']} - {row['Indication']}: {row['Count']} medicines")

print(f"\nSummary:")
print(f"Total OTC medicines: {len(otc)}")
print(f"Total Prescription medicines: {len(prescription)}")
print(f"OTC categories available: {otc['Category'].nunique()}")

print("\nOTC Categories:")
for category in sorted(otc['Category'].unique()):
    count = len(otc[otc['Category'] == category])
    print(f"- {category}: {count} medicines")