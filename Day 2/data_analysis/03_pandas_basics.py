# 03: Pandas Basics
print("Introduction to Pandas: The Swiss Army Knife for Data Analysis")
print("-------------------------------------------------------------")

import pandas as pd
import numpy as np
import os

# 1. Introduction to Pandas Series
print("\n1. Pandas Series")
print("--------------")

# Series is a one-dimensional labeled array
simple_series = pd.Series([10, 20, 30, 40])
print("Simple Series:")
print(simple_series)

# Series with custom index
labeled_series = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
print("\nSeries with custom index:")
print(labeled_series)

# Series from dictionary
dict_series = pd.Series({'a': 10, 'b': 20, 'c': 30, 'd': 40})
print("\nSeries from dictionary:")
print(dict_series)

# Series operations
print("\nSeries operations:")
print(f"Element at index 'b': {labeled_series['b']}")
print(f"Elements at indices 'a' and 'c': {labeled_series[['a', 'c']]}")
print(f"Elements > 20: {labeled_series[labeled_series > 20]}")

# 2. Introduction to Pandas DataFrame
print("\n2. Pandas DataFrame")
print("------------------")

# Create a DataFrame from a dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston'],
    'Salary': [70000, 80000, 90000, 100000]
}

df = pd.DataFrame(data)
print("DataFrame from dictionary:")
print(df)

# Basic DataFrame attributes
print("\nDataFrame shape:", df.shape)
print("\nDataFrame info:")
print(df.info())
print("\nDataFrame summary statistics:")
print(df.describe())
print("\nDataFrame columns:", df.columns.tolist())
print("DataFame index:", df.index.tolist())
print("DataFame data types:\n", df.dtypes)

# 3. Reading data from files
print("\n3. Reading Data from Files")
print("-----------------------")

# Check if the file exists
loan_file = "loan_applications.csv"
loan_path = os.path.join("data_analysis", loan_file)

print(f"Loading data from '{loan_path}'...")
loans_df = pd.read_csv(loan_path)

# Display basic information
print("\nDataset dimensions:", loans_df.shape)
print("\nFirst 5 rows:")
print(loans_df.head())

# 4. Data exploration
print("\n4. Data Exploration")
print("-----------------")

# Basic information about the dataset
print("\nDataset info:")
print(loans_df.info())

# Statistical summary
print("\nNumerical columns summary:")
print(loans_df.describe())

# Column names and types
print("\nColumn names:")
print(loans_df.columns.tolist())

# Check for missing values
print("\nMissing values per column:")
print(loans_df.isnull().sum())

# 5. Data selection and indexing
print("\n5. Data Selection and Indexing")
print("----------------------------")

# Select a single column (returns a Series)
print("\nApplicant ages:")
print(loans_df['age'].head())

# Select multiple columns (returns a DataFrame)
print("\nSelected columns:")
print(loans_df[['application_id', 'age', 'income', 'loan_amount']].head())

# Select rows by position
print("\nRows 10-15:")
print(loans_df.iloc[10:15])

# Select rows and columns by position
print("\nRows 10-15, columns 1-4:")
print(loans_df.iloc[10:15, 1:5])

# Select rows by label/condition
print("\nApplicants with high income (>100,000):")
high_income = loans_df[loans_df['income'] > 100000]
print(high_income.head())

# More complex conditions
print("\nYoung applicants with high loan amounts:")
young_high_loan = loans_df[(loans_df['age'] < 30) & (loans_df['loan_amount'] > 100000)]
print(young_high_loan.head())

# 6. Basic data manipulation
print("\n6. Basic Data Manipulation")
print("------------------------")

# Create a copy to avoid warnings
loans_copy = loans_df.copy()

# Add a new column: loan amount per year of term
loans_copy['yearly_loan_amount'] = loans_copy['loan_amount'] / loans_copy['loan_term'] * 12
print("\nYearly loan amount (first 5 rows):")
print(loans_copy[['loan_amount', 'loan_term', 'yearly_loan_amount']].head())

# Transform existing column: income in thousands
loans_copy['income_thousands'] = loans_copy['income'] / 1000
print("\nIncome in thousands (first 5 rows):")
print(loans_copy[['income', 'income_thousands']].head())

# 7. Handling missing values
print("\n7. Handling Missing Values")
print("------------------------")

# Create a sample DataFrame with missing values
sample_df = pd.DataFrame({
    'A': [1, 2, np.nan, 4, 5],
    'B': [np.nan, 2, 3, 4, 5],
    'C': [1, 2, 3, np.nan, 5]
})

print("\nSample DataFrame with NaN values:")
print(sample_df)

# Check for missing values
print("\nMissing values in each column:")
print(sample_df.isnull().sum())

# Dropping rows with any missing values
print("\nDropping rows with any NaN values:")
print(sample_df.dropna())

# Dropping rows with all missing values
print("\nDropping rows with all NaN values:")
print(sample_df.dropna(how='all'))

# Filling missing values
print("\nFilling NaN values with 0:")
print(sample_df.fillna(0))

# Filling missing values with column mean
print("\nFilling NaN values with column mean:")
print(sample_df.fillna(sample_df.mean()))

# 8. Exploring the loan applications dataset
print("\n8. Exploring Loan Applications Dataset")
print("------------------------------------")

# Basic categorization
print("\nLoan application results:")
print(loans_df['default'].value_counts())
print("\nPercentage of defaults:")
default_percentage = loans_df['default'].mean() * 100
print(f"{default_percentage:.2f}%")

# Gender distribution
print("\nGender distribution:")
print(loans_df['gender'].value_counts())

# Education distribution
print("\nEducation levels:")
print(loans_df['education'].value_counts())

# Occupation distribution
print("\nTop 5 occupations:")
print(loans_df['occupation'].value_counts().head())

# Numerical variables statistics by loan outcome
print("\nNumerical statistics by default status:")
print(loans_df.groupby('default')['age', 'income', 'loan_amount', 'credit_score'].mean())

print("\n--- Exercise ---")
print("Using the loan applications dataset:")
print("1. Find the average loan amount by education level")
print("2. Calculate the default rate by gender")
print("3. Identify the cities with the highest default rates (min 10 applications)")
print("4. Create a new column 'loan_to_income_ratio' and analyze its relationship with defaults")