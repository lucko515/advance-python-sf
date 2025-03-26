# 06: Integrated Data Analysis Workflow
print("Integrated Data Analysis: From Raw Data to Insights")
print("---------------------------------------------------")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier

# Set style for visualizations
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('viridis')

# 1. Define the Problem and Analysis Goals
print("\n1. Problem Statement and Analysis Goals")
print("-------------------------------------")
print("Problem: Predicting loan defaults and understanding risk factors")
print("Goals:")
print("  - Identify key factors that influence loan defaults")
print("  - Build a predictive model for loan default risk")
print("  - Generate actionable insights for loan approval process")

# 2. Load and Explore the Data
print("\n2. Data Loading and Initial Exploration")
print("--------------------------------------")

# Load the loan applications dataset
loan_file = "loan_applications.csv"
loan_path = os.path.join("data_analysis", loan_file)
loans_df = pd.read_csv(loan_path)

# Display basic information
print("\nDataset dimensions:", loans_df.shape)
print("\nFirst 3 rows:")
print(loans_df.head(3))

# Check data types and missing values
print("\nData types and non-null counts:")
print(loans_df.info())

# Statistical summary
print("\nNumerical columns summary:")
print(loans_df.describe())

# Target variable distribution
print("\nDefault rate:")
default_rate = loans_df['default'].mean() * 100
print(f"{default_rate:.2f}% of loans defaulted")

# 3. Data Cleaning and Preprocessing
print("\n3. Data Cleaning and Preprocessing")
print("--------------------------------")

# Create a copy for cleaning
loans_clean = loans_df.copy()

# Convert application_date to datetime
loans_clean['application_date'] = pd.to_datetime(loans_clean['application_date'])

# Extract date components for time-based analysis
loans_clean['year'] = loans_clean['application_date'].dt.year
loans_clean['month'] = loans_clean['application_date'].dt.month
loans_clean['day_of_week'] = loans_clean['application_date'].dt.day_name()

# Check for and handle duplicates
dupe_count = loans_clean.duplicated().sum()
if dupe_count > 0:
    print(f"Found {dupe_count} duplicate rows, removing them.")
    loans_clean = loans_clean.drop_duplicates()
else:
    print("No duplicate rows found.")

# Check for missing values
missing_values = loans_clean.isnull().sum()
print("\nMissing values by column:")
print(missing_values[missing_values > 0] if missing_values.any() else "No missing values")

# Look for outliers using IQR method
def detect_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

# Check for outliers in key numerical columns
for column in ['income', 'loan_amount', 'interest_rate', 'credit_score']:
    outliers, lb, ub = detect_outliers(loans_clean, column)
    print(f"\nOutliers in {column}: {len(outliers)} rows")
    print(f"  Range: {lb:.2f} to {ub:.2f}")
    
# 4. Feature Engineering
print("\n4. Feature Engineering")
print("--------------------")

# Create derived variables that might help with prediction
print("Creating derived features to improve analysis...")

# Loan-to-income ratio (measure of debt burden)
loans_clean['loan_to_income_ratio'] = loans_clean['loan_amount'] / loans_clean['income']
print("- Added loan_to_income_ratio")

# Monthly payment as percentage of monthly income
loans_clean['payment_to_income_ratio'] = loans_clean['monthly_payment'] / (loans_clean['income'] / 12)
print("- Added payment_to_income_ratio")

