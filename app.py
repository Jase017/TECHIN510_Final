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
    # Convert logo image to base64
    logo_base64 = load_image_to_base64("pawsitive.png")  # Replace with the path to your logo image
    gif_base64 = load_image_to_base64("giphy.gif")  # Replace with the path to your GIF image

    # Add a logo at the top left
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #FAF3E0;  /* Sets the background color to off-white */
            color: black;  /* Sets text color to black */
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; /* Improves font appearance */
        }}
        .logo {{
            position: fixed;
            top: 50px;  /* Adjust this value to move the logo down */
            left: 50px;  /* Adjust this value to move the logo right */
            width: 200px;  /* Adjust the width as needed */
            height: 200px;  /* Adjust the height as needed */
        }}
        h1 {{
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: black; /* Sets text color to black */
        }}
        h2 {{
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: black; /* Sets text color to black */
        }}
        p {{
            text-align: center;
            font-size: 20px;
            color: black; /* Sets text color to black */
        }}
        .data-container {{
            white-space: pre-wrap;  /* Allows content to wrap */
            color: black; /* Sets text color to black */
        }}
        </style>
        <div>
            <img src="data:image/png;base64,{logo_base64}" class="logo">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Layout using columns
    col1, col2, col3 = st.columns(3)

    # Container for time in the first column with clock icon
    with col1:
        st.markdown("<h2><i class='far fa-clock'></i> Time</h2>", unsafe_allow_html=True)
        time_container = st.empty()

    # Container for weather in the second column with cloud sun icon
    with col2:
        st.markdown("<h2><i class='fas fa-cloud-sun'></i> Weather</h2>", unsafe_allow_html=True)
        weather_container = st.empty()

    # Firebase data containers in the third column
    with col3:
        st.markdown("<h2>Realtime Data</h2>", unsafe_allow_html=True)
        heartrate_container = st.empty()
        barkingcount_container = st.empty()

    # Additional row for "Your dog is active!" and GIF
    st.markdown("<h2>Your Dog is Active!</h2>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <img src="data:image/gif;base64,{gif_base64}" width="400" height="400" />
        </div>
        """,
        unsafe_allow_html=True
    )

    # Continuously update time, weather, and Firebase data
    while True:
        current_time = get_time()
        time_container.markdown(f"<p class='data-container'><b>Current Time:</b>\n{current_time}</p>", unsafe_allow_html=True)

        try:
            city = get_location()
            weather_data = get_weather(city)
            if 'main' in weather_data:
                temperature = f"{weather_data['main']['temp']} °C"
                description = weather_data['weather'][0]['description']
                weather_info = f"<p class='data-container'><b>Weather in {city}:</b>\n{temperature},\n{description}</p>"
            else:
                weather_info = "<p class='data-container'>Weather data not available</p>"
        except Exception as e:
            weather_info = f"<p class='data-container'>Error fetching weather data: {e}</p>"

        weather_container.markdown(weather_info, unsafe_allow_html=True)

        try:
            heartrate = get_firebase_data('heart_rate_data/heart_rate')
            timestamp = get_firebase_data('heart_rate_data/timestamp')
            barkingcount = get_firebase_data('Barking/count')
            heartrate_container.markdown(f"<p class='data-container'><b>Heartrate:</b>\n{heartrate}\n{timestamp}</p>", unsafe_allow_html=True)
            barkingcount_container.markdown(f"<p class='data-container'><b>Barking Count:</b>\n{barkingcount}</p>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error fetching Firebase data: {e}")

        time.sleep(10)  # Update every 10 seconds

if __name__ == "__main__":
    main()
