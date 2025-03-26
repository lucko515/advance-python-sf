# 04: Advanced Pandas Operations
print("Advanced Pandas: Transforming and Analyzing Data")
print("------------------------------------------------")

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime

# Load the loan applications dataset
loan_file = "loan_applications.csv"
loan_path = os.path.join("data_analysis", loan_file)
loans_df = pd.read_csv(loan_path)

# Quick data overview
print("\nDataset dimensions:", loans_df.shape)
print("First 3 rows:")
print(loans_df.head(3))

# 1. GroupBy Operations
print("\n1. GroupBy Operations")
print("-------------------")
print("GroupBy splits data into groups and applies functions to each group")

# Simple groupby with one column
print("\nAverage loan amount by education level:")
education_loan_avg = loans_df.groupby('education')['loan_amount'].mean().sort_values(ascending=False)
print(education_loan_avg)

# Multiple aggregation functions
print("\nMultiple statistics by education level:")
education_stats = loans_df.groupby('education').agg({
    'loan_amount': ['mean', 'median', 'min', 'max', 'count'],
    'interest_rate': ['mean', 'median'],
    'default': 'mean'  # Default rate
})
print(education_stats)

# Groupby with multiple columns
print("\nDefault rate by education and gender:")
default_by_ed_gender = loans_df.groupby(['education', 'gender'])['default'].mean().sort_values(ascending=False)
print(default_by_ed_gender)

# Groupby with custom aggregation function
print("\nLoan amount disparity (max/min ratio) by occupation:")
loan_disparity = loans_df.groupby('occupation').agg(
    min_loan=('loan_amount', 'min'),
    max_loan=('loan_amount', 'max')
).eval('disparity = max_loan / min_loan').sort_values('disparity', ascending=False)
print(loan_disparity.head())

# 2. Pivot Tables
print("\n2. Pivot Tables")
print("-------------")
print("Pivot tables reshape data to provide a different view")

# Basic pivot table
print("\nAverage loan amount by education and gender:")
pivot_loan = loans_df.pivot_table(
    values='loan_amount',
    index='education',
    columns='gender',
    aggfunc='mean'
)
print(pivot_loan)

# Multiple values and aggregations
print("\nMultiple metrics by education and gender:")
pivot_multi = loans_df.pivot_table(
    values=['loan_amount', 'interest_rate', 'credit_score'],
    index='education',
    columns='gender',
    aggfunc={'loan_amount': 'mean', 'interest_rate': 'mean', 'credit_score': 'median'}
)
print(pivot_multi)

# Adding totals to pivot tables
print("\nPivot table with totals:")
pivot_with_totals = loans_df.pivot_table(
    values='loan_amount',
    index='education',
    columns='gender',
    aggfunc='mean',
    margins=True,
    margins_name='Total'
)
print(pivot_with_totals)

# 3. Merging and Joining DataFrames
print("\n3. Merging and Joining DataFrames")
print("-------------------------------")
print("Combining data from multiple sources is a common task")

# Create some sample DataFrames to demonstrate merging
# Applicant details
applicants = loans_df[['application_id', 'age', 'gender', 'education', 'occupation']].head(10)
print("\nApplicant details (first 5 rows):")
print(applicants.head(5))

# Loan details
loans = loans_df[['application_id', 'loan_amount', 'loan_term', 'interest_rate', 'monthly_payment']].head(15)
print("\nLoan details (first 5 rows):")
print(loans.head(5))

# Inner join (only matching records)
print("\nInner join (only rows with matches in both DataFrames):")
inner_join = pd.merge(applicants, loans, on='application_id', how='inner')
print(inner_join.head())
print(f"Result shape: {inner_join.shape}")

# Left join (all records from left DataFrame)
print("\nLeft join (all rows from left DataFrame):")
left_join = pd.merge(applicants, loans, on='application_id', how='left')
print(left_join.head())
print(f"Result shape: {left_join.shape}")

# Outer join (all records from both DataFrames)
print("\nOuter join (all rows from both DataFrames):")
outer_join = pd.merge(applicants, loans, on='application_id', how='outer')
print(outer_join.head())
print(f"Result shape: {outer_join.shape}")

# Concatenating DataFrames
print("\nConcatenating DataFrames (stacking rows):")
stacked = pd.concat([applicants.head(3), applicants.tail(3)])
print(stacked)

