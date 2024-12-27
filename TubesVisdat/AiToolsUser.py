import pandas as pd
import streamlit as st
import random

# Predefined set of vibrant colors
VIBRANT_COLORS = [
    "#FF5733", "#FF8D1A", "#FFC300", "#DAF7A6", "#33FF57", "#1AFF8D", 
    "#1AC6FF", "#3375FF", "#8D1AFF", "#FF33C4"
]

def get_random_vibrant_color():
    # Randomly pick a vibrant color
    return random.choice(VIBRANT_COLORS)

def load_data():
    data = pd.read_csv('merged_data.csv')
    return data

def plot_AiToolsUsers():
    data = load_data()
    
    # Filter data for "AI Tools Users"
    market_size_data = data[data['Chart'] == 'AI Tools Users']
    
    # Pick relevant columns including 'Market' and 'Unit'
    filtered_data = market_size_data[['Region', 'Name', 'Market', 'Unit', '2020', '2021', '2022', '2023', '2024']]
    
    # Filter for only "Artificial Intelligence" in 'Market'
    filtered_data = filtered_data[filtered_data['Market'] == 'Artificial Intelligence']
    
    # Reshape data for the chart (pivot data)
    pivot_data = filtered_data.melt(
        id_vars=["Region", "Name"], 
        value_vars=["2020", "2021", "2022", "2023", "2024"], 
        var_name="Year", value_name="Value")
    
    # Convert 'Value' column to numeric, forcing errors to NaN
    pivot_data['Value'] = pd.to_numeric(pivot_data['Value'], errors='coerce')
    
    # Select region from the dropdown (default to "Worldwide")
    region = st.selectbox("Select Region", 
                          filtered_data['Region'].unique(), 
                          index=list(filtered_data['Region']).index("Worldwide")
                          )
    
    region_data = pivot_data[pivot_data['Region'] == region]
    
    # Create cards for each year
    st.write("\n")
    col1, col2, col3, col4, col5 = st.columns(5)
    cards = [col1, col2, col3, col4, col5]
    
    years = region_data['Year'].unique()
    for i, year in enumerate(sorted(years)):
        with cards[i]:
            year_value = region_data[region_data['Year'] == year]['Value'].values[0]
            
            # Get random vibrant colors for border and text
            border_color = get_random_vibrant_color()
            text_color = get_random_vibrant_color()
            
            st.markdown(f"""
                <div style="text-align: center; padding: 10px; background-color: transparent; border: 2px solid {border_color}; border-radius: 10px;">
                    <p style="color: {text_color}; font-size: 32px; font-weight: bold; margin: 0;">{year}</p>
                    <p style="color: {text_color}; font-size: 24px; margin: 0;">{year_value}</p>
                    <p style="color: {text_color}; font-size: 16px; margin: 0;">Million</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Line chart for visualization
    region_data_pivot = region_data.pivot_table(
        index="Year", 
        columns="Name", 
        values="Value", 
        aggfunc="sum"
        )
    st.write("\n")
    st.write("\n")
    st.line_chart(region_data_pivot)