# Categorize credit scores
bins = [300, 580, 670, 740, 800, 850]
labels = ['Very Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
loans_clean['credit_score_category'] = pd.cut(loans_clean['credit_score'], bins=bins, labels=labels)
print("- Added credit_score_category")

# Age groups
age_bins = [18, 25, 35, 45, 55, 65, 100]
age_labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
loans_clean['age_group'] = pd.cut(loans_clean['age'], bins=age_bins, labels=age_labels)
print("- Added age_group")

# Employment length categories
emp_bins = [0, 1, 3, 5, 10, 100]
emp_labels = ['<1 year', '1-3 years', '3-5 years', '5-10 years', '10+ years']
loans_clean['employment_length_category'] = pd.cut(loans_clean['employment_length'], bins=emp_bins, labels=emp_labels)
print("- Added employment_length_category")

# Loan term categories
loans_clean['loan_term_category'] = pd.cut(loans_clean['loan_term'], 
                                          bins=[0, 12, 36, 60, 84, 360], 
                                          labels=['≤1 year', '1-3 years', '3-5 years', '5-7 years', '>7 years'])
print("- Added loan_term_category")

# Interest rate categories
loans_clean['interest_rate_category'] = pd.cut(loans_clean['interest_rate'],
                                              bins=[0, 5, 10, 15, 20, 100],
                                              labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
print("- Added interest_rate_category")

# 5. Exploratory Data Analysis (EDA)
print("\n5. Exploratory Data Analysis")
print("--------------------------")

# Create a figure for correlation heatmap
plt.figure(figsize=(12, 10))
numeric_cols = ['age', 'income', 'loan_amount', 'loan_term', 'interest_rate', 
                'monthly_payment', 'credit_score', 'employment_length', 
                'existing_loans', 'previous_defaults', 'default',
                'loan_to_income_ratio', 'payment_to_income_ratio']

correlation = loans_clean[numeric_cols].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', linewidths=0.5, fmt='.2f', cbar_kws={'shrink': .8})
plt.title('Correlation Matrix of Numeric Variables', fontsize=16)
plt.tight_layout()
plt.show()

# Default rates by different categorical variables
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Default Rates by Various Factors', fontsize=18)

# Education
default_by_education = loans_clean.groupby('education')['default'].mean().sort_values(ascending=False) * 100
axes[0, 0].bar(default_by_education.index, default_by_education.values, color='skyblue')
axes[0, 0].set_title('Default Rate by Education')
axes[0, 0].set_ylabel('Default Rate (%)')
axes[0, 0].tick_params(axis='x', rotation=45)
for i, v in enumerate(default_by_education.values):
    axes[0, 0].text(i, v + 0.5, f'{v:.1f}%', ha='center')

# Occupation (top 8)
top_occupations = loans_clean['occupation'].value_counts().nlargest(8).index
default_by_occupation = loans_clean[loans_clean['occupation'].isin(top_occupations)].groupby('occupation')['default'].mean().sort_values(ascending=False) * 100
axes[0, 1].bar(default_by_occupation.index, default_by_occupation.values, color='salmon')
axes[0, 1].set_title('Default Rate by Occupation (Top 8)')
axes[0, 1].tick_params(axis='x', rotation=45)
for i, v in enumerate(default_by_occupation.values):
    axes[0, 1].text(i, v + 0.5, f'{v:.1f}%', ha='center')

# Credit score category
default_by_credit = loans_clean.groupby('credit_score_category')['default'].mean().sort_values(ascending=False) * 100
axes[0, 2].bar(default_by_credit.index, default_by_credit.values, color='lightgreen')
axes[0, 2].set_title('Default Rate by Credit Score Category')
axes[0, 2].tick_params(axis='x', rotation=45)
for i, v in enumerate(default_by_credit.values):
    axes[0, 2].text(i, v + 0.5, f'{v:.1f}%', ha='center')

# Loan term category
default_by_term = loans_clean.groupby('loan_term_category')['default'].mean().sort_values(ascending=False) * 100
axes[1, 0].bar(default_by_term.index, default_by_term.values, color='lightskyblue')
axes[1, 0].set_title('Default Rate by Loan Term')
axes[1, 0].set_ylabel('Default Rate (%)')
axes[1, 0].tick_params(axis='x', rotation=45)
for i, v in enumerate(default_by_term.values):
    axes[1, 0].text(i, v + 0.5, f'{v:.1f}%', ha='center')

# Employment length category
default_by_emp = loans_clean.groupby('employment_length_category')['default'].mean().sort_values(ascending=False) * 100
axes[1, 1].bar(default_by_emp.index, default_by_emp.values, color='plum')
axes[1, 1].set_title('Default Rate by Employment Length')
axes[1, 1].tick_params(axis='x', rotation=45)
for i, v in enumerate(default_by_emp.values):
    axes[1, 1].text(i, v + 0.5, f'{v:.1f}%', ha='center')

# Interest rate category
default_by_interest = loans_clean.groupby('interest_rate_category')['default'].mean() * 100
axes[1, 2].bar(default_by_interest.index, default_by_interest.values, color='peachpuff')
axes[1, 2].set_title('Default Rate by Interest Rate Category')
axes[1, 2].tick_params(axis='x', rotation=45)
for i, v in enumerate(default_by_interest.values):
    axes[1, 2].text(i, v + 0.5, f'{v:.1f}%', ha='center')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

# Loan to income ratio vs payment to income ratio by default status
plt.figure(figsize=(12, 8))
plt.scatter(loans_clean[loans_clean['default'] == 0]['loan_to_income_ratio'],
            loans_clean[loans_clean['default'] == 0]['payment_to_income_ratio'],
            alpha=0.5, c='blue', label='Not Defaulted')
plt.scatter(loans_clean[loans_clean['default'] == 1]['loan_to_income_ratio'],
            loans_clean[loans_clean['default'] == 1]['payment_to_income_ratio'],
            alpha=0.5, c='red', label='Defaulted')
plt.title('Loan-to-Income Ratio vs. Payment-to-Income Ratio by Default Status', fontsize=16)
plt.xlabel('Loan-to-Income Ratio')
plt.ylabel('Payment-to-Income Ratio')
plt.legend()
plt.grid(True, alpha=0.3)
# Limit axes to avoid extreme outliers
plt.xlim(0, 5)
plt.ylim(0, 1)
plt.show()

# Distribution of credit scores by default status
plt.figure(figsize=(12, 6))
plt.hist(loans_clean[loans_clean['default'] == 0]['credit_score'], bins=30, alpha=0.5, color='blue', label='Not Defaulted')
plt.hist(loans_clean[loans_clean['default'] == 1]['credit_score'], bins=30, alpha=0.5, color='red', label='Defaulted')
plt.title('Distribution of Credit Scores by Default Status', fontsize=16)
plt.xlabel('Credit Score')
plt.ylabel('Count')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# 6. Prepare Data for Modeling
print("\n6. Prepare Data for Modeling")
print("---------------------------")

# Select features for model
print("Selecting features for modeling...")
model_features = [
    'age', 'income', 'loan_amount', 'loan_term', 'interest_rate', 
    'monthly_payment', 'credit_score', 'employment_length', 
    'existing_loans', 'previous_defaults', 'loan_to_income_ratio', 
    'payment_to_income_ratio'
]

# Also include categorical variables using one-hot encoding
categorical_features = ['gender', 'education', 'occupation']
model_data = pd.get_dummies(loans_clean, columns=categorical_features, drop_first=True)

# Define X (features) and y (target)
X = model_data[model_features].copy()
y = model_data['default'].copy()

print(f"Selected {len(model_features)} numerical features")
print(f"After one-hot encoding, feature count expanded to {X.shape[1]}")

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
print(f"Training set: {X_train.shape[0]} samples")
print(f"Testing set: {X_test.shape[0]} samples")

# Scale numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 7. Build and Evaluate Models
print("\n7. Model Building and Evaluation")
print("------------------------------")

# Logistic Regression Model
print("\nTraining Logistic Regression model...")
log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_train_scaled, y_train)

# Predictions
y_pred_log = log_reg.predict(X_test_scaled)
y_pred_prob_log = log_reg.predict_proba(X_test_scaled)[:, 1]

# Evaluation
print("\nLogistic Regression - Classification Report:")
print(classification_report(y_test, y_pred_log))

# Calculate confusion matrix
cm_log = confusion_matrix(y_test, y_pred_log)
# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm_log, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['No Default', 'Default'],
            yticklabels=['No Default', 'Default'])
