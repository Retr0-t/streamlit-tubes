import pandas as pd
import streamlit as st

def load_data():
    data = pd.read_csv('merged_data.csv')
    return data

def plot_top_6_regions():
    data = load_data()
    # Filter data untuk "Market Size"
    market_size_data = data[data['Chart'] == 'Market Size']
    # Pilih kolom yang relevan, termasuk kolom 'Market' dan 'Unit'
    filtered_data = market_size_data[['Region', 'Name', 'Market', 'Unit', '2024']]
    # Filter hanya "Artificial Intelligence" dari kolom 'Market'
    filtered_data = filtered_data[filtered_data['Market'] == 'Artificial Intelligence']
    # Filter data berdasarkan 'Unit' yaitu "billion USD (US$)"
    filtered_data = filtered_data[filtered_data['Unit'] == 'billion USD (US$)']
    # Reshape data untuk grafik (pivot data)
    pivot_data = filtered_data.pivot_table(
        index='Region', 
        columns='Name', 
        values='2024', 
        aggfunc='sum'
    ).reset_index()
    # Hapus kolom 'Total' jika ada di pivot data
    if 'Total' in pivot_data.columns:
        pivot_data = pivot_data.drop(columns=['Total'])

    # Bersihkan nama kolom dari spasi ekstra
    pivot_data.columns = pivot_data.columns.str.strip()
    # Tambahkan kolom "Total Value" untuk menghitung total nilai tahun 2024 per region
    pivot_data['Total Value'] = pivot_data.iloc[:, 1:].sum(axis=1)
    # Urutkan berdasarkan "Total Value" secara menurun
    pivot_data = pivot_data.sort_values(by='Total Value', ascending=False)
    # Ambil hanya 6 region dengan nilai tertinggi
    top_6_regions = pivot_data.head(6)
    # Hapus kolom "Total Value" dari tabel akhir sebelum visualisasi
    top_6_regions = top_6_regions.drop(columns=['Total Value'])
    # Menghapus baris dengan Region "Worldwide"
    top_6_regions = top_6_regions[top_6_regions['Region'] != 'Worldwide']
    
    st.write("In Billion USD")
    st.bar_chart(
        top_6_regions.set_index('Region'),  # Region sebagai sumbu X
    )
