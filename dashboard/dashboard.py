import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_monthly_df(df):
    monthly_df = df.resample('M', on="dteday").agg({
        'cnt' : 'sum'
    })

    monthly_df.index = monthly_df.index.strftime('%Y-%m')
    monthly_df.reset_index(inplace=True)
    
    return monthly_df

def create_season_df(df):
    return df.groupby("season").cnt.sum().sort_values(ascending=False).reset_index()

day_df = pd.read_csv("dashboard/all_data.csv")

day_df['dteday'] = pd.to_datetime(day_df.dteday)
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)


# komponen filter
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://bikeshare.metro.net/wp-content/uploads/2016/04/cropped-metro-bike-share-favicon.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]


monthly_df = create_monthly_df(main_df)
season_df = create_season_df(main_df)


st.header('Bike Share Dashboard :sparkles:')

st.subheader("Riders per month")
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_df["dteday"],
    monthly_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=10)
fig.autofmt_xdate()
st.pyplot(fig)

st.subheader("Best Season of Riders")
 
fig, ax = plt.subplots(figsize=(10,6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(season_df.sort_values('cnt', ascending=False), y='season', x='cnt', palette=colors)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title("Best Season of Casual", loc="center", fontsize=15)
ax.tick_params(axis ='y', labelsize=12)
 
st.pyplot(fig)
 
st.caption('Copyright (c) Dicoding 2023')