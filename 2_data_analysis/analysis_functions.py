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
    """Plot a heatmap to identify the co-occurrence of product purchases."""
    # Pivot table to create a binary matrix of products purchased per transaction (invoice)
    cooccurrence_matrix = df_analysis.pivot_table(index='invoiceno', columns='description', values='quantity', aggfunc='sum').fillna(0)
    cooccurrence_matrix = cooccurrence_matrix.applymap(lambda x: 1 if x > 0 else 0)
    
    # Calculate the correlation matrix of product co-occurrence
    correlation_matrix = cooccurrence_matrix.corr()
    
    # Plot the heatmap
    plt.figure(figsize=(14, 10))
    sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Product Co-occurrence Correlation Matrix')
    plt.show()

def segment_customers(df_analysis, num_segments=3):
    """Segment customers based on their total spending."""
    customer_totals = df_analysis.groupby('customerid')['total_purchase'].sum()
    customer_segments = pd.qcut(customer_totals, num_segments, labels=[f'Segment {i+1}' for i in range(num_segments)])
    return customer_segments.value_counts()

def analyze_seasonal_trends(df_analysis):
    """Investigate if certain product categories are more popular during specific times of the year."""
    df_analysis['month'] = pd.to_datetime(df_analysis['invoicedate']).dt.month
    seasonal_trends = df_analysis.groupby(['month', 'description'])['total_purchase'].sum().unstack().fillna(0)
    return seasonal_trends
