import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(page_title="Energy Forecast App", layout="centered")

st.title(" Household Energy Analytics & Forecasting")

st.markdown("""
Explore past energy usage patterns and predict your household's energy consumption based on input conditions.
""")

# === Load historical data for analytics ===
data_path = "household_energy.csv"
if os.path.exists(data_path):
    df = pd.read_csv(data_path, parse_dates=["timestamp"])
    df['hour'] = df['timestamp'].dt.hour
    df['weekday'] = df['timestamp'].dt.dayofweek
    avg_energy = df['energy_consumption'].mean()

    # === Show Analytics ===
    st.header(" Analytics Dashboard")

    # Hourly Trend Plot
    st.subheader(" Hourly Energy Trend")
    hourly_avg = df.groupby('hour')['energy_consumption'].mean()
    fig1, ax1 = plt.subplots()
    ax1.plot(hourly_avg.index, hourly_avg.values, marker='o', color='skyblue')
    ax1.set_xlabel("Hour of Day")
    ax1.set_ylabel("Average kWh")
    ax1.set_title("Average Energy Usage by Hour")
    st.pyplot(fig1)

    # Weekday Trend Plot
    st.subheader("Weekday Energy Trend")
    weekday_avg = df.groupby('weekday')['energy_consumption'].mean()
    fig2, ax2 = plt.subplots()
    ax2.bar(weekday_avg.index, weekday_avg.values, color='lightgreen')
    ax2.set_xlabel("Weekday (0 = Mon ... 6 = Sun)")
    ax2.set_ylabel("Average kWh")
    ax2.set_title("Average Energy Usage by Day of Week")
    st.pyplot(fig2)
else:
    df = None
    avg_energy = 3.0  # fallback
    st.info("Analytics not available – dataset 'household_energy.csv' not found.")

# === Prediction Section ===
st.header(" Predict Energy Consumption")

# Load model
model_path = "forecast_model.pkl"
if not os.path.exists(model_path):
    st.error("Model file 'forecast_model.pkl' not found. Please upload or train the model first.")
    st.stop()

model = joblib.load(model_path)

# User Inputs
temperature = st.number_input("Indoor Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0)
outside_temperature = st.number_input("Outside Temperature (°C)", min_value=-10.0, max_value=50.0, value=30.0)
device_usage = st.number_input("🔌 Device Usage (0 = Off, 1 = On)", min_value=0, max_value=1, value=1)
hour = st.number_input("Hour of Day (0–23)", min_value=0, max_value=23, value=12)
weekday = st.number_input("Day of Week (0 = Mon, ..., 6 = Sun)", min_value=0, max_value=6, value=2)

# Predict button
if st.button("Predict Energy Consumption"):
    features = np.array([[temperature, outside_temperature, device_usage, hour, weekday]])
    prediction = model.predict(features)[0]
    st.success(f" Predicted Energy Consumption: *{prediction:.2f} kWh*")

    # Efficiency feedback
    st.subheader("⚙ Efficiency Insight")
    if prediction > 1.25 * avg_energy:
        st.warning("⚠ High predicted usage! Consider reducing appliance use or adjusting temperature settings.")
    elif prediction < 0.75 * avg_energy:
        st.info(" Efficient usage predicted!")
    else:
        st.info(" Usage is within normal expected range.")