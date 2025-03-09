import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi tampilan Streamlit
st.set_page_config(page_title="Analisis Data Share Bike", layout="wide")

# Load dan gabungkan data tanpa upload
@st.cache_data
def load_data():
    day_data = pd.read_csv("day.csv")
    hour_data = pd.read_csv("hour.csv")
    
    day_data['dteday'] = pd.to_datetime(day_data['dteday'])
    hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
    
    # Gabungkan berdasarkan tanggal
    merged_data = pd.merge(hour_data, day_data, on="dteday", suffixes=("_hour", "_day"))
    
    return merged_data

data = load_data()

# Sidebar - Pilih rentang tanggal
st.sidebar.header("Opsi Analisis")
start_date = st.sidebar.date_input("Tanggal Mulai", data['dteday'].min())
end_date = st.sidebar.date_input("Tanggal Akhir", data['dteday'].max())

# Filter data berdasarkan rentang tanggal
filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]

show_summary = st.sidebar.checkbox("Tampilkan Ringkasan Data")
show_usage_trend = st.sidebar.checkbox("Tampilkan Tren Penggunaan")
show_correlation = st.sidebar.checkbox("Tampilkan Korelasi Musim dan Hari Libur")
show_season_impact = st.sidebar.checkbox("Tampilkan Pengaruh Musim")

st.header("Dashboard Analisis Data Share Bike")
st.write(f"### Data dalam rentang {start_date} hingga {end_date}")
st.write(filtered_data.head())

if show_summary:
    st.subheader("Ringkasan Data")
    st.write(filtered_data.describe())
    st.write("Jumlah Data yang Hilang:")
    st.write(filtered_data.isnull().sum())

if show_usage_trend:
    st.subheader("Tren Penggunaan Sepeda")
    usage_trend = filtered_data.groupby(filtered_data['dteday'].dt.to_period("M")).sum(numeric_only=True)
    plt.figure(figsize=(10,5))
    sns.lineplot(x=usage_trend.index.astype(str), y=usage_trend['cnt_hour'])
    plt.xticks(rotation=45)
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Penggunaan")
    plt.title("Tren Penggunaan Sepeda Bulanan")
    st.pyplot(plt)

if show_correlation:
    st.subheader("Korelasi Musim dan Hari Libur terhadap Penggunaan")
    plt.figure(figsize=(8,5))
    corr_cols = ['season_hour', 'holiday_hour', 'cnt_hour']
    sns.heatmap(filtered_data[corr_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
    st.pyplot(plt)

if show_season_impact:
    st.subheader("Pengaruh Musim terhadap Penggunaan Sepeda")
    season_impact = filtered_data.groupby('season_hour', as_index=False)['cnt_hour'].mean()
    plt.figure(figsize=(8,5))
    sns.barplot(x=season_impact['season_hour'], y=season_impact['cnt_hour'], palette="viridis")
    plt.xlabel("Musim")
    plt.ylabel("Rata-rata Penggunaan")
    plt.title("Pengaruh Musim terhadap Penggunaan Sepeda")
    st.pyplot(plt)
