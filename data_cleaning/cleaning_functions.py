import panda as pd

def convert_to_datetime(df, column_name):
    """Convert a column to datetime format."""
    df[column_name] = pd.to_datetime(df[column_name])
    return df

def fill_missing_values(df, column_name, fill_value):
    """Fill missing values in a specified column."""
    df[column_name] = df[column_name].fillna(fill_value)
    return df

def convert_to_int(df, column_name):
    """Convert a column to integers."""
    df[column_name] = df[column_name].astype(int)
    return df

def lowercase_columns(df):
    """Convert all column names to lowercase."""
    df.columns = df.columns.str.lower()
    return df

def save_cleaned_data(df, file_path):
    """Save the cleaned dataframe to a CSV file."""
    df.to_csv(file_path, index=False)
    return df