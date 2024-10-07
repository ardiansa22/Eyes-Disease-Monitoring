import json
import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st

st.set_page_config(layout="wide")

st.sidebar.title('Plase Select Year')
selected_year = st.sidebar.selectbox('Select Year:', options=[2022, 2023,2024], index=0)
# Membuka dan memuat file GeoJSON
with open("dissolved.geojson", "r") as file:
    geojson = json.load(file)
# Membaca data dari CSV
data = pd.read_csv("real.csv")
# Membuat peta dengan pusat di Indonesia
map_center = [-7.683333, 108.633333]
m = folium.Map(location=map_center, zoom_start=10)

# Menambahkan GeoJson layer ke peta
folium.GeoJson(geojson).add_to(m)

# Menambahkan marker untuk setiap kecamatan berdasarkan data dari CSV
# Menambahkan marker untuk setiap kecamatan berdasarkan data dari CSV
for index, row in data.iterrows():
    icon_color = "green"  # Default color

    if row["cluster"] == 0:
        icon_color = "green"
    elif row["cluster"] == 0:
        icon_color = "yellow"
    elif row["cluster"] == 1:
        icon_color = "red"

    folium.Marker(
        location=[row["Lat"], row["Long"]],
        popup=f"Kecamatan: {row['Kecamatan']}<br>Kasus: {row['total_pasien']}<br>Claster: {row['cluster']}",
        tooltip=row["Kecamatan"],
        icon=folium.Icon(color=icon_color, icon="info-sign")
    ).add_to(m)


# Menampilkan peta di Streamlit
st.title("Visualisasi Penyebaran Penyakit Mata di Kabupaten Pangandaran")
st.write("Peta ini menunjukkan jumlah kasus penyakit mata di beberapa kecamatan di Kabupaten Pangandaran.")

# Render peta dengan streamlit_folium
st_folium(m, width=1600, height=950)
