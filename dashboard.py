import json
import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
import base64

st.set_page_config(layout="wide")

# Menampilkan peta di Streamlit
st.title("Visualisasi Penyebaran Penyakit Mata di Kabupaten Pangandaran")
st.write("Peta ini menunjukkan jumlah kasus penyakit mata di beberapa kecamatan di Kabupaten Pangandaran.")
st.sidebar.title('Plase Select Year')
selected_year = st.sidebar.selectbox('Select Year:', options=[2022, 2023, 2024], index=0)

# Membuka dan memuat file GeoJSON
with open("dissolved.geojson", "r") as file:
    geojson = json.load(file)

# Membaca data dari CSV
data = pd.read_csv("real.csv")
dataset = pd.read_csv("Finaly.csv")

# Membuat peta dengan pusat di Indonesia
map_center = [-7.683333, 108.633333]
m = folium.Map(location=map_center, zoom_start=10)

# Menambahkan GeoJson layer ke peta
folium.GeoJson(geojson).add_to(m)

# Fungsi untuk membuat diagram berdasarkan hasil groupby
def create_chart(kecamatan):
    # Agregasi data berdasarkan Kecamatan dan Block Code
    grouped_data = dataset[dataset['Kecamatan'] == kecamatan].groupby(by=['Kecamatan', 'block_code']).agg({
        "block_code": "count"
    }).rename(columns={"block_code": "count"}).reset_index()

    # Membuat diagram batang menggunakan hasil agregasi
    plt.figure(figsize=(6, 4))  # Meningkatkan ukuran gambar
    plt.bar(grouped_data['block_code'], grouped_data['count'], color='blue')
    plt.title(f"Kecamatan: {kecamatan}")
    plt.xlabel('block_code')
    plt.ylabel('Jumlah Kasus')

    # Menambahkan rotasi pada label sumbu x (block_code) sebesar 90 derajat
    plt.xticks(rotation=90)

    # Menggunakan tight_layout untuk menghindari label yang terpotong
    plt.tight_layout()

    # Simpan diagram ke buffer dalam format PNG
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    # Encode gambar ke base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64

# Menambahkan marker dengan popup yang berisi diagram berdasarkan kecamatan yang diklik
for index, row in data.iterrows():
    icon_color = "green"  # Default color
    
    # Membuat diagram berdasarkan kecamatan yang diklik
    img_base64 = create_chart(row['Kecamatan'])
    
    # Membuat HTML untuk popup yang menampilkan diagram
    html = f"""
    <h4>Kecamatan: {row['Kecamatan']}</h4>
    <img src="data:image/png;base64,{img_base64}" width="300">
    """
    
    iframe = folium.IFrame(html=html, width=350, height=300)
    popup = folium.Popup(iframe, max_width=350)
    
    folium.Marker(
        location=[row["Lat"], row["Long"]],
        popup=popup,
        tooltip=row["Kecamatan"],
        icon=folium.Icon(color=icon_color, icon="info-sign")
    ).add_to(m)

# Render peta dengan streamlit_folium
st_folium(m, width=1600, height=950)
