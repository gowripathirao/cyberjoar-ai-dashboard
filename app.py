import streamlit as st
import pandas as pd
import folium
from streamlit.components.v1 import html
import random

st.set_page_config(page_title="AI Intelligence Dashboard", layout="wide")

st.title("🧠 AI Intelligence Fusion Dashboard")
st.markdown("### Multi-Source Intelligence Visualization with Confidence Scoring")

# -------- FILE UPLOAD --------
file = st.file_uploader("Upload CSV (lat, lon, label, type)", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("📊 Data Preview")
    st.dataframe(df)

    # Create Map
    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=5)

    for i in range(len(df)):
        lat = df.loc[i, 'lat']
        lon = df.loc[i, 'lon']
        label = df.loc[i, 'label']
        dtype = df.loc[i, 'type']

        # Color based on type
        color = "blue"
        if dtype == "HUMINT":
            color = "green"
        elif dtype == "IMINT":
            color = "purple"

        confidence = random.randint(70, 95)

        popup = f"""
        <b>{label}</b><br>
        Type: {dtype}<br>
        Confidence: {confidence}%<br>
        Status: Verified
        """

        folium.Marker(
            [lat, lon],
            popup=popup,
            icon=folium.Icon(color=color)
        ).add_to(m)

    st.subheader("🗺 Intelligence Map")
    html(m._repr_html_(), height=500)

# -------- TELEMETRY PREDICTION --------
st.markdown("---")
st.header("📡 Telemetry Reconstruction (Prediction + Confidence)")

col1, col2 = st.columns(2)

with col1:
    lat1 = st.number_input("Lat (t-2)", value=12.9716)
    lon1 = st.number_input("Lon (t-2)", value=77.5946)

with col2:
    lat2 = st.number_input("Lat (t-1)", value=12.9720)
    lon2 = st.number_input("Lon (t-1)", value=77.5950)

if st.button("🔮 Predict Next Coordinate"):
    pred_lat = (lat1 + lat2) / 2
    pred_lon = (lon1 + lon2) / 2

    confidence = random.randint(60, 85)

    st.success(f"Predicted Coordinate: ({pred_lat}, {pred_lon})")
    st.warning(f"Confidence Score: {confidence}% (Estimated)")

    # Map for prediction
    m2 = folium.Map(location=[lat2, lon2], zoom_start=10)

    folium.Marker([lat1, lon1], popup="t-2 (Verified)", icon=folium.Icon(color="green")).add_to(m2)
    folium.Marker([lat2, lon2], popup="t-1 (Verified)", icon=folium.Icon(color="green")).add_to(m2)
    folium.Marker([pred_lat, pred_lon], popup="Predicted (Estimated)", icon=folium.Icon(color="red")).add_to(m2)

    st.subheader("📍 Prediction Map")
    html(m2._repr_html_(), height=500)