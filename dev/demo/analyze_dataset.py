import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
print("Loading medicine dataset...")
df = pd.read_csv('main_data.csv')

print("="*50)
print("MEDICINE DATASET ANALYSIS")
print("="*50)

# Basic information about the dataset
print("\n1. DATASET OVERVIEW")
print("-" * 30)
print(f"Dataset shape: {df.shape}")
print(f"Total records: {df.shape[0]:,}")
print(f"Total columns: {df.shape[1]}")

print("\n2. COLUMN INFORMATION")
print("-" * 30)
print(df.info())

print("\n3. FIRST FEW RECORDS")
print("-" * 30)
print(df.head(10))

print("\n4. BASIC STATISTICS")
print("-" * 30)
print(df.describe(include='all'))

print("\n5. MISSING VALUES")
print("-" * 30)
missing_values = df.isnull().sum()
print("Missing values per column:")
for col, count in missing_values.items():
    print(f"{col}: {count} ({count/len(df)*100:.2f}%)")

print("\n6. DATA TYPES")
print("-" * 30)
print(df.dtypes)

print("\n7. UNIQUE VALUES PER COLUMN")
print("-" * 30)
for col in df.columns:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count:,} unique values")

# Categorical analysis - using actual columns from main_data.csv
categorical_columns = ['Category', 'Dosage Form', 'Manufacturer', 'Indication', 'Classification']

print("\n8. CATEGORICAL ANALYSIS")
print("-" * 30)

for col in categorical_columns:
    if col in df.columns:
        print(f"\n{col.upper()} Distribution:")
        value_counts = df[col].value_counts().head(10)
        for value, count in value_counts.items():
            percentage = (count / len(df)) * 100
            print(f"  {value}: {count:,} ({percentage:.2f}%)")

# Medicine category analysis
print("\n9. MEDICINE CATEGORY ANALYSIS")
print("-" * 30)
if 'Category' in df.columns:
    category_counts = df['Category'].value_counts()
    print("Medicine categories distribution:")
    for i, (category, count) in enumerate(category_counts.items(), 1):
        percentage = (count / len(df)) * 100
        print(f"{i:2d}. {category}: {count:,} ({percentage:.2f}%)")

# Indication analysis
print("\n10. MEDICAL INDICATIONS ANALYSIS")
print("-" * 30)
if 'Indication' in df.columns:
    indication_counts = df['Indication'].value_counts()
    print("Top medical indications:")
    for i, (indication, count) in enumerate(indication_counts.items(), 1):
        percentage = (count / len(df)) * 100
        print(f"{i:2d}. {indication}: {count:,} ({percentage:.2f}%)")

# Dosage form analysis
print("\n11. DOSAGE FORM ANALYSIS")
print("-" * 30)
if 'Dosage Form' in df.columns:
    dosage_counts = df['Dosage Form'].value_counts()
    print("Dosage forms distribution:")
    for i, (dosage, count) in enumerate(dosage_counts.items(), 1):
        percentage = (count / len(df)) * 100
        print(f"{i:2d}. {dosage}: {count:,} ({percentage:.2f}%)")

print("\n12. DUPLICATE RECORDS")
print("-" * 30)
duplicates = df.duplicated().sum()
print(f"Number of duplicate records: {duplicates:,}")
if duplicates > 0:
    print("Sample duplicate records:")
    print(df[df.duplicated()].head())

# Strength analysis
print("\n13. STRENGTH ANALYSIS")
print("-" * 30)
if 'Strength' in df.columns:
    # Extract numeric values from strength
    df['Strength_Numeric'] = df['Strength'].str.extract('(\d+)').astype(float)
    print("Strength statistics (mg):")
    print(f"Mean: {df['Strength_Numeric'].mean():.2f} mg")
    print(f"Median: {df['Strength_Numeric'].median():.2f} mg")
    print(f"Min: {df['Strength_Numeric'].min():.0f} mg")
    print(f"Max: {df['Strength_Numeric'].max():.0f} mg")
    print(f"Standard deviation: {df['Strength_Numeric'].std():.2f} mg")

# Top manufacturers analysis
print("\n14. TOP MANUFACTURERS ANALYSIS")
print("-" * 30)
if 'Manufacturer' in df.columns:
    manufacturer_counts = df['Manufacturer'].value_counts().head(10)
    print("Top 10 pharmaceutical manufacturers:")
    for i, (manufacturer, count) in enumerate(manufacturer_counts.items(), 1):
        percentage = (count / len(df)) * 100
        print(f"{i:2d}. {manufacturer}: {count:,} medicines ({percentage:.2f}%)")

# Create visualizations
print("\n15. CREATING VISUALIZATIONS...")
print("-" * 30)

plt.style.use('default')
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Medicine Dataset Analysis', fontsize=16, fontweight='bold')

# Category distribution (pie chart)
if 'Category' in df.columns:
    category_counts = df['Category'].value_counts().head(8)
    axes[0, 0].pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
    axes[0, 0].set_title('Medicine Categories Distribution')

