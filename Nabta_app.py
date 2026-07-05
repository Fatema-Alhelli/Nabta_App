import streamlit as st
import pandas as pd
from datetime import datetime
import plant_manager as pm

st.title("🌱 Nabta App")
st.write("Welcome to Nabta🌱.. Your smart companion to care for your houseplants and track their growth step by step✨.")

with st.sidebar:
    choice = st.selectbox("Select an option:",
        (
            "🌻 Add a new plant to the collection",
            "📋 View all plants",
            "🚨 View plants due for care",
            "🔍 Search plants by name or location",
            "💡 Get Custom Care & Advice (Camera Live) "
        )
    )

if choice == "🌻 Add a new plant to the collection":
    st.subheader("Add New Plant Details")
    name = st.text_input("Plant Name:")
    location = st.text_input("Location (e.g., Balcony, Living Room):")
    date = st.text_input("Date Acquired (YYYY-MM-DD):", value=datetime.today().strftime('%Y-%m-%d'))
    watering = st.number_input("Watering Frequency (Every X days):", min_value=1, value=3)
    sunlight = st.selectbox("Sunlight Requirement:", ["Low", "Medium", "High"])
    
    if st.button("Save Plant"):
        if name and location:
            pm.add_plant(name, location, date, watering, sunlight)
            st.success(f"'{name}' has been added successfully! 🎉")
        else:
            st.error("Please fill in both Plant Name and Location.")

elif choice == "📋 View all plants":
    st.subheader("Your Plant Collection")
    try:
        df = pm.get_all_plants()
        st.dataframe(df)
    except:
        st.info("No plants added yet. Go to 'Add a new plant' first!")

elif choice == "🚨 View plants due for care":
    st.subheader("Plants That Need Care Immediately")
    df_due = pm.get_due_plants()
    if not df_due.empty:
        st.warning("The following plants need your attention:")
        st.dataframe(df_due)
    else:
        st.success("All your plants are healthy and hydrated! 💧")

elif choice == "🔍 Search plants by name or location":
    st.subheader("Search your Garden")
    term = st.text_input("Enter plant name or location to search:")
    if term:
        results = pm.search_plants(term)
        if not results.empty:
            st.write(f"Found {len(results)} matching results:")
            st.dataframe(results)
        else:
            st.error("No matching plants found.")

elif choice == "💡 Get Custom Care & Advice (Camera Live) ":
    st.subheader("Custom Plant Care, Photos & Advice")
    
    name = st.text_input("Enter Plant Name to update/get advice:")
    
    advice_type = st.selectbox("What advice do you need today?", ["Watering & Seasonal Care", "Symptom Diagnosis"])
    
    st.markdown("---")
    st.markdown("### 📸 Document Plant Progress")
    height = st.number_input("Current Height (cm):", min_value=0.0, step=0.1)
    
    picture = st.camera_input("Take a snapshot of your plant 📸")
    
    img_path = "None"
    if picture:
        img_path = f"{name}_care.png"
        with open(img_path, "wb") as f:
            f.write(picture.getbuffer())
        st.success("Photo captured and ready to save!")

    if st.button("Submit & Get Custom Advice"):
        if name:
            date_today = datetime.today().strftime('%Y-%m-%d')
            if pm.log_progress(name, date_today, height, img_path, advice_type):
                st.success("Care progress logged into inventory!")
                
                if advice_type == "Watering & Seasonal Care":
                    season = st.selectbox("Select Current Season:", ["Summer", "Winter"])
                    care_info = pm.get_seasonal_care(name, season)
                    st.info(f"📋 **Schedule Adjustment:** {care_info['Watering_Adjustment']}")
                    st.warning(f"💡 **Pro-Tip:** {care_info['Reminder']}")
                
                elif advice_type == "Symptom Diagnosis":
                    symptom = st.selectbox("Select Observed Symptom:", ["Yellow Leaves", "Brown Tips", "White Spots"])
                    diagnosis = pm.diagnose_problem(symptom)
                    st.error(f"🔍 **Diagnosis Result:** {diagnosis}")
            else:
                st.error("Plant name not found. Please add the plant in option 1 first.")
        else:
            st.error("Please enter the plant name.")


