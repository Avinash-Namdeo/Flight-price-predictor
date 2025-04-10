import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("Flight Price Predictor")

st.markdown("Fill out the flight details below to predict the ticket price.")
st.markdown("""Time Range
            
            Early_Morning : 4:00 AM to 8:00 AM  
            
            Morning: 8:00 Am to 12:00 PM
            
            Afternoon: 12:00 PM to 4: 00 PM
            
            Evening: 4:00 PM to 8:00 PM
            
            Night: 8:00 PM to 12:00 AM
            
            Late_Night: 12:00 AM to 4:00 AM
            """)

airline = st.selectbox("Airline", [
    "Indigo", "Air India", "SpiceJet", "Vistara", "GO FIRST", "AirAsia"
])

source_city = st.selectbox("Source City", [
    "Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai", "Hyderabad"
])

destination_city = st.selectbox("Destination City", [
    "Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai", "Hyderabad"
])

departure_time = st.selectbox("Departure Time", [
    "Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"
])
arrival_time = st.selectbox("Arrival Time", [
    "Early_Morning", "Morning", "Afternoon", "Evening", "Night", "Late_Night"
])

travel_class = st.selectbox("Class", ["Economy", "Business"])

days_left = st.number_input("Days Left Until Departure", min_value=1, max_value=60)



# --- Prediction ---
if st.button("Predict Price"):
    if source_city == destination_city:
        st.error("❌ Source and destination cities must be different.")
    else:
        input_data = pd.DataFrame([{
            "airline": airline,
            "source_city": source_city,
            "departure_time": departure_time,
            "arrival_time":arrival_time,
            "destination_city": destination_city,
            "class": travel_class,
            "days_left": days_left
        }])

        try:
            log_prediction = model.predict(input_data)
            price = np.expm1(log_prediction)[0]
            st.success(f"✈️ Predicted Flight Price: ₹{price:,.0f}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
