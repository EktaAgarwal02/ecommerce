from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
# Use Agg backend for non-interactive environments
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('BlinkIT-Grocery-Data (1).csv')

# Sales Trends Over Time
def create_sales_trends_analysis():
    fig8=go.Figure()
    # Create a new column for 'Year'
    df['Year'] = df['Outlet Establishment Year']

    # Group by 'Year' and sum the 'Sales'
    year_sales = df.groupby('Year')['Sales'].sum().reset_index()

    # Create the animated line plot
    fig8 = px.line(year_sales, 
                x='Year', 
                y='Sales', 
                title='Sales Trends Over Time (by Year of Outlet Establishment)',
                labels={'Sales': 'Total Sales', 'Year': 'Year'},
                width=800, height=500)

    # Add a frame for animation
    fig8.update_traces(mode='lines+markers')  # Add markers to the line
    fig8.update_layout(transition_duration=500)  # Duration of the animation transition
    graph8_html = pio.to_html(fig8,full_html=False)
    return graph8_html

# Top 10 Selling Items
def create_top_selling_items():
    top_items = df.groupby('Item Type')['Sales'].sum().sort_values(ascending=False).head(10)
    top_items.plot(kind='barh', figsize=(15, 8))
    plt.title('Top 10 Best-Selling Items by Item Type')
    plt.xlabel('Total Sales')
    plt.ylabel('Item Type')
    plt.savefig('static/images/top_selling_items.png')
    plt.clf()
# Visualization of Item Types
def create_item_type_analysis():
    fig2 = go.Figure()
    # Create a count plot for 'Item Type' using Plotly
    item_counts = df['Item Type'].value_counts().reset_index()
    item_counts.columns = ['Item Type', 'Count']  # Rename columns for clarity

    # Create a bar chart with multi-color
    fig2 = px.bar(
        item_counts, 
        x='Item Type', 
        y='Count', 
        title='Distribution of Item Types',
        color='Item Type',  # Use Item Type for color differentiation
        color_discrete_sequence=px.colors.qualitative.Plotly  # Use a qualitative color palette
    )

    # Update layout for aesthetics
    fig2.update_layout(
        xaxis_title='Item Type',
        yaxis_title='Count',
        title_x=0.5,  # Center the title
        template='plotly_white',  # Use a white theme
        xaxis_tickangle=-45,  # Rotate x-axis labels for better visibility
        paper_bgcolor='white',  # White paper background
        plot_bgcolor='white',  # White plot background
        height=600,  # Increase height for better visibility
        width=900,   # Increase width for better visibility
        font=dict(size=14),  # Increase font size
        xaxis=dict(showgrid=True, gridcolor='lightgrey'),  # Add gridlines
        yaxis=dict(showgrid=True, gridcolor='lightgrey')   # Add gridlines
    )

    # Adding labels on top of the bars
    fig2.update_traces(
        texttemplate='%{y}',  # Show the count value
        textposition='outside',  # Position text above the bars
        marker=dict(line=dict(color='black', width=1))  # Add black border around bars
    )

    # Customize hover information
    fig2.update_traces(hoverinfo='x+y', hovertemplate='Item Type: %{x}<br>Count: %{y}<extra></extra>')
    graph2_html = pio.to_html(fig2,full_html=False)
    return graph2_html

# Item Visibility vs Sales
def create_visibility_vs_sales_analysis():
    fig9=go.Figure()
# Create the scatter plot using plotly.express with multi-color points
    fig9 = px.scatter(df, 
        x='Item Visibility', 
        y='Sales', 
        title='Item Visibility vs Sales',
        labels={'Item Visibility': 'Item Visibility', 'Sales': 'Sales'},
        color='Item Type',  # Use a categorical variable for color
        opacity=0.5,  # Set opacity for points
        width=800,height=500)
    graph9_html = pio.to_html(fig9,full_html=False)
    return graph9_html