plt.title('Logistic Regression - Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.show()

# Feature importance
coef_df = pd.DataFrame({
    'Feature': model_features,
    'Coefficient': log_reg.coef_[0]
})
coef_df = coef_df.reindex(coef_df['Coefficient'].abs().sort_values(ascending=False).index)

plt.figure(figsize=(12, 8))
plt.barh(coef_df['Feature'], coef_df['Coefficient'])
plt.title('Logistic Regression - Feature Importance')
plt.xlabel('Coefficient Value')
plt.ylabel('Feature')
plt.axvline(x=0, color='gray', linestyle='-')
plt.grid(axis='x', alpha=0.3)
plt.show()

# Random Forest Model
print("\nTraining Random Forest model...")
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)  # Random Forest doesn't require scaling

# Predictions
y_pred_rf = rf.predict(X_test)
y_pred_prob_rf = rf.predict_proba(X_test)[:, 1]

# Evaluation
print("\nRandom Forest - Classification Report:")
print(classification_report(y_test, y_pred_rf))

# Calculate confusion matrix
cm_rf = confusion_matrix(y_test, y_pred_rf)
# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['No Default', 'Default'],
            yticklabels=['No Default', 'Default'])
plt.title('Random Forest - Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.show()

# Feature importance
feat_importance = pd.DataFrame({
    'Feature': model_features,
    'Importance': rf.feature_importances_
})
feat_importance = feat_importance.sort_values('Importance', ascending=False)

plt.figure(figsize=(12, 8))
plt.barh(feat_importance['Feature'], feat_importance['Importance'])
plt.title('Random Forest - Feature Importance')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.grid(axis='x', alpha=0.3)
plt.show()

# Compare ROC curves
plt.figure(figsize=(10, 8))
# Logistic Regression ROC
fpr_log, tpr_log, _ = roc_curve(y_test, y_pred_prob_log)
roc_auc_log = auc(fpr_log, tpr_log)
plt.plot(fpr_log, tpr_log, label=f'Logistic Regression (AUC = {roc_auc_log:.3f})')

# Random Forest ROC
fpr_rf, tpr_rf, _ = roc_curve(y_test, y_pred_prob_rf)
roc_auc_rf = auc(fpr_rf, tpr_rf)
plt.plot(fpr_rf, tpr_rf, label=f'Random Forest (AUC = {roc_auc_rf:.3f})')

# Diagonal line (random classifier)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)
plt.show()

# 8. Insights and Recommendations
print("\n8. Key Insights and Recommendations")
print("---------------------------------")

print("Based on our analysis, here are the key insights about loan defaults:")

# Find top positive and negative coefficients from logistic regression
top_pos_coef = coef_df[coef_df['Coefficient'] > 0].head(3)
top_neg_coef = coef_df[coef_df['Coefficient'] < 0].head(3)

print("\nTop factors increasing default risk:")
for _, row in top_pos_coef.iterrows():
    print(f"- {row['Feature']}: {row['Coefficient']:.4f}")

print("\nTop factors decreasing default risk:")
for _, row in top_neg_coef.iterrows():
    print(f"- {row['Feature']}: {row['Coefficient']:.4f}")

# Top features from random forest
print("\nMost important factors according to Random Forest:")
for _, row in feat_importance.head(5).iterrows():
    print(f"- {row['Feature']}: {row['Importance']:.4f}")

print("\nRecommendations for loan approval process:")
print("1. Focus on payment-to-income ratio as a key risk indicator")
print("2. Set stricter requirements for applicants with low credit scores")
print("3. Consider offering lower interest rates to reduce default probability")
print("4. Implement different risk thresholds based on education and occupation")
print("5. Monitor the loan-to-income ratio closely during application review")

print("\n--- Exercise ---")
print("Using the loan applications dataset:")
print("1. Build a more advanced model with additional features or a different algorithm")
print("2. Create a visualization dashboard focused on a specific aspect of loan defaults")
print("3. Develop a risk scoring system based on the insights from our analysis")
print("4. Design a procedure for identifying high-risk applications during the review process")