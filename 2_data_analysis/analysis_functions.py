import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

def calculate_purchase_amount(df_analysis):
    """Calculate the total purchase amount for each row."""
    df_analysis['total_purchase'] = df_analysis['quantity'] * df_analysis['unitprice']
    return df_analysis

def calculate_descriptive_stats(df_analysis):
    """Calculate mean, median, and mode for purchase amounts and quantities."""
    purchase_stats = {
        'mean_purchase_amount': df_analysis['total_purchase'].mean(),
        'median_purchase_amount': df_analysis['total_purchase'].median(),
        'mode_purchase_amount': df_analysis['total_purchase'].mode()[0],
        'mean_quantity': df_analysis['quantity'].mean(),
        'median_quantity': df_analysis['quantity'].median(),
        'mode_quantity': df_analysis['quantity'].mode()[0]
    }
    return purchase_stats

def get_top_categories(df_analysis, top_n=5):
    """Identify top N product categories with the highest average purchase amounts."""
    category_avg_purchase = df_analysis.groupby('description')['total_purchase'].mean().sort_values(ascending=False)
    return category_avg_purchase.head(top_n)

def plot_bar_chart(df_analysis):
    """Plot a bar chart showing the top 15 products based on total purchase amounts."""
    # Calculate the total purchase amount for each product category
    category_totals = df_analysis.groupby('description')['total_purchase'].sum().sort_values(ascending=False)
    
    # Select the top 15 product categories
    top_15_categories = category_totals.head(15)
    
    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    top_15_categories.plot(kind='bar')
    plt.title('Top 15 Products by Total Purchase Amount')
    plt.ylabel('Total Purchase Amount')
    plt.xlabel('Product Category')
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels for better readability
    plt.show()

def plot_line_graph(df_analysis):
    """Plot a line graph to visualize sales trends over time with a readable y-axis scale."""
    df_analysis['month'] = pd.to_datetime(df_analysis['invoicedate']).dt.to_period('M')
    monthly_sales = df_analysis.groupby('month')['total_purchase'].sum()
    
    plt.figure(figsize=(10, 6))
    ax = monthly_sales.plot(kind='line')
    
    # Customize y-axis to show values in millions
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
    
    plt.title('Monthly Sales Trends')
    plt.ylabel('Total Sales (in Millions)')
    plt.xlabel('Month')
    plt.show()

def plot_product_cooccurrence_heatmap(df_analysis):
    """Plot a heatmap to identify the co-occurrence of top 15 product purchases."""
    # Calculate the total quantity sold for each product
    top_products = df_analysis.groupby('description')['quantity'].sum().sort_values(ascending=False).head(15).index
    
    # Filter the dataframe to include only the top 15 products
    top_15_df = df_analysis[df_analysis['description'].isin(top_products)]
    
    # Pivot table to create a binary matrix of products purchased per transaction (invoice)
    cooccurrence_matrix = top_15_df.pivot_table(index='invoiceno', columns='description', values='quantity', aggfunc='sum').fillna(0)
    cooccurrence_matrix = cooccurrence_matrix.applymap(lambda x: 1 if x > 0 else 0)
    
    # Calculate the correlation matrix of product co-occurrence
    correlation_matrix = cooccurrence_matrix.corr()
    
    # Plot the heatmap
    plt.figure(figsize=(14, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Top 15 Product Co-occurrence Correlation Matrix')
    plt.show()

def generate_customer_segments_manual(df_analysis):
    """Generate customer segments based on purchase frequency and total spending using manual bins."""
    
    # Step 1: Calculate total spending and purchase frequency for each customer
    customer_data = df_analysis.groupby('customerid').agg({
        'invoiceno': 'nunique',  # Number of unique invoices (purchase frequency)
        'total_purchase': 'sum'  # Total spending
    }).rename(columns={'invoiceno': 'purchase_frequency', 'total_purchase': 'total_spending'})
    
    # Step 2: Manual binning for segmentation
    spending_bins = [0, 100, 1000, 5000, df_analysis['total_purchase'].max()]
    frequency_bins = [0, 2, 5, 10, df_analysis['invoiceno'].nunique()]
    
    customer_data['spending_segment'] = pd.cut(customer_data['total_spending'], bins=spending_bins, labels=['Low', 'Medium', 'High', 'Very High'])
    customer_data['frequency_segment'] = pd.cut(customer_data['purchase_frequency'], bins=frequency_bins, labels=['Low', 'Medium', 'High', 'Very High'])
    
    # Step 3: Combine segments to identify high-value customers
    customer_data['overall_segment'] = customer_data['spending_segment'].astype(str) + ' Spending / ' + customer_data['frequency_segment'].astype(str) + ' Frequency'
    
    return customer_data

def visualize_customer_segments(customer_data):
    """Visualize customer segments based on spending and frequency."""
    
    # Ensure spending and frequency segments are categorical for better color separation
    customer_data['spending_segment'] = customer_data['spending_segment'].astype('category')
    customer_data['frequency_segment'] = customer_data['frequency_segment'].astype('category')
    
    # Exclude rows with 'nan' in the overall_segment column
    customer_data = customer_data.dropna(subset=['overall_segment'])
    
    # Step 4: Visualize the segments
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=customer_data, x='purchase_frequency', y='total_spending', hue='overall_segment', palette='coolwarm')
    plt.title('Customer Segmentation Based on Spending and Frequency')
    plt.xlabel('Purchase Frequency')
    plt.ylabel('Total Spending')
    plt.yscale('log')  # Use log scale if spending values have a wide range
    plt.xscale('log')  # Use log scale if frequency values have a wide range
    plt.show()

def prepare_monthly_sales(df_analysis):
    """Prepare the monthly sales data aggregated by product category."""
    
    # Convert the 'invoicedate' to a datetime format and extract month and year
    df_analysis['invoicedate'] = pd.to_datetime(df_analysis['invoicedate'])
    df_analysis['month'] = df_analysis['invoicedate'].dt.month
    df_analysis['year'] = df_analysis['invoicedate'].dt.year
    
    # Aggregate sales data by product category and month
    monthly_sales = df_analysis.groupby(['year', 'month', 'description'])['total_purchase'].sum().unstack().fillna(0)
    
    return monthly_sales

def plot_seasonal_trends(monthly_sales, top_n=10):
    """Plot the sales trends for the top N most popular product categories."""
    
    # Select the top N popular product categories for visualization
    popular_categories = monthly_sales.sum().sort_values(ascending=False).head(top_n).index
    
    # Plot the sales trends for these popular categories
    plt.figure(figsize=(14, 8))
    for category in popular_categories:
        plt.plot(monthly_sales.index.get_level_values('month'), monthly_sales[category], label=category)
    
    plt.title('Monthly Sales Trends for Popular Product Categories')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.legend(title='Product Categories')
    plt.show()