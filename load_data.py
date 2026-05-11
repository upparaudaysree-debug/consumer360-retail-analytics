import pandas as pd

# Load dataset
df = pd.read_csv("../data/OnlineRetail.csv", encoding='latin1')

# Show first rows
print("FIRST 5 ROWS")
print(df.head())

# Shape before cleaning
print("\nDataset Shape Before Cleaning:")
print(df.shape)

# Remove missing CustomerID
df = df.dropna(subset=['CustomerID'])

# Remove cancelled invoices
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

# Convert InvoiceDate
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create TotalPrice column
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Shape after cleaning
print("\nDataset Shape After Cleaning:")
print(df.shape)

# Check null values
print("\nNull Values:")
print(df.isnull().sum())

# Display cleaned data
print("\nCLEANED DATA")
print(df.head())

# Export cleaned data
df.head(5000).to_csv("../data/sample_retail_data.csv", index=False)

print("Cleaned data exported successfully!")