# 4. Working with Dates and Times
print("\n4. Working with Dates and Times")
print("-----------------------------")

# Convert application_date to datetime
loans_df['application_date'] = pd.to_datetime(loans_df['application_date'])
print("\nFirst few dates after conversion:")
print(loans_df['application_date'].head())

# Extract components from dates
loans_df['year'] = loans_df['application_date'].dt.year
loans_df['month'] = loans_df['application_date'].dt.month
loans_df['day'] = loans_df['application_date'].dt.day
loans_df['day_of_week'] = loans_df['application_date'].dt.day_name()

print("\nDate components (first 5 rows):")
print(loans_df[['application_date', 'year', 'month', 'day', 'day_of_week']].head())

# Analyze by time period
print("\nDefault rate by year:")
default_by_year = loans_df.groupby('year')['default'].mean().sort_index()
print(default_by_year)

print("\nDefault rate by month:")
default_by_month = loans_df.groupby('month')['default'].mean().sort_index()
print(default_by_month)

print("\nDefault rate by day of week:")
default_by_dow = loans_df.groupby('day_of_week')['default'].mean().sort_values()
print(default_by_dow)

# 5. Data Cleaning and Preprocessing
print("\n5. Data Cleaning and Preprocessing")
print("--------------------------------")

# Create a copy of the DataFrame for cleaning
loans_clean = loans_df.copy()

# Check for duplicates
print("\nNumber of duplicate rows:", loans_clean.duplicated().sum())

# Remove duplicates if any
if loans_clean.duplicated().sum() > 0:
    loans_clean = loans_clean.drop_duplicates()
    print("Duplicates removed.")

# Handling outliers
print("\nLoan amount statistics:")
print(loans_clean['loan_amount'].describe())

# Identify outliers using IQR
Q1 = loans_clean['loan_amount'].quantile(0.25)
Q3 = loans_clean['loan_amount'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"\nIQR range for loan amount: {lower_bound:.2f} to {upper_bound:.2f}")
outliers = loans_clean[(loans_clean['loan_amount'] < lower_bound) | 
                       (loans_clean['loan_amount'] > upper_bound)]
print(f"Number of outliers: {len(outliers)}")

# Handling categorical variables
print("\nEncoding education levels:")
education_mapping = {
    'High School': 0,
    'Bachelor': 1,
    'Master': 2,
    'PhD': 3,
    'Other': -1
}
loans_clean['education_code'] = loans_clean['education'].map(education_mapping)
print(loans_clean[['education', 'education_code']].drop_duplicates().sort_values('education_code'))

# One-hot encoding
print("\nOne-hot encoding for occupation:")
occupation_dummies = pd.get_dummies(loans_clean['occupation'], prefix='job')
print(f"Original column count: {loans_clean.shape[1]}")
print(f"After one-hot encoding occupations: {(loans_clean.shape[1] + occupation_dummies.shape[1] - 1)}")
print(f"First 5 occupation dummy columns: {list(occupation_dummies.columns[:5])}")

# 6. Advanced Indexing and Selection
print("\n6. Advanced Indexing and Selection")
print("--------------------------------")

# Set index to application_id
loans_indexed = loans_clean.set_index('application_id')
print("\nDataFrame with application_id as index (first 3 rows):")
print(loans_indexed.head(3))

# MultiIndex - groupby with as_index=False creates a MultiIndex
multi_index_df = loans_clean.groupby(['education', 'gender'], as_index=False).mean()
print("\nMultiIndex DataFrame:")
print(multi_index_df.head())

# Convert to proper MultiIndex
proper_multi = loans_clean.groupby(['education', 'gender']).mean()
print("\nProper MultiIndex DataFrame:")
print(proper_multi.head())

# Selecting from MultiIndex
print("\nSelecting a specific group:")
print(proper_multi.loc['Bachelor'])
print("\nSelecting a specific subgroup:")
print(proper_multi.loc[('Bachelor', 'M')])

# 7. Apply, Map, and Vectorized Operations
print("\n7. Apply, Map, and Vectorized Operations")
print("--------------------------------------")

# Apply a function to each column
print("\nNormalizing loan amounts (z-score):")
def normalize(x):
    return (x - x.mean()) / x.std()

