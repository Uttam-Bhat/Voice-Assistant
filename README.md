About
A simple AI voice assistant using Flask, Gemini API, and Speech Recognition. It listens to your voice, responds with AI, and can give weather updates.

Libraries to Install 
 You can install all the libraries through your System prompt
 Command:- pip install Flask SpeechRecognition pyttsx3 google-generativeai requests 

API Keys
You can create yuor api keys through these particular website
  Gemini API Key from Google AI Studio
  OpenWeatherMap API Key from https://openweathermap.org/api
  Add them inside assistant.py like this:
    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  
    WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  

Run this Command in your terminal of any code editor
  python assistant.py
Then Open any browser and paste the URL:-  http://127.0.0.1:5000
