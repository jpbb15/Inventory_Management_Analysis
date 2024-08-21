import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_top_selling_categories(df, top_n=10):
    """Plot the top N selling product categories based on total sales."""
    category_totals = df.groupby('description')['total_purchase'].sum().sort_values(ascending=False).head(top_n)
    plt.figure(figsize=(12, 6))
    category_totals.plot(kind='bar', color='skyblue')
    plt.title(f'Top {top_n} Selling Product Categories')
    plt.ylabel('Total Sales Amount')
    plt.xlabel('Product Category')
    plt.xticks(rotation=45, ha='right')
    plt.show()

def plot_monthly_sales_trends(df):
    """Plot monthly sales trends over time."""
    df['month_year'] = pd.to_datetime(df['invoicedate']).dt.to_period('M')
    monthly_sales = df.groupby('month_year')['total_purchase'].sum()
    plt.figure(figsize=(12, 6))
    monthly_sales.plot(kind='line', marker='o', color='blue')
    plt.title('Monthly Sales Trends')
    plt.ylabel('Total Sales Amount')
    plt.xlabel('Month-Year')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

def plot_customer_segment_boxplot(df):
    """Plot the distribution of total purchases across different customer segments."""
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='purchase_frequency_segment', y='total_purchase', data=df, palette='coolwarm')
    plt.title('Distribution of Total Purchases by Customer Segment')
    plt.xlabel('Customer Segment')
    plt.ylabel('Total Purchase Amount')
    plt.show()

def plot_sales_by_day_of_week(df):
    """Plot total sales by day of the week."""
    sales_by_day = df.groupby('day_of_week')['total_purchase'].sum()
    plt.figure(figsize=(10, 5))
    sales_by_day.plot(kind='bar', color='orange')
    plt.title('Sales by Day of the Week')
    plt.ylabel('Total Sales Amount')
    plt.xlabel('Day of the Week')
    plt.xticks(rotation=0)
    plt.show()

def statistical_summary(df):
    """Print a statistical summary of key features in the dataset."""
    print("Statistical Summary of Key Features")
    print(df.describe())
    
    # Example: Group-wise analysis summary if available
    if 'purchase_frequency_segment' in df.columns:
        print("\nGroup-wise analysis of total_purchase by purchase_frequency_segment:")
        print(df.groupby('purchase_frequency_segment')['total_purchase'].describe())

