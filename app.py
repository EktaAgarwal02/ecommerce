from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretmre'

# Load the dataset
file_path = 'BlinkIT-Grocery-Data (1).csv'
df = pd.read_csv(file_path)

# Helper function to generate graphs
def generate_graphs(item_type=None, outlet_type=None):
    # Filter based on the selected item type and outlet type
    filtered_df = df.copy()
    if item_type:
        filtered_df = filtered_df[filtered_df['Item Type'] == item_type]
    if outlet_type:
        filtered_df = filtered_df[filtered_df['Outlet Type'] == outlet_type]

    # Graphs
    fig1 = px.histogram(filtered_df, x='Item Type', y='Sales', title='Sales Distribution by Item Type')
    fig2 = px.bar(filtered_df.groupby('Outlet Type')['Sales'].mean().reset_index(),
                  x='Outlet Type', y='Sales', title='Average Sales by Outlet Type')
    fig3 = px.box(filtered_df, x='Outlet Type', y='Sales', title='Sales Distribution by Outlet Type')
    fig4 = px.pie(filtered_df, names='Item Type', values='Sales', title='Sales Share by Item Type')
    fig5 = px.scatter(filtered_df, x='Sales', y='Discount', color='Item Type',
                      title='Sales vs. Discount by Item Type')
    fig6 = px.line(filtered_df.groupby('Date')['Sales'].sum().reset_index(),
                   x='Date', y='Sales', title='Daily Sales Over Time')
    fig7 = px.bar(filtered_df.groupby('Region')['Sales'].sum().reset_index(),
                  x='Region', y='Sales', title='Total Sales by Region')
    fig8 = px.treemap(filtered_df, path=['Region', 'City'], values='Sales', title='Sales by Region and City')
    fig9 = px.bar(filtered_df.groupby('Outlet Size')['Sales'].sum().reset_index(),
                  x='Outlet Size', y='Sales', title='Sales by Outlet Size')
    fig10 = px.histogram(filtered_df, x='Item Type', y='Discount', title='Discount Distribution by Item Type')
    fig11 = px.scatter(filtered_df, x='Sales', y='Profit', color='Outlet Type', title='Sales vs. Profit by Outlet Type')
    fig12 = px.box(filtered_df, x='Item Type', y='Sales', title='Sales Distribution by Item Type')
    fig13 = px.histogram(filtered_df, x='City', y='Sales', title='Sales Distribution by City')
    fig14 = px.bar(filtered_df.groupby('Item Type')['Sales'].mean().reset_index(),
                   x='Item Type', y='Sales', title='Average Sales by Item Type')
    fig15 = px.pie(filtered_df, names='Outlet Type', values='Sales', title='Sales Share by Outlet Type')

    # Convert the plots to JSON
    graphs = {
        'graph1': json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder),
        'graph2': json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder),
        'graph3': json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder),
        'graph4': json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder),
        'graph5': json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder),
        'graph6': json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder),
        'graph7': json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder),
        'graph8': json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder),
        'graph ind_fig8': json.dumps(fig8, cls=plotly.utils.PlotlyJSONEncoder),
        'graph9': json.dumps(fig9, cls=plotly.utils.PlotlyJSONEncoder),
        'graph10': json.dumps(fig10, cls=plotly.utils.PlotlyJSONEncoder),
        'graph11': json.dumps(fig11, cls=plotly.utils.PlotlyJSONEncoder),
        'graph12': json.dumps(fig12, cls=plotly.utils.PlotlyJSONEncoder),
        'graph13': json.dumps(fig13, cls=plotly.utils.PlotlyJSONEncoder),
        'graph14': json.dumps(fig14, cls=plotly.utils.PlotlyJSONEncoder),
        'graph15': json.dumps(fig15, cls=plotly.utils.PlotlyJSONEncoder),
    }
    return graphs

@app.route('/', methods=['GET', 'POST'])
def index():
    item_type = request.form.get('item_type')
    outlet_type = request.form.get('outlet_type')

    graphs = generate_graphs(item_type, outlet_type)

    # Populate the dropdown options
    item_types = df['Item Type'].unique()
    outlet_types = df['Outlet Type'].unique()

    # Summary content
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_items_sold = df['Sales'].count()
    avg_sales_per_outlet = df.groupby('Outlet Type')['Sales'].mean().reset_index()
    avg_discount = df['Discount'].mean()

    return render_template('dashboard.html', graphs=graphs, item_types=item_types, outlet_types=outlet_types,
                           total_sales=total_sales, total_profit=total_profited_profit = df['Profit'].sum()
, avg_sales_per_outlet=avg_sales_per_outlet, total_items_sold=total_items_sold, avg_discount=avg_discount)

if __name__ == '_main_':
    app.run(debug=True)