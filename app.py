from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
# Visualization of Item Types
def create_item_type_analysis():
    plt.figure(figsize=(12, 8))
    sns.countplot(data=df, x='Item Type', order=df['Item Type'].value_counts().index)
    plt.title('Distribution of Item Types')
    plt.xlabel('Item Type')
    plt.ylabel('Count')
    plt.xticks(rotation=90)
    plt.savefig('static/images/item_type.png')
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

def fat_content_analysis():
    plt.figure(figsize=(10, 6))
    sns.histplot(df[' ItemFat Content'], bins=30, kde=True)
    plt.title('Distribution of Fat Content')
    plt.xlabel('Fat Content')
    plt.ylabel('Frequency')
    plt.savefig('static/images/fat_content_analysis.png')
    plt.clf()

# Plot pie chart for outlet sizes
def outlet_size_distribution():
    plt.figure(figsize=(8, 8))
    plt.pie(outlet_size_distribution, labels=outlet_size_distribution.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Outlet Sizes')
    plt.savefig('static/images/outlet_size_distribution')
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
@app.route('/top-selling-items')
def item_type_analysis():
    create_item_type_analysis()
    return render_template('top_selling_items.html')

@app.route('/visibility-vs-sales')
def visibility_vs_sales():
    create_visibility_vs_sales_analysis()
    return render_template('visibility_vs_sales.html')

@app.route('/sales-by-location')
def sales_by_location():
    create_sales_by_location_analysis()
    return render_template('sales_by_location.html')

@app.route('/top-selling-items')
def outlet_item_analysis():
    fat_content_analysis()
    return render_template('top_selling_items.html')
@app.route('/outlet-item-analysis')
def outlet_size_distribution():
    outlet_size_distribution()
    return render_template('outlet-item-analysis.html')

if __name__ == '__main__':
    app.run(debug=True)
