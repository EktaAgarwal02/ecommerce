from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load and preprocess the dataset
df = pd.read_csv('BlinkIT-Grocery-Data (1).csv')

# Sample preprocessing (replace with relevant column names in your dataset)
# For example, let's assume the dataset has the following columns:
# 'date', 'category', 'product', 'region', 'city', 'quantity_sold', 'sales'

df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M')

# Helper function to convert Plotly figures to JSON for use in templates
def plot_to_json(fig):
    return pio.to_json(fig)

# Home Route (Landing Page)
@app.route('/')
def index():
    # Example metrics (replace with appropriate calculations based on your dataset)
    total_sales = df['sales'].sum()
    total_orders = len(df)
    avg_order_value = df['sales'].mean()

    return render_template('index.html', total_sales=total_sales, total_orders=total_orders, avg_order_value=avg_order_value)

# Sales Overview Page
@app.route('/sales_overview')
def sales_overview():
    # Total Sales Over Time
    sales_over_time = df.groupby('month')['sales'].sum().reset_index()
    fig_sales_line = px.line(sales_over_time, x='month', y='sales', title='Total Sales Over Time')
    sales_line_data = plot_to_json(fig_sales_line)

    # Monthly Sales Distribution
    sales_by_month = df.groupby(df['date'].dt.month)['sales'].sum().reset_index()
    fig_sales_bar = px.bar(sales_by_month, x='date', y='sales', title='Monthly Sales Distribution')
    sales_bar_data = plot_to_json(fig_sales_bar)

    return render_template('sales_overview.html', sales_line_data=sales_line_data, sales_bar_data=sales_bar_data)

# Category Performance Page
@app.route('/category_performance')
def category_performance():
    # Category-wise Sales
    category_sales = df.groupby('category')['sales'].sum().reset_index()
    fig_category_pie = px.pie(category_sales, values='sales', names='category', title='Category-wise Sales')
    category_pie_data = plot_to_json(fig_category_pie)

    # Category Sales Over Time
    category_sales_time = df.groupby(['month', 'category'])['sales'].sum().reset_index()
    fig_category_bar = px.bar(category_sales_time, x='month', y='sales', color='category', title='Category Sales Over Time')
    category_bar_data = plot_to_json(fig_category_bar)

    return render_template('category_performance.html', category_pie_data=category_pie_data, category_bar_data=category_bar_data)

# Top Products Analysis Page
@app.route('/top_products')
def top_products():
    # Top 10 Products by Sales
    top_products_sales = df.groupby('product')['sales'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_top_products_sales = px.bar(top_products_sales, x='product', y='sales', title='Top 10 Products by Sales')
    top_products_sales_data = plot_to_json(fig_top_products_sales)

    # Top 10 Products by Quantity Sold
    top_products_quantity = df.groupby('product')['quantity_sold'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_top_products_quantity = px.bar(top_products_quantity, x='product', y='quantity_sold', title='Top 10 Products by Quantity Sold', orientation='h')
    top_products_quantity_data = plot_to_json(fig_top_products_quantity)

    return render_template('top_products.html', top_products_sales_data=top_products_sales_data, top_products_quantity_data=top_products_quantity_data)

# Regional Sales Insights Page
@app.route('/regional_sales')
def regional_sales():
    # Sales by Region
    regional_sales = df.groupby('region')['sales'].sum().reset_index()
    fig_regional_sales = px.scatter_geo(regional_sales, locations='region', locationmode='country names', size='sales', title='Sales by Region')
    regional_sales_data = plot_to_json(fig_regional_sales)

    # Sales by City
    city_sales = df.groupby('city')['sales'].sum().reset_index()
    fig_city_sales = px.density_heatmap(city_sales, x='city', y='sales', title='Sales by City')
    city_sales_data = plot_to_json(fig_city_sales)

    return render_template('regional_sales.html', regional_sales_data=regional_sales_data, city_sales_data=city_sales_data)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
