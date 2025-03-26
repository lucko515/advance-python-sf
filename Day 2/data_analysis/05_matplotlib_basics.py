# 05: Matplotlib Basics
print("Introduction to Matplotlib: Data Visualization in Python")
print("-------------------------------------------------------")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set a professional style
plt.style.use('seaborn-v0_8-whitegrid')

# 1. Basic Line Plot
print("\n1. Basic Line Plot")
print("----------------")

# Create some simple data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Basic plot
plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.title('Basic Sine Wave')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()

# 2. Customizing Line Plots
print("\n2. Customizing Line Plots")
print("-----------------------")

# Create multiple lines with different styles
plt.figure(figsize=(10, 6))
plt.plot(x, np.sin(x), label='sine', color='blue', linestyle='-', linewidth=2)
plt.plot(x, np.cos(x), label='cosine', color='red', linestyle='--', linewidth=2)
plt.plot(x, np.sin(x + np.pi/4), label='shifted sine', color='green', linestyle=':', linewidth=2)

# Add customization
plt.title('Multiple Trigonometric Functions', fontsize=16)
plt.xlabel('X-axis', fontsize=12)
plt.ylabel('Y-axis', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True)
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)  # Add horizontal line at y=0
plt.axvline(x=5, color='k', linestyle='-', alpha=0.3)  # Add vertical line at x=5

# Add text annotations
plt.annotate('Peak', xy=(1.5, 1), xytext=(3, 1.3),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5))

plt.show()

# 3. Scatter Plots
print("\n3. Scatter Plots")
print("--------------")

# Create random data for scatter plot
np.random.seed(42)  # For reproducibility
x = np.random.rand(50)
y = np.random.rand(50)
colors = np.random.rand(50)
sizes = 1000 * np.random.rand(50)

plt.figure(figsize=(10, 6))
plt.scatter(x, y, c=colors, s=sizes, alpha=0.5, cmap='viridis')
plt.colorbar(label='Color Value')
plt.title('Scatter Plot with Size and Color Mapping')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()

# 4. Bar Plots
print("\n4. Bar Plots")
print("-----------")

# Basic bar plot
categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
values = [25, 40, 30, 55, 15]

plt.figure(figsize=(10, 6))
plt.bar(categories, values, color='skyblue', edgecolor='black')
plt.title('Basic Bar Plot')
plt.xlabel('Category')
plt.ylabel('Value')
plt.ylim(0, 60)  # Set y-axis limits
plt.show()

# Horizontal bar plot
plt.figure(figsize=(10, 6))
plt.barh(categories, values, color='salmon', edgecolor='black')
plt.title('Horizontal Bar Plot')
plt.xlabel('Value')
plt.ylabel('Category')
plt.xlim(0, 60)  # Set x-axis limits
plt.show()

# Grouped bar chart
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(categories))
width = 0.35

group1 = [25, 40, 30, 55, 15]
group2 = [15, 30, 40, 20, 35]

ax.bar(x - width/2, group1, width, label='Group 1', color='skyblue', edgecolor='black')
ax.bar(x + width/2, group2, width, label='Group 2', color='salmon', edgecolor='black')

ax.set_title('Grouped Bar Chart')
ax.set_xlabel('Category')
ax.set_ylabel('Value')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
plt.show()

# 5. Histograms
print("\n5. Histograms")
print("------------")

# Generate random data with normal distribution
data = np.random.randn(1000)

plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Histogram of Random Data')
plt.xlabel('Value')
plt.ylabel('Frequency')

# Add a vertical line at the mean
plt.axvline(data.mean(), color='red', linestyle='dashed', linewidth=2, label=f'Mean: {data.mean():.2f}')
# Add a vertical line at the median
plt.axvline(np.median(data), color='green', linestyle='dashed', linewidth=2, label=f'Median: {np.median(data):.2f}')
plt.legend()
plt.show()