# Sales by Outlet Location Type
def create_sales_by_location_analysis():
    data = {
    'Outlet Type': ['Supermarket ', 'Grocery Store', 'Other'],
    'Percentage': [65, 13, 22]  # Provided percentages
}
# Create a DataFrame
    df = pd.DataFrame(data)
    fig6=go.Figure()
    # Create a bar chart
    fig6 = px.bar(
        df,
        x='Outlet Type',
        y='Percentage',
        title='Outlet Type Distribution',
        labels={'Percentage': 'Percentage (%)', 'Outlet Type': 'Outlet Type'},
        color='Outlet Type',  # Color differentiation by Outlet Type
        color_discrete_map={
            'Supermarket ': 'blue',
            'Grocery Store': 'orange',
            'Other': 'green'
        },
        width=700,
        height=500
    )
# Customize layout for better aesthetics
    fig6.update_layout(
        title_x=0.5,  # Center the title
        template='plotly_white',
        paper_bgcolor='white',
        font=dict(size=14),
    )
    graph6_html = pio.to_html(fig6,full_html=False)
    return graph6_html
    
# # Fat Content Analysis
# def fat_content_analysis():
#         df[' ItemFat Content'] = df[' ItemFat Content'].replace({
#         'LF': 'Low Fat',
#         'low fat': 'Low Fat',
#         'reg': 'Regular'
#         })

#         plt.figure(figsize=(10, 6))
#         sns.histplot(df[' ItemFat Content'], bins=30, kde=True)
#         plt.title('Distribution of Fat Content')
#         plt.xlabel('Fat Content')
#         plt.ylabel('Frequency')
#         plt.savefig('static/images/fat_content_analyse.png')
#         plt.clf()


#outlet size analysis
def create_outlet_size_analysis():
    outlet_size_distribution = df['Outlet Siz0e'].value_counts()
    # Custom color palette for the pie chart
    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
    fig4=go.Figure()
    # Create a more attractive pie chart for outlet size distribution
    fig4 = px.pie(values=outlet_size_distribution, 
                names=outlet_size_distribution.index, 
                title='Distribution of Outlet Sizes',
                hole=0.3, 
                color_discrete_sequence=colors)

    # Update the layout for aesthetics
    fig4.update_traces(
        textinfo='percent+label', 
        hoverinfo='label+percent+value',  # Show label, percentage, and value on hover
        pull=[0.05]*len(outlet_size_distribution),  # Pull slices out slightly for emphasis
        marker=dict(line=dict(color='white', width=2))  # Add white borders around slices
    )

    # Customizing the overall layout
    fig4.update_layout(
        title_font_size=22,  # Larger title font
        title_x=0.5,  # Center the title
        annotations=[dict(text='Outlet Sizes', x=0.5, y=0.5, font_size=18, showarrow=False)],  # Add text in the donut hole
        showlegend=True,  # Show legend
        legend=dict(
            font_size=12,  # Increase legend font size
            bgcolor='rgba(0,0,0,0)',  # Transparent legend background
        ),
        template='plotly_white'  # Use a  theme for a vibrant look
    )
    graph4_html = pio.to_html(fig4,full_html=False)
    return graph4_html


# Visualization of Outlet Locations
def create_outlet_location_analysis():
        # Create a count plot for 'Outlet Location Type' using Plotly
    location_counts = df['Outlet Location Type'].value_counts().reset_index()
    location_counts.columns = ['Outlet Location Type', 'Count']  # Rename columns for clarity
    fig3=go.Figure()
    # Create a bar chart with elegant colors
    fig3 = px.bar(
        location_counts,
        x='Outlet Location Type',
        y='Count',
        title='Distribution of Outlet Locations',
        color='Outlet Location Type',  # Use Outlet Location Type for color differentiation
        color_discrete_sequence=px.colors.sequential.Plasma  # Use an elegant sequential color palette
    )

    # Update layout for aesthetics
    fig3.update_layout(
        xaxis_title='Outlet Location Type',
        yaxis_title='Count',
        title_x=0.5,  # Center the title
        template='plotly_white',  # Use a white theme
        xaxis_tickangle=-45,  # Rotate x-axis labels for better visibility
        paper_bgcolor='white',  # White paper background
        plot_bgcolor='white',  # White plot background
        height=600,  # Increase height for better visibility
        width=900,   # Increase width for better visibility
        font=dict(size=14),  # Increase font size
        xaxis=dict(showgrid=True, gridcolor='lightgrey'),  # Add gridlines
        yaxis=dict(showgrid=True, gridcolor='lightgrey')   # Add gridlines
    )

    # Adding labels on top of the bars
    fig3.update_traces(
        texttemplate='%{y}',  # Show the count value
        textposition='outside',  # Position text above the bars
        marker=dict(line=dict(color='black', width=1))  # Add black border around bars
    )
    # Customize hover information
    fig3.update_traces(hoverinfo='x+y', hovertemplate='Location Type: %{x}<br>Count: %{y}<extra></extra>')
    graph3_html = pio.to_html(fig3,full_html=False)
    return graph3_html
    
