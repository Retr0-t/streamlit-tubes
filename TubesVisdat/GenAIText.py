import pandas as pd
import streamlit as st
import plotly.express as px

def load_data():
    data = pd.read_csv('merged_data.csv')
    return data

def plot_GenAIText():
    data = load_data()
    
    # Filter data untuk "Text generation AI tools" dan "Image generation AI tools"
    market_size_text = data[data['Chart'] == 'Users - Text generation AI tools']
    market_size_image = data[data['Chart'] == 'Users - Image generation AI tools']
    
    # Pilih kolom yang relevan
    filtered_text = market_size_text[['Region', 'Name', 'Market', 'Unit', '2022']]
    filtered_image = market_size_image[['Region', 'Name', 'Market', 'Unit', '2022']]
    
    # Filter hanya untuk "Generative AI" di kolom 'Market'
    filtered_text = filtered_text[filtered_text['Market'] == 'Generative AI']
    filtered_image = filtered_image[filtered_image['Market'] == 'Generative AI']
    
    # Konversi kolom '2022' ke numerik
    filtered_text['2022'] = pd.to_numeric(filtered_text['2022'], errors='coerce')
    filtered_image['2022'] = pd.to_numeric(filtered_image['2022'], errors='coerce')
    
    # Pilih region dari dropdown
    region = st.selectbox(
        "Select Region",
        filtered_text['Region'].unique(),
        index=0  # Default ke region pertama
    )
    
    # Filter data berdasarkan region yang dipilih
    region_text = filtered_text[filtered_text['Region'] == region]
    region_image = filtered_image[filtered_image['Region'] == region]
    
    # Jika data kosong, tampilkan pesan
    if region_text.empty:
        st.write("No data available for Text Generation AI tools in the selected region.")
    else:
        # Tampilkan grafik Pie untuk Text Generation
        st.subheader(f"Text Generation AI Tool Users in {region} (2022)")
        fig_text = px.pie(
            region_text,
            values='2022',
            names='Name',
            title=f"Text Generation AI Tool Users in {region} (2022)",
            hole=0.4  # Gaya donut chart
        )
        fig_text.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_text, use_container_width=True)
    
    if region_image.empty:
        st.write("No data available for Image Generation AI tools in the selected region.")
    else:
        # Tampilkan grafik Pie untuk Image Generation
        st.subheader(f"Image Generation AI Tool Users in {region} (2022)")
        fig_image = px.pie(
            region_image,
            values='2022',
            names='Name',
            title=f"Image Generation AI Tool Users in {region} (2022)",
            hole=0.4  # Gaya donut chart
        )
        fig_image.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_image, use_container_width=True)
