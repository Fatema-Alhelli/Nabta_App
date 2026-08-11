import pandas as pd
from datetime import datetime
import streamlit as st
import requests
import os

def add_plant(name, location, date, watering, sunlight):
    try:
        inventory = pd.read_csv('plant_inventory.csv')
    except FileNotFoundError:
        inventory = pd.DataFrame(columns=[
            "Plant_Name", "Location", "Date_Acquired", 
            "Watering_Freq", "Sunlight", "Last_Watered",
            "Height", "Image_Path", "Symptoms"
        ])
    
    new_plant = {
        "Plant_Name": name, "Location": location, "Date_Acquired": date, 
        "Watering_Freq": watering, "Sunlight": sunlight, "Last_Watered": date,
        "Height": 0.0, "Image_Path": "None", "Symptoms": "None"
    }
    inventory.loc[len(inventory)] = new_plant
    inventory.to_csv('plant_inventory.csv', index=False)

def plant_care(plant_name):
    inventory = pd.read_csv('plant_inventory.csv')
    return inventory[inventory['Plant_Name'] == plant_name]

def get_all_plants():
    return pd.read_csv('plant_inventory.csv')

def get_due_plants():
    inventory = pd.read_csv('plant_inventory.csv')    
    inventory['Watering_Freq'] = pd.to_numeric(inventory['Watering_Freq'])
    return inventory[inventory['Watering_Freq'] <= 3]

def search_plants(term):
    inventory = pd.read_csv('plant_inventory.csv')
    return inventory[
        inventory['Plant_Name'].str.contains(term, case=False, na=False) | 
        inventory['Location'].str.contains(term, case=False, na=False)
    ]

def log_progress(name, date, height, image_path, symptoms):
    inventory = pd.read_csv('plant_inventory.csv')
    
    if name in inventory['Plant_Name'].values:
        idx = inventory[inventory['Plant_Name'] == name].index[0]
        
        inventory.loc[idx, 'Height'] = height
        inventory.loc[idx, 'Image_Path'] = image_path
        inventory.loc[idx, 'Symptoms'] = symptoms
        inventory.loc[idx, 'Last_Watered'] = date
        
        inventory.to_csv('plant_inventory.csv', index=False)
        return True
    return False

def get_seasonal_care(plant_type, season):
    seasonal_rules = {
        "Summer": {
            "Watering_Adjustment": "Increase watering (Every 2 days due to heat)",
            "Reminder": "Move plant to shade away from intense afternoon sun."
        },
        "Winter": {
            "Watering_Adjustment": "Reduce watering (Every 7-10 days, plant is dormant)",
            "Reminder": "Keep plant away from cold window drafts."
        }
    }
    return seasonal_rules.get(season, {"Watering_Adjustment": "Normal Schedule", "Reminder": "Follow standard care."})

def diagnose_problem(symptom):
    diagnosis_rules = {
        "Yellow Leaves": "Overwatering (Soil is drowning, reduce water frequency)",
        "Brown Tips": "Low Humidity (Air is too dry, mist the leaves)",
        "White Spots": "Fungal Infection (Isolate the plant and apply fungicide)"
    }
    return diagnosis_rules.get(symptom, "Unknown Symptom (Check soil moisture and pests)")

def Quotes_about_plants():

    url = "https://instagram-scraper-ai1.p.rapidapi.com/media/comments/"

    querystring = {"media_id":"3410747375005229467"}

    headers = {
	"x-rapidapi-key": st.secrets['api_key'],
	"x-rapidapi-host": "instagram-scraper-ai1.p.rapidapi.com",
	"Content-Type": "application/json"
     }

     response = requests.get(url, headers = headers, params = querystring)

def get_llm_response(prompt):

	load_dotenv('OPEN_ROUTER_KEY_DAY.env')
	openai_api_key = os.getenv('OPEN_ROUTER_KEY_DAY')

client = OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key = OPEN_ROUTER_KEY_DAY
    )

completion = client.chat.completions.create(
        model = "cohere/north-mini-code:free",
        messages = [
            {
                "role": "system",
                "content": "you are a funny assistant, Tell jokes in plant",
            },
            {"role": "user", "content": prompt},
        ],
        temperature = 0.0,
    )
    response = completion.choices[0].message.content
    return response