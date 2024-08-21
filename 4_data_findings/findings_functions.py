import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    """
    Load the dataset from a CSV file.
    """
    data = pd.read_csv(file_path)
    data['invoicedate'] = pd.to_datetime(data['invoicedate'])
    data['month_year'] = data['invoicedate'].dt.to_period('M')
    return data

def plot_monthly_sales_trend(data):
    """
    Plot the monthly sales trend.
    """
    monthly_sales = data.groupby('month_year')['total_purchase'].sum().reset_index()
    monthly_sales['month_year'] = monthly_sales['month_year'].astype(str)

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='month_year', y='total_purchase', data=monthly_sales, marker='o')
    plt.title('Monthly Sales Trend')
    plt.xlabel('Month-Year')
    plt.ylabel('Total Purchase ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_customer_purchase_frequency(data):
    """
    Plot the customer purchase frequency.
    """
    customer_freq = data['customerid'].value_counts().reset_index()
    customer_freq.columns = ['customerid', 'purchase_count']

    plt.figure(figsize=(10, 6))
    sns.histplot(customer_freq['purchase_count'], bins=50, kde=True)
    plt.title('Customer Purchase Frequency')
    plt.xlabel('Number of Purchases')
    plt.ylabel('Number of Customers')
    plt.tight_layout()
    plt.show()

def plot_quantity_distribution(data):
    """
    Plot the distribution of purchase quantities.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(data['quantity'], bins=50, kde=True)
    plt.title('Distribution of Purchase Quantities')
    plt.xlabel('Quantity')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()
