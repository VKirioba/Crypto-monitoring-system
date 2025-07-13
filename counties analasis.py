# Step 1: Import necessary libraries
import pandas as pd
import tabula
import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Define file path and extract tables from the PDF
file_path = r"c:\Users\hp\Downloads\County-Executives-2023-2024.pdf"
# Use tabula to read all tables from the PDF; adjust pages parameter as necessary
dfs = tabula.read_pdf(file_path, pages='all', multiple_tables=True)

# Step 3: Identify and concatenate relevant DataFrames
# Assuming the relevant tables are in a list (e.g., tables for all counties) and share a similar structure:
county_dfs = []
for df in dfs:
    # Optional: Inspect each DataFrame (print(df.head())) and decide if it should be included
    if 'County' in df.columns[0]:  # simple check, adjust as needed
        county_dfs.append(df)

# Concatenate all county DataFrames into one
if county_dfs:
    data = pd.concat(county_dfs, ignore_index=True)
else:
    data = pd.DataFrame()  # or handle error appropriately

# Step 4: Data Cleaning
# Rename columns to something meaningful. Adjust based on the actual table structure.
data.columns = ['County', 'Audit Opinion', 'Financial Figure', 'Under Funding', 'Variance', 'Other Metrics']
# Drop rows with missing County names (if any)
data = data.dropna(subset=['County'])

# Convert financial columns to numeric (remove commas, currency symbols, etc.)
for col in ['Financial Figure', 'Under Funding', 'Variance']:
    data[col] = data[col].replace('[\$,]', '', regex=True).astype(float)

# Step 5: Analysis
# For example, get summary statistics grouped by Audit Opinion
summary_by_opinion = data.groupby('Audit Opinion').agg({
    'Financial Figure': 'sum',
    'Under Funding': 'mean',
    'Variance': 'mean'
}).reset_index()
print("Summary by Audit Opinion:")
print(summary_by_opinion)

# Step 6: Visualization
# Plot total financial figures per audit opinion
plt.figure(figsize=(10,6))
sns.barplot(x='Audit Opinion', y='Financial Figure', data=summary_by_opinion)
plt.title("Total Financial Figures by Audit Opinion")
plt.xlabel("Audit Opinion")
plt.ylabel("Total Financial Figure")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# You can also create additional plots, for example, a histogram of under-funding across counties:
plt.figure(figsize=(10,6))
sns.histplot(data['Under Funding'], bins=20, kde=True)
plt.title("Distribution of Under Funding Across Counties")
plt.xlabel("Under Funding")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
