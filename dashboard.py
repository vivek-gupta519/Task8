import pandas as pd
import plotly.express as px
import streamlit as st

# Page setup
st.set_page_config(page_title="Simple Sales Dashboard", layout="wide")
st.title("📊 Simple Sales Dashboard")

# Load dataset
df = pd.read_csv("Superstore_Sales.csv")
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Month-Year'] = df['Order Date'].dt.strftime('%b-%Y')

# Sidebar filter
region_filter = st.sidebar.multiselect(
    "Select Region(s)",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Filter data
df_filtered = df[df['Region'].isin(region_filter)]

# Line Chart: Sales over Months
sales_month = df_filtered.groupby('Month-Year')['Sales'].sum().reset_index()
fig_line = px.line(sales_month, x='Month-Year', y='Sales', title="Sales Over Months")
fig_line.update_traces(mode='lines+markers')

# Bar Chart: Sales by Region
sales_region = df_filtered.groupby('Region')['Sales'].sum().reset_index()
fig_bar = px.bar(sales_region, x='Region', y='Sales', title="Sales by Region",
                 color='Sales', text='Sales')
fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')

# Donut Chart: Sales by Category
sales_category = df_filtered.groupby('Category')['Sales'].sum().reset_index()
fig_donut = px.pie(sales_category, values='Sales', names='Category',
                   hole=0.5, title="Sales by Category")

# Layout
col1, col2 = st.columns([2, 1])
col1.plotly_chart(fig_line, use_container_width=True)
col2.plotly_chart(fig_donut, use_container_width=True)

st.plotly_chart(fig_bar, use_container_width=True)

# Insights
st.markdown("### 🔍 Insights")
st.write("""
1. West region often shows the highest total sales.
2. Technology usually dominates category sales.
3. Sales tend to peak in holiday months like November and December.
""")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit & Plotly")
