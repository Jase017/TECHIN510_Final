# Pawsitive🐾
Welcome to the "Pawsitive" project, where we help you better understand and communicate with your furry friend by visually tracking their feelings and health.
## Problem Statement
Based on our research, Over 50% of people in the United States have dogs and treat them like family, creating a desire to understand their feelings and health, especially when owners are not present. Our strategy aims to visually reflect a dog's emotions and health, helping owners "communicate" with their pets even when they are apart.
## Project Strategy
Our strategy includes measuring dogs' heart rate variability (HRV) and using DSP and ML analysis to turn this data into stress level indicators, along with a sound sensor to detect barking. The hardware design features a clip-on device for the dog's collar and a display device that shows real-time data through an web app on the owner's device.
## Teechnologies used
	1. Streamlit: A powerful and user-friendly Python library for creating interactive web applications, which forms the foundation of the app.
    2. IPinfo API: Utilized to determine the user’s geographical location through their IP address.
	3. OpenWeather API: Used to fetch current weather data based on the user’s location.
	4. WorldTimeAPI: Provides accurate time data, ensuring the app displays the current local time.
	5. Firebase Realtime Database: Integrated to fetch dynamic data such as heart rate, barking count, and activity stage of the user’s dog.
    6.
## How to run
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

streamlit run app.py
```
## Lessons Learned
* How to download real-time data from Firebase and deploy it to web apps like Streamlit
* Front-end development skills and abilities, which also ability to program in HTML.
## Questions
* How can we optimize the data collection process to ensure we gather enough samples from different states without introducing biases or inconsistencies?
* What are the best practices for feature selection in heart rate data analysis, and how can we systematically evaluate and choose the most significant features for our model?