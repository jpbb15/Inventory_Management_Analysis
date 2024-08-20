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

def save_manipulated_data(df_selected, output_file='data_manipulated.csv'):
    """Saves the manipulated data to a CSV file and prints a confirmation message."""
    df_selected.to_csv(output_file, index=False)
    print(f"Data manipulation completed and saved to {output_file}.")