import pandas as pd

# Load dataset
df = pd.read_csv("../data/OnlineRetail.csv", encoding='latin1')

# Data cleaning
df = df.dropna(subset=['CustomerID'])
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

# Convert date column
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create TotalPrice
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Reference date
today_date = df['InvoiceDate'].max()

# RFM Calculation
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (today_date - x.max()).days,
    'InvoiceNo': 'count',
    'TotalPrice': 'sum'
})

# Rename columns
rfm.columns = ['Recency', 'Frequency', 'Monetary']

# RFM Scores
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1,2,3,4])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4])

# Customer Segmentation
def segment_customer(row):
    if row['R_Score'] == 4 and row['F_Score'] == 4:
        return 'Champion'
    elif row['F_Score'] >= 3:
        return 'Loyal Customer'
    elif row['R_Score'] <= 2:
        return 'At Risk'
    else:
        return 'Regular Customer'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

# Display results
print(rfm.head(20))
# Export RFM Analysis
rfm.to_csv("../reports/rfm_customer_segments.csv")

print("RFM Customer Segments Exported Successfully!")