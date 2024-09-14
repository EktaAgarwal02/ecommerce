from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt

# Use Agg backend for non-interactive environments
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('BlinkIT-Grocery-Data (1).csv')

# Sales Trends Over Time
def create_sales_trends_analysis():
    df['Year'] = df['Outlet Establishment Year']
    year_sales = df.groupby('Year')['Sales'].sum()
    year_sales.plot(kind='line', figsize=(10, 6))
    plt.title('Sales Trends Over Time (by Year of Outlet Establishment)')
    plt.xlabel('Year')
    plt.ylabel('Total Sales')
    plt.savefig('static/images/sales_trends.png')
    plt.clf()

# Top 10 Selling Items
def create_top_selling_items_analysis():
    top_items = df.groupby('Item Identifier')['Sales'].sum().sort_values(ascending=False).head(10)
    top_items.plot(kind='bar', figsize=(10, 6))
    plt.title('Top 10 Best-Selling Items')
    plt.xlabel('Item Identifier')
    plt.ylabel('Total Sales')
    plt.savefig('static/images/top_selling_items.png')
    plt.clf()

# Item Visibility vs Sales
def create_visibility_vs_sales_analysis():
    plt.scatter(df['Item Visibility'], df['Sales'], alpha=0.5)
    plt.title('Item Visibility vs Sales')
    plt.xlabel('Item Visibility')
    plt.ylabel('Sales')
    plt.savefig('static/images/visibility_vs_sales.png')
    plt.clf()

# Sales by Outlet Location Type
def create_sales_by_location_analysis():
    location_sales = df.groupby('Outlet Location Type')['Sales'].sum()
    location_sales.plot(kind='bar', figsize=(10, 6))
    plt.title('Sales by Outlet Location Type')
    plt.xlabel('Outlet Location Type')
    plt.ylabel('Total Sales')
    plt.savefig('static/images/sales_by_location.png')
    plt.clf()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/sales-trends')
def sales_trends():
    create_sales_trends_analysis()
    return render_template('sales_trends.html')

@app.route('/top-selling-items')
def top_selling_items():
    create_top_selling_items_analysis()
    return render_template('top_selling_items.html')

@app.route('/visibility-vs-sales')
def visibility_vs_sales():
    create_visibility_vs_sales_analysis()
    return render_template('visibility_vs_sales.html')

@app.route('/sales-by-location')
def sales_by_location():
    create_sales_by_location_analysis()
    return render_template('sales_by_location.html')

if __name__ == '__main__':
    app.run(debug=True)
