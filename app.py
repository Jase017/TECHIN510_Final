import streamlit as st
import requests
from datetime import datetime
import time
import base64

# Constants for API
WEATHER_API_KEY = 'bb75a58b0c1df1a9a5cd689e1ea9d145'
WEATHER_BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
IPINFO_API_KEY = '63eb356a3a40a2'
IPINFO_URL = f"https://ipinfo.io?token={IPINFO_API_KEY}"
TIME_API_URL = 'http://worldtimeapi.org/api/timezone/America/Los_Angeles'
FIREBASE_URL = 'https://pawsitude-2bab7-default-rtdb.firebaseio.com/'

def get_location():
    """Fetch the location based on IP address"""
    response = requests.get(IPINFO_URL)
    data = response.json()
    return data['city']

def get_weather(city):
    """Fetch weather data for a specified city"""
    response = requests.get(f"{WEATHER_BASE_URL}q={city}&appid={WEATHER_API_KEY}&units=metric")
    data = response.json()
    return data

def get_time():
    """Fetch current time from WorldTimeAPI"""
    response = requests.get(TIME_API_URL)
    data = response.json()
    datetime_str = data['datetime']
    return datetime_str.split('T')[1].split('.')[0]  # Extract time in HH:MM:SS format

def load_image_to_base64(image_path):
    """Convert image to base64 to use as a background"""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def get_firebase_data(path):
    """Fetch data from Firebase"""
    url = f"{FIREBASE_URL}{path}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    # Convert images to base64
    background_base64 = load_image_to_base64("background.jpg")
    logo_base64 = load_image_to_base64("pawsitive.png")  # Replace with the path to your logo image

    # Use base64 image as a background and add a logo at the top left
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: white;  /* Sets the background color to white */
            background-image: url("data:image/jpeg;base64,{background_base64}");
            background-size: 25%;  /* Reduces the image size to 25% of its original size */
            background-repeat: no-repeat;  /* No tiling */
            background-attachment: fixed;  /* Image does not scroll with the content */
            background-position: bottom center;  /* Position at the bottom center */
            color: black;  /* Sets text color to black */
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; /* Improves font appearance */
        }}
        .logo {{
            position: fixed;
            top: 50px;  /* Adjust this value to move the logo down */
            left: 50px;  /* Adjust this value to move the logo right */
            width: 100px;  /* Adjust the width as needed */
            height: 100px;  /* Adjust the height as needed */
        }}
        h1, h2, h3, h4, h5, h6, p, .stMarkdown {{
            color: black;  /* Sets text color to black for headers and paragraphs */
            text-align: center; /* Aligns text to center */
        }}
        </style>
        <div>
            <img src="data:image/png;base64,{logo_base64}" class="logo">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Title of the app with clock icon
    st.markdown("<h1 style='text-align: center;'><i class='fas fa-desktop'></i> Desktop Assistant</h1>", unsafe_allow_html=True)

    # Layout using columns
    col1, col2 = st.columns(2)

    # Container for time in the first column with clock icon
    with col1:
        st.markdown("<h2 style='text-align: center;'><i class='far fa-clock'></i> Time</h2>", unsafe_allow_html=True)
        time_container = st.empty()

    # Container for weather in the second column with cloud sun icon
    with col2:
        st.markdown("<h2 style='text-align: center;'><i class='fas fa-cloud-sun'></i> Weather</h2>", unsafe_allow_html=True)
        weather_container = st.empty()

    # Firebase data containers
    st.markdown("<h2 style='text-align: center;'>Realtime Data</h2>", unsafe_allow_html=True)
    heartrate_container = st.empty()
    barkingcount_container = st.empty()

    # Continuously update time, weather, and Firebase data
    while True:
        current_time = get_time()
        time_container.markdown(f"**Current Time:** {current_time}", unsafe_allow_html=True)

        try:
            city = get_location()
            weather_data = get_weather(city)
            if 'main' in weather_data:
                temperature = f"{weather_data['main']['temp']} °C"
                description = weather_data['weather'][0]['description']
                weather_info = f"**Weather in {city}**: {temperature}, {description}"
            else:
                weather_info = "Weather data not available"
        except Exception as e:
            weather_info = f"Error fetching weather data: {e}"

        weather_container.markdown(weather_info, unsafe_allow_html=True)

        try:
            heartrate = get_firebase_data('heart_rate_data')
            barkingcount = get_firebase_data('Barking/count')
            heartrate_container.markdown(f"**Heartrate:** {heartrate}", unsafe_allow_html=True)
            barkingcount_container.markdown(f"**Barking Count:** {barkingcount}", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error fetching Firebase data: {e}")

        time.sleep(1)  # Update every 10 seconds

if __name__ == "__main__":
    main()
