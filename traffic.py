import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title='Traffic Accident Analysis', layout='wide')

# Title
st.title('Traffic Accident Analysis Dashboard')

# File uploader
uploaded_file = st.file_uploader("Upload Traffic Accident Data (CSV)", type=["csv"])

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    st.write("### Raw Data Preview")
    st.dataframe(df.head())
    
    # Check necessary columns
    required_columns = ['Latitude', 'Longitude', 'Severity', 'Date', 'Time']
    if not all(col in df.columns for col in required_columns):
        st.error("The dataset must contain the following columns: Latitude, Longitude, Severity, Date, and Time.")
    else:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        
        # Sidebar filters
        st.sidebar.header("Filter Data")
        selected_severity = st.sidebar.selectbox("Select Accident Severity", df['Severity'].unique())
        filtered_df = df[df['Severity'] == selected_severity]
        
        st.write(f"### Filtered Data by Severity {selected_severity}")
        st.dataframe(filtered_df.head())
        
        # Visualization - Trend Over Time
        st.write("### Accident Trends Over Time")
        accidents_per_year = df.groupby('Year').size()
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=accidents_per_year.index, y=accidents_per_year.values, marker='o')
        plt.xlabel("Year")
        plt.ylabel("Number of Accidents")
        plt.title("Accidents Over Time")
        st.pyplot(plt)
        
        # Map Visualization
        st.write("### Accident Hotspot Map")
        accident_map = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=10)
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=5,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.6
            ).add_to(accident_map)
        folium_static(accident_map)
        
        # Severity Distribution
        st.write("### Severity Distribution")
        plt.figure(figsize=(8, 5))
        sns.countplot(x='Severity', data=df, palette='coolwarm')
        plt.xlabel("Severity Level")
        plt.ylabel("Number of Accidents")
        plt.title("Distribution of Accident Severity")
        st.pyplot(plt)