loans_clean[['loan_amount_normalized']] = loans_clean[['loan_amount']].apply(normalize)
print(loans_clean[['loan_amount', 'loan_amount_normalized']].head())

# Apply a function to each row
print("\nCalculating risk score based on multiple factors:")
def risk_score(row):
    base_score = 500
    # Higher credit score is better
    base_score += (row['credit_score'] - 650) * 0.5
    # Lower loan-to-income ratio is better
    ratio = row['loan_amount'] / row['income']
    if ratio > 3:
        base_score -= 100
    elif ratio > 2:
        base_score -= 50
    elif ratio > 1:
        base_score -= 10
    # Previous defaults are bad
    if row['previous_defaults'] > 0:
        base_score -= 200
    return max(0, min(base_score, 1000))  # Cap between 0 and 1000

loans_clean['risk_score'] = loans_clean.apply(risk_score, axis=1)
print(loans_clean[['loan_amount', 'income', 'credit_score', 'previous_defaults', 'risk_score']].head())
    
# Map values using a dictionary
print("\nMapping risk scores to categories:")
risk_categories = {
    (0, 300): 'Very High Risk',
    (300, 500): 'High Risk',
    (500, 700): 'Medium Risk',
    (700, 850): 'Low Risk',
    (850, 1001): 'Very Low Risk'
}

def categorize_risk(score):
    for range_key, category in risk_categories.items():
        if range_key[0] <= score < range_key[1]:
            return category
    return 'Unknown'

loans_clean['risk_category'] = loans_clean['risk_score'].apply(categorize_risk)
print(loans_clean[['risk_score', 'risk_category']].head(10))

# Vector operations are faster than apply
print("\nVector operations vs. apply (creating a debt-to-income ratio):")

# Time the apply method
import time
start = time.time()
loans_clean['dti_apply'] = loans_clean.apply(lambda row: row['monthly_payment'] / (row['income'] / 12), axis=1)
apply_time = time.time() - start
print(f"Apply method time: {apply_time:.6f} seconds")

# Time the vectorized method
start = time.time()
loans_clean['dti_vector'] = loans_clean['monthly_payment'] / (loans_clean['income'] / 12)
vector_time = time.time() - start
print(f"Vectorized method time: {vector_time:.6f} seconds")
print(f"Speedup: {apply_time / vector_time:.1f}x faster")

# 8. Advanced Analysis with the Loan Dataset
print("\n8. Advanced Analysis with the Loan Dataset")
print("----------------------------------------")

# Correlation analysis
print("\nCorrelation matrix for key variables:")
correlation = loans_clean[['age', 'income', 'loan_amount', 'interest_rate', 
                          'monthly_payment', 'credit_score', 'default']].corr()
print(correlation)

# Feature importance analysis using basic statistics
print("\nFeature importance for default prediction:")
default_correlation = correlation['default'].sort_values(ascending=False)
print(default_correlation)

# Creating an approval recommendation model
print("\nCreating a simple loan approval recommendation system:")
def approval_recommendation(row):
    # Simple rule-based system
    if row['credit_score'] < 600:
        return 'Decline'
    
    dti = row['monthly_payment'] / (row['income'] / 12)
    if dti > 0.4:  # Debt-to-income ratio too high
        return 'Decline'
    
    if row['previous_defaults'] > 0:
        return 'Review'
    
    if row['loan_amount'] > row['income'] * 3:
        return 'Review'
    
    return 'Approve'

loans_clean['recommendation'] = loans_clean.apply(approval_recommendation, axis=1)
print(loans_clean[['credit_score', 'monthly_payment', 'income', 'previous_defaults', 'recommendation']].head(10))

# Summarize recommendations
print("\nRecommendation distribution:")
print(loans_clean['recommendation'].value_counts())

# Compare with actual defaults
print("\nDefault rate by recommendation:")
print(loans_clean.groupby('recommendation')['default'].mean().sort_values())

print("\n--- Exercise ---")
print("Using the loan applications dataset:")
print("1. Create a pivot table showing default rates by education level and employment length ranges")
print("2. Develop a more sophisticated risk scoring model using multiple factors")
print("3. Build a feature that identifies 'suspicious applications' based on outlier detection")
print("4. Calculate loan approval rates by month and visualize the trend")