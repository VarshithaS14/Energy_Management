# 🔋 Household Energy Analytics & Forecasting

A Streamlit web app to visualize historical household energy consumption and predict future energy usage based on environmental and device conditions.

## 🚀 Features

- 📊 **Energy Analytics Dashboard**
  - Hourly and weekday energy usage trends
- 🔮 **Energy Consumption Prediction**
  - Predict energy usage using a pre-trained machine learning model
  - Inputs: indoor/outdoor temperature, device usage, hour, and weekday
- ⚙️ **Efficiency Feedback**
  - Insight on whether predicted usage is efficient, normal, or high

## 🗂️ Project Structure

energy_app/
│
├── app.py # Streamlit application
├── household_energy.csv # Historical energy usage data (required)
├── forecast_model.pkl # Trained machine learning model (required)
├── requirements.txt # Python dependencies
└── README.md # Project documentation
