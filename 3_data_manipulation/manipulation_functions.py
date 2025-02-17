import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def identify_outliers(df, column):
    """Identify outliers in a specified column using the IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers

def cap_outliers(df, column):
    """Cap outliers at the upper and lower bounds of the IQR."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Cap the values at the lower and upper bounds
    df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])
    df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
    
    return df

def visualize_outliers(df, column):
    """Visualize the distribution of a column with outliers highlighted."""
    plt.figure(figsize=(12, 6))
    
    # Plot the distribution of the column
    sns.boxplot(x=df[column])
    
    # Add titles and labels
    plt.title(f'Boxplot of {column} with Outliers Highlighted')
    plt.xlabel(column)
    
    plt.show()

def type_casting(df_manipulation):
    """Ensures all fields are in the correct format."""
    
    # Convert 'invoicedate' to datetime if not already done
    df_manipulation['invoicedate'] = pd.to_datetime(df_manipulation['invoicedate'])
    
    # Ensure 'quantity' and 'unitprice' are floats
    df_manipulation['quantity'] = df_manipulation['quantity'].astype(float)
    df_manipulation['unitprice'] = df_manipulation['unitprice'].astype(float)
    
    return df_manipulation

def select_features(df_manipulation):
    """Selects the relevant features for analysis based on project objectives."""
    
    # Define the relevant features to keep
    features = ['invoicedate', 'customerid', 'description', 'quantity', 'unitprice', 'total_purchase', 'country']
    
    # Check if all features are available in the dataframe, if not, drop the unavailable ones
    features = [feature for feature in features if feature in df_manipulation.columns]
    
    df_selected = df_manipulation[features]
    
    return df_selected

def one_hot_encode(df_manipulation):
    """Applies one-hot encoding to the product categories."""
    df_encoded = pd.get_dummies(df_manipulation, columns=['description'], prefix='category')
    return df_encoded

def extract_date_features(df_manipulation):
    """Extracts useful features from the invoicedate, including year, month, and day."""
    df_manipulation['year'] = df_manipulation['invoicedate'].dt.year
    df_manipulation['month'] = df_manipulation['invoicedate'].dt.month
    df_manipulation['day'] = df_manipulation['invoicedate'].dt.day
    df_manipulation['day_of_week'] = df_manipulation['invoicedate'].dt.dayofweek
    return df_manipulation

def correlation_analysis(df_manipulation):
    """Performs a correlation analysis between numerical features and visualizes the results."""
    
    # Drop non-numeric or irrelevant columns before correlation analysis
    columns_to_exclude = ['customerid', 'invoicedate']
    df_numerical = df_manipulation.drop(columns=columns_to_exclude, errors='ignore')
    
    # Ensure only numerical columns are kept
    df_numerical = df_numerical.select_dtypes(include=[np.number])
    
    # Compute the correlation matrix
    correlation_matrix = df_numerical.corr()
    
    # Visualize the correlation matrix using a heatmap
    plt.figure(figsize=(14, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title("Correlation Matrix")
    plt.show()
    
    return correlation_matrix

def group_analysis(df_manipulation, group_by_column, analysis_column):
    """Performs a group-wise analysis to understand customer behavior."""
    # Perform group-wise analysis and compute descriptive statistics
    group_data = df_manipulation.groupby(group_by_column)[analysis_column].describe()
    
    # Display the results
    print(f"Group-wise analysis of {analysis_column} by {group_by_column}:")
    print(group_data)
    
    # Optionally, visualize the distribution of the analysis_column within each group
    plt.figure(figsize=(12, 6))
    sns.boxplot(x=group_by_column, y=analysis_column, data=df_manipulation)
    plt.title(f'Distribution of {analysis_column} by {group_by_column}')
    plt.show()
    
    return group_data

def save_manipulated_data(df_selected, output_file='data_manipulated.csv'):
    """Saves the manipulated data to a CSV file and prints a confirmation message."""
    df_selected.to_csv(output_file, index=False)
    print(f"Data manipulation completed and saved to {output_file}.")