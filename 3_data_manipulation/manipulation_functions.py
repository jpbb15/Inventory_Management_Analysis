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

def handle_outliers(df, column, method='remove'):
    """Handle outliers by either removing or capping them."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    if method == 'remove':
        df_cleaned = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    elif method == 'cap':
        df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])
        df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
        df_cleaned = df
    else:
        raise ValueError("Method should be 'remove' or 'cap'")
    
    return df_cleaned