# Visualization of Outlet Establishment Year
def create_Outlet_Establishment_Year():
    
    # Create a count plot for 'Outlet Establishment Year' using Plotly
    # First, we create a DataFrame with counts and sort it
    year_counts = df['Outlet Establishment Year'].value_counts().reset_index()
    year_counts.columns = ['Year', 'Count']  # Rename columns for clarity
    year_counts.sort_values('Year', inplace=True)  # Sort by Year
    fig5=go.Figure()
    # Create a histogram with multi-colors
    fig5 = px.bar(
        year_counts, 
        x='Year', 
        y='Count', 
        title='Outlet Establishment Year Distribution',
        color='Year',  # Use Year for color differentiation
        color_discrete_sequence=px.colors.qualitative.Plotly  # Use a qualitative color palette
    )

    # Update the layout for aesthetics
    fig5.update_layout(
        xaxis_title='Year',
        yaxis_title='Count',
        title_x=0.5,  # Center the title
        template='plotly_white',  # Use a white theme
        bargap=0.3,  # Add space between bars
        plot_bgcolor='white',  # White plot background
        paper_bgcolor='white',  # White paper background
    )

    # Adding labels on top of the bars
    fig5.update_traces(
        texttemplate='%{y}',  # Show the count value
        textposition='outside',  # Position text above the bars
        marker=dict(line=dict(color='black', width=1))  # Add black border around bars
    )

    # Customize hover information
    fig5.update_traces(hoverinfo='x+y', hovertemplate='Year: %{x}<br>Count: %{y}<extra></extra>')
    graph5_html = pio.to_html(fig5,full_html=False)
    return graph5_html

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/sales-trends')
def sales_trends():
    # create_sales_trends_analysis()
    graph8=create_sales_trends_analysis()
    return render_template('sales_trends.html',graph8=graph8)

@app.route('/top-selling-items')
def top_selling_items():
    create_top_selling_items()
    return render_template('top_selling_items.html')

@app.route('/item-type-analysis')
def item_type_analysis():
    # create_item_type_analysis()
    return render_template('item_type_analysis.html')

@app.route('/top-selling-items')
def outlet_item_analysis():
    #fat_content_analysis()
    return render_template('top_selling_items.html')


@app.route('/sales-by-location')
def sales_by_location():
    # create_sales_by_location_analysis()
    graph6 = create_sales_by_location_analysis()
    return render_template('sales_by_location.html',graph6=graph6)

@app.route('/outlet-item-analysis')
def Outlet_Size():
    # create_outlet_size_analysis()
    graph3=create_outlet_location_analysis()
    graph4=create_outlet_size_analysis()
    graph5=create_Outlet_Establishment_Year()
    return render_template('outlet_item_analysis.html',graph3=graph3,graph4=graph4,graph5=graph5)
@app.route('/visibility-vs-sales')
def create_visibility_vs_sales_analysis():
    graph9=create_visibility_vs_sales_analysis()
    return render_template('visibility_vs_sales.html',graph9=graph9)

if __name__ == '__main__':
    app.run(debug=True)