# Multiple histograms
plt.figure(figsize=(10, 6))
plt.hist(np.random.normal(0, 1, 1000), bins=30, alpha=0.5, label='Normal (μ=0, σ=1)', color='blue')
plt.hist(np.random.normal(2, 1, 1000), bins=30, alpha=0.5, label='Normal (μ=2, σ=1)', color='red')
plt.title('Multiple Histograms')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()
plt.show()

# 6. Pie Charts
print("\n6. Pie Charts")
print("------------")

labels = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
sizes = [25, 40, 30, 55, 15]
explode = (0, 0.1, 0, 0, 0)  # Explode the 2nd slice (Category B)

plt.figure(figsize=(10, 8))
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90, colors=plt.cm.Set3.colors)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.title('Basic Pie Chart')
plt.show()

# 7. Box Plots
print("\n7. Box Plots")
print("-----------")

# Generate random data
data = [np.random.normal(0, std, 100) for std in range(1, 6)]
labels = ['Group A', 'Group B', 'Group C', 'Group D', 'Group E']

plt.figure(figsize=(10, 6))
plt.boxplot(data, labels=labels, patch_artist=True, 
            boxprops=dict(facecolor='lightblue'),
            medianprops=dict(color='red'))
plt.title('Box Plot of Different Groups')
plt.xlabel('Group')
plt.ylabel('Value')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# 8. Subplots
print("\n8. Subplots")
print("-----------")

# Create a figure with a 2x2 grid of subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Multiple Plots in a Figure', fontsize=16)

# Line plot (top-left)
axes[0, 0].plot(x, np.sin(x), color='blue')
axes[0, 0].set_title('Line Plot')
axes[0, 0].set_xlabel('X-axis')
axes[0, 0].set_ylabel('Y-axis')

# Scatter plot (top-right)
axes[0, 1].scatter(np.random.rand(50), np.random.rand(50), color='red', alpha=0.5)
axes[0, 1].set_title('Scatter Plot')
axes[0, 1].set_xlabel('X-axis')
axes[0, 1].set_ylabel('Y-axis')

# Bar plot (bottom-left)
axes[1, 0].bar(['A', 'B', 'C', 'D'], [10, 20, 15, 25], color='green')
axes[1, 0].set_title('Bar Plot')
axes[1, 0].set_xlabel('Category')
axes[1, 0].set_ylabel('Value')

# Histogram (bottom-right)
axes[1, 1].hist(np.random.normal(0, 1, 1000), bins=20, color='purple', alpha=0.7)
axes[1, 1].set_title('Histogram')
axes[1, 1].set_xlabel('Value')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make room for the figure title
plt.show()

# 9. Saving Figures
print("\n9. Saving Figures")
print("---------------")

# Create a simple figure
plt.figure(figsize=(8, 6))
plt.plot(np.arange(10), np.arange(10) ** 2, 'b-')
plt.title('Quadratic Function')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Save the figure with different formats and settings
plt.savefig(os.path.join('data_analysis', 'quadratic.png'), dpi=300, bbox_inches='tight')
print("Figure saved as 'data_analysis/quadratic.png'")

# Close the figure to free up memory
plt.close()

# 10. Working with Real Data - Loan Dataset
print("\n10. Visualizing Loan Application Data")
print("----------------------------------")

# Load the loan dataset
loan_file = "loan_applications.csv"
loan_path = os.path.join("data_analysis", loan_file)
loans_df = pd.read_csv(loan_path)

