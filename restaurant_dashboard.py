import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load Data
file_path = "restaurant_analytics_data_large.csv"  
df = pd.read_csv(file_path)

# Convert date column
df['Order_Time'] = pd.to_datetime(df['Order_Time'], errors='coerce')
df['hour'] = df['Order_Time'].dt.hour  # Extract hour for analysis

# Title of the Dashboard
st.title("📊 Restaurant Analytics Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_weather = st.sidebar.multiselect("Select Weather Conditions", df['Weather_Condition'].unique(), default=df['Weather_Condition'].unique())
selected_platform = st.sidebar.multiselect("Select Delivery Platforms", df['Delivery_Platform_Used'].dropna().unique(), default=df['Delivery_Platform_Used'].dropna().unique())

# Apply Filters to the Whole Dataset
filtered_df = df[
    (df['Weather_Condition'].isin(selected_weather)) & 
    (df['Delivery_Platform_Used'].fillna("").isin(selected_platform))
]

### 📅 Orders Per Day
st.subheader("📅 Orders Per Day")
daily_orders = filtered_df.groupby('Order_Time')['Total_Orders_Per_Hour'].sum().reset_index()
daily_orders['Average_Orders'] = daily_orders['Total_Orders_Per_Hour'].rolling(7, min_periods=1).mean()
fig1 = px.line(daily_orders, x='Order_Time', y='Average_Orders', 
               title="📊 Orders Per Day",
               labels={"Order_Time": "Date", "Average_Orders": "Total Orders"},
               color_discrete_sequence=['#FF5733'])
fig1.update_xaxes(tickformat="%d-%b", tickmode="auto", nticks=10, showgrid=True)
st.plotly_chart(fig1)

### 🚀 Revenue by Delivery Platform
st.subheader("🚀 Revenue Contribution by Delivery Platforms")
platform_revenue = filtered_df.groupby('Delivery_Platform_Used')['Total_Revenue'].sum().reset_index()
fig2 = px.bar(platform_revenue, x='Delivery_Platform_Used', y='Total_Revenue', 
              title="📊 Revenue by Delivery Platform", 
              color='Delivery_Platform_Used', 
              color_discrete_sequence=['#FF5733', '#33C3FF', '#66CC33'])
st.plotly_chart(fig2)

### 🌦️ Impact of Weather on Orders
st.subheader("🌦️ Weather Impact on Orders")
weather_orders = filtered_df.groupby('Weather_Condition')['Total_Orders_Per_Hour'].sum().reset_index()
fig3 = px.bar(weather_orders, x='Weather_Condition', y='Total_Orders_Per_Hour', 
              title="Orders by Weather Condition", 
              color='Total_Orders_Per_Hour', 
              color_continuous_scale='oranges')
st.plotly_chart(fig3)

### ⏰ Peak Order Hours
st.subheader("⏰ Peak Order Hours")
hourly_orders = filtered_df.groupby('hour')['Total_Orders_Per_Hour'].sum().reset_index()
fig4 = px.bar(hourly_orders, x='hour', y='Total_Orders_Per_Hour', 
              title="Total Orders by Hour of the Day", 
              color='Total_Orders_Per_Hour', 
              color_continuous_scale='viridis')
st.plotly_chart(fig4)

### 🍔 Top 5 Best-Selling Menu Items
st.subheader("🍔 Top 5 Best-Selling Menu Items")
menu_performance = filtered_df.groupby('Menu_Item')['Total_Orders_Per_Hour'].sum().reset_index().sort_values(by='Total_Orders_Per_Hour', ascending=False).head(5)
fig5 = px.bar(menu_performance, x='Total_Orders_Per_Hour', y='Menu_Item', 
              title="Top 5 Best-Selling Menu Items", 
              orientation='h', 
              color='Total_Orders_Per_Hour', 
              color_continuous_scale='reds')
st.plotly_chart(fig5)

### 🚚 Average Delivery Time by Platform
st.subheader("🚚 Average Delivery Time by Platform")
delivery_time = filtered_df.groupby('Delivery_Platform_Used')['Delivery_Time_Minutes'].mean().reset_index()
fig6 = px.bar(delivery_time, x='Delivery_Platform_Used', y='Delivery_Time_Minutes', 
              title="Average Delivery Time by Platform", 
              color='Delivery_Time_Minutes', 
              color_continuous_scale='greens')
st.plotly_chart(fig6)

### 👨‍🍳 Orders vs. Staff On Duty
st.subheader("👨‍🍳 Orders vs. Staff On Duty Throughout the Day")
hourly_data = filtered_df.groupby('hour').agg({'Total_Orders_Per_Hour': 'sum', 'Staff_On_Duty': 'mean'}).reset_index()
fig7 = go.Figure()

# Plot total orders on primary y-axis (Blue)
fig7.add_trace(go.Scatter(
    x=hourly_data['hour'], y=hourly_data['Total_Orders_Per_Hour'],
    mode='lines+markers', name="Total Orders",
    marker=dict(color='blue')
))

# Plot staff on duty on secondary y-axis (Orange)
fig7.add_trace(go.Scatter(
    x=hourly_data['hour'], y=hourly_data['Staff_On_Duty'],
    mode='lines+markers', name="Staff On Duty",
    marker=dict(color='orange'),
    yaxis="y2"
))

# Format the layout
fig7.update_layout(
    title="📊 Orders vs. Staff On Duty Throughout the Day",
    xaxis=dict(title="Hour of the Day", tickmode="linear", dtick=1),
    yaxis=dict(title="Total Orders", side="left"),
    yaxis2=dict(title="Staff On Duty", overlaying="y", side="right", showgrid=False),
    legend=dict(title="Metrics", x=0.8, y=1.2)
)
st.plotly_chart(fig7)
