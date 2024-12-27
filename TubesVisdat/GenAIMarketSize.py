import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def load_data():
    data = pd.read_csv('merged_data.csv')
    return data

def map_plot_Generative_AI_MarketSize():
    data = load_data()
    
    # Filter data untuk "Market Size"
    market_size_data = data[data['Chart'] == 'Market Size']
    
    # Pilih kolom yang relevan, termasuk kolom 'Market' dan 'Unit'
    filtered_data = market_size_data[['Region', 'Name', 'Market', 'Unit', '2024']]
    
    # Filter hanya "Generative AI" dari kolom 'Market'
    filtered_data = filtered_data[filtered_data['Market'] == 'Generative AI']
    
    # Tambahkan kolom untuk keterangan hover (gabungkan nilai dan unit)
    filtered_data['Unit Info'] = filtered_data.apply(
        lambda row: f"{row['2024']} ({row['Unit']})", axis=1
    )
    
    # Kelompokkan nilai 2024 berdasarkan region dan gabungkan info hover
    grouped_data = filtered_data.groupby('Region').agg({
        '2024': 'sum',
        'Unit Info': lambda x: '<br>'.join(x)  # Gabungkan informasi hover
    }).reset_index()
    
    # Tambahkan peta interaktif menggunakan Plotly
    fig = px.choropleth(
        grouped_data,
        locations='Region',  
        locationmode='country names', 
        color='2024',  
        hover_name='Region',  
        hover_data={'Unit Info': True, '2024': False}, 
        color_continuous_scale='Reds',
        title='Generative AI Market Size by Region (2024)',
    )
    
    # Tambahkan layout untuk menyesuaikan tampilan peta
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )
    
    # Tampilkan peta di Streamlit
    st.plotly_chart(fig, use_container_width=True)

def plot_top_6_genAIMarketSize():
    data = load_data()
    
    # Filter data untuk "Market Size"
    market_size_data = data[data['Chart'] == 'Market Size']
    
    # Pilih kolom yang relevan, termasuk kolom 'Market' dan 'Unit'
    filtered_data = market_size_data[['Region', 'Market', 'Unit', '2020', '2021', '2022', '2023', '2024']]
    
    # Filter hanya "Generative AI" dari kolom 'Market'
    filtered_data = filtered_data[filtered_data['Market'] == 'Generative AI']
    
    # Filter data berdasarkan 'Unit' yaitu "billion USD (US$)"
    filtered_data = filtered_data[filtered_data['Unit'] == 'billion USD (US$)']
    
    # Transformasi data dari wide ke long format
    long_data = filtered_data.melt(
        id_vars=['Region'], 
        value_vars=['2020', '2021', '2022', '2023', '2024'], 
        var_name='Year', 
        value_name='Market Size'
    )
    
    # Pastikan 'Market Size' adalah numerik
    long_data['Market Size'] = pd.to_numeric(long_data['Market Size'], errors='coerce')
    
    # Hapus baris dengan nilai NaN
    long_data = long_data.dropna(subset=['Market Size'])
    
    # Kelompokkan data berdasarkan region dan tahun
    grouped_data = long_data.groupby(['Region', 'Year'])['Market Size'].sum().reset_index()
    
    # Urutkan region berdasarkan total market size
    total_market_size = grouped_data.groupby('Region')['Market Size'].sum().reset_index()
    top_regions = total_market_size.sort_values(by='Market Size', ascending=False).head(6)['Region']
    
    # Filter hanya 6 region dengan nilai tertinggi
    grouped_data = grouped_data[grouped_data['Region'].isin(top_regions)]
    
    # Plot area chart menggunakan Plotly
    fig = go.Figure()
    
    # Tambahkan setiap region sebagai trace dengan warna berbeda
    for region in top_regions:
        region_data = grouped_data[grouped_data['Region'] == region]
        fig.add_trace(go.Scatter(
            x=region_data['Year'],
            y=region_data['Market Size'],
            mode='lines',
            stackgroup='one',  
            name=region
        ))
    
    # Tambahkan layout untuk mempercantik grafik
    fig.update_layout(
        title="Top 6 Generative AI Market Size by Region (2020-2024)",
        xaxis_title="Year",
        yaxis_title="Market Size (Billion USD)",
        legend_title="Regions",
        template="plotly",
    )

    # Tampilkan grafik di Streamlit
    st.plotly_chart(fig, use_container_width=True)