# Classification distribution (bar chart)
if 'Classification' in df.columns:
    classification_counts = df['Classification'].value_counts()
    axes[0, 1].bar(range(len(classification_counts)), classification_counts.values, 
                   color=['skyblue', 'lightcoral'])
    axes[0, 1].set_xticks(range(len(classification_counts)))
    axes[0, 1].set_xticklabels(classification_counts.index, rotation=0)
    axes[0, 1].set_title('Medicine Classification Distribution')
    axes[0, 1].set_ylabel('Count')

# Top indications (horizontal bar chart)
if 'Indication' in df.columns:
    indication_counts = df['Indication'].value_counts().head(8)
    axes[1, 0].barh(range(len(indication_counts)), indication_counts.values, 
                    color='lightgreen')
    axes[1, 0].set_yticks(range(len(indication_counts)))
    axes[1, 0].set_yticklabels(indication_counts.index)
    axes[1, 0].set_title('Top Medical Indications')
    axes[1, 0].set_xlabel('Frequency')

# Dosage forms distribution
if 'Dosage Form' in df.columns:
    dosage_counts = df['Dosage Form'].value_counts()
    colors = plt.cm.Set3(np.linspace(0, 1, len(dosage_counts)))
    axes[1, 1].bar(range(len(dosage_counts)), dosage_counts.values, color=colors)
    axes[1, 1].set_xticks(range(len(dosage_counts)))
    axes[1, 1].set_xticklabels(dosage_counts.index, rotation=45, ha='right')
    axes[1, 1].set_title('Dosage Forms Distribution')
    axes[1, 1].set_ylabel('Count')

plt.tight_layout()
plt.savefig('medicine_dataset_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Cross-tabulation analysis
print("\n16. CROSS-TABULATION ANALYSIS")
print("-" * 30)
if 'Category' in df.columns and 'Classification' in df.columns:
    print("Medicine Category vs Classification:")
    crosstab = pd.crosstab(df['Category'], df['Classification'], margins=True)
    print(crosstab)

# Medicine name patterns analysis
print("\n17. MEDICINE NAME PATTERNS")
print("-" * 30)
if 'Name' in df.columns:
    # Common prefixes
    prefixes = [name[:4] for name in df['Name'] if len(name) >= 4]
    prefix_counter = Counter(prefixes)
    print("Most common medicine name prefixes:")
    for i, (prefix, count) in enumerate(prefix_counter.most_common(10), 1):
        percentage = (count / len(df)) * 100
        print(f"{i:2d}. '{prefix}': {count:,} medicines ({percentage:.2f}%)")

# Strength distribution by category
print("\n18. STRENGTH BY CATEGORY ANALYSIS")
print("-" * 30)
if 'Strength_Numeric' in df.columns and 'Category' in df.columns:
    strength_by_category = df.groupby('Category')['Strength_Numeric'].agg(['mean', 'median', 'count'])
    print("Average strength by medicine category:")
    for category in strength_by_category.index:
        mean_strength = strength_by_category.loc[category, 'mean']
        median_strength = strength_by_category.loc[category, 'median']
        count = strength_by_category.loc[category, 'count']
        print(f"  {category}: Mean={mean_strength:.1f}mg, Median={median_strength:.1f}mg (n={count})")

print("\n19. SUMMARY INSIGHTS")
print("-" * 30)
print("Key findings from the medicine dataset:")
print(f"• Dataset contains {df.shape[0]:,} medicine records with {df.shape[1]} attributes")
print(f"• {df['Name'].nunique() if 'Name' in df.columns else 'N/A':,} unique medicine names")
print(f"• {df['Category'].nunique() if 'Category' in df.columns else 'N/A'} different medicine categories")
print(f"• {df['Dosage Form'].nunique() if 'Dosage Form' in df.columns else 'N/A'} different dosage forms")
print(f"• {df['Manufacturer'].nunique() if 'Manufacturer' in df.columns else 'N/A'} different pharmaceutical manufacturers")
print(f"• {df['Indication'].nunique() if 'Indication' in df.columns else 'N/A'} different medical indications")

# Classification distribution
if 'Classification' in df.columns:
    otc_count = (df['Classification'] == 'Over-the-Counter').sum()
    prescription_count = (df['Classification'] == 'Prescription').sum()
    print(f"• {otc_count:,} Over-the-Counter medicines ({otc_count/len(df)*100:.1f}%)")
    print(f"• {prescription_count:,} Prescription medicines ({prescription_count/len(df)*100:.1f}%)")

if duplicates > 0:
    print(f"• Warning: {duplicates:,} duplicate records found")
else:
    print("• No duplicate records found")

missing_percentage = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
print(f"• Overall missing data: {missing_percentage:.2f}%")

# Most common category and indication
if 'Category' in df.columns:
    most_common_category = df['Category'].mode().iloc[0]
    category_percentage = (df['Category'] == most_common_category).sum() / len(df) * 100
    print(f"• Most common category: {most_common_category} ({category_percentage:.1f}%)")

if 'Indication' in df.columns:
    most_common_indication = df['Indication'].mode().iloc[0]
    indication_percentage = (df['Indication'] == most_common_indication).sum() / len(df) * 100
    print(f"• Most common indication: {most_common_indication} ({indication_percentage:.1f}%)")

print(f"\nAnalysis complete! Visualization saved as 'medicine_dataset_analysis.png'")