# Visualizing the distribution of loan amounts
plt.figure(figsize=(10, 6))
plt.hist(loans_df['loan_amount'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Distribution of Loan Amounts')
plt.xlabel('Loan Amount ($)')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
plt.show()

# Scatter plot of income vs. loan amount, colored by default status
plt.figure(figsize=(10, 8))
default_mask = loans_df['default'] == 1

plt.scatter(loans_df.loc[~default_mask, 'income'], 
            loans_df.loc[~default_mask, 'loan_amount'],
            c='blue', alpha=0.5, label='Non-Default')
            
plt.scatter(loans_df.loc[default_mask, 'income'], 
            loans_df.loc[default_mask, 'loan_amount'],
            c='red', alpha=0.5, label='Default')
            
plt.title('Income vs. Loan Amount by Default Status')
plt.xlabel('Income ($)')
plt.ylabel('Loan Amount ($)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Bar chart of default rate by education level
default_by_education = loans_df.groupby('education')['default'].mean().sort_values(ascending=False) * 100

plt.figure(figsize=(10, 6))
bars = plt.bar(default_by_education.index, default_by_education.values, color='salmon', edgecolor='black')
plt.title('Default Rate by Education Level')
plt.xlabel('Education Level')
plt.ylabel('Default Rate (%)')
plt.ylim(0, default_by_education.max() * 1.1)  # Add some space above the highest bar

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{height:.1f}%', ha='center', va='bottom')

plt.show()

# Box plot of credit scores by occupation
plt.figure(figsize=(12, 8))
occupations = loans_df['occupation'].value_counts().nlargest(8).index
occupation_data = [loans_df[loans_df['occupation'] == occ]['credit_score'] for occ in occupations]

plt.boxplot(occupation_data, labels=occupations, patch_artist=True)
plt.title('Credit Score Distribution by Occupation (Top 8)')
plt.xlabel('Occupation')
plt.ylabel('Credit Score')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Multiple subplots to compare different aspects of the data
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle('Loan Application Analysis Dashboard', fontsize=16)

# Top left: Distribution of loan terms
axes[0, 0].hist(loans_df['loan_term'], bins=np.unique(loans_df['loan_term']).size, 
                color='skyblue', edgecolor='black')
axes[0, 0].set_title('Distribution of Loan Terms')
axes[0, 0].set_xlabel('Term (months)')
axes[0, 0].set_ylabel('Count')

# Top right: Interest rate vs. credit score
axes[0, 1].scatter(loans_df['credit_score'], loans_df['interest_rate'], 
                  alpha=0.5, c=loans_df['loan_amount'], cmap='viridis')
axes[0, 1].set_title('Interest Rate vs. Credit Score')
axes[0, 1].set_xlabel('Credit Score')
axes[0, 1].set_ylabel('Interest Rate (%)')
axes[0, 1].grid(True, alpha=0.3)

# Bottom left: Default rate by gender
gender_default = loans_df.groupby('gender')['default'].mean() * 100
axes[1, 0].bar(gender_default.index, gender_default.values, color=['skyblue', 'salmon'])
axes[1, 0].set_title('Default Rate by Gender')
axes[1, 0].set_xlabel('Gender')
axes[1, 0].set_ylabel('Default Rate (%)')
for i, v in enumerate(gender_default.values):
    axes[1, 0].text(i, v + 0.1, f'{v:.1f}%', ha='center')

# Bottom right: Age distribution
axes[1, 1].hist(loans_df['age'], bins=30, color='green', alpha=0.7, edgecolor='black')
axes[1, 1].set_title('Age Distribution of Applicants')
axes[1, 1].set_xlabel('Age')
axes[1, 1].set_ylabel('Count')
axes[1, 1].axvline(loans_df['age'].mean(), color='red', linestyle='dashed', 
                  linewidth=2, label=f'Mean: {loans_df["age"].mean():.1f}')
axes[1, 1].legend()

plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout for the figure title
plt.show()

print("\n--- Exercise ---")
print("Using the loan applications dataset:")
print("1. Create a scatter plot of loan amount vs. monthly payment, colored by default status")
print("2. Make a grouped bar chart showing average credit scores by education level and gender")
print("3. Create a pie chart showing the distribution of occupations")
print("4. Design a dashboard with 4 different visualizations that tell a story about the data")