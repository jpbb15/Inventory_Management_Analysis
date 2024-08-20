import numpy as np
import pandas as pd

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