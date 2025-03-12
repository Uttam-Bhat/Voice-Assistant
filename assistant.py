from flask import Flask, jsonify, send_from_directory
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import requests
import os
import time
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__, static_url_path='', static_folder='')

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyBuUfZ4jQS73dwJ0_DQZIdws_0f3Nw8MaQ"
# OpenWeatherMap API key - you'll need to get one from https://openweathermap.org/api
WEATHER_API_KEY = "1de1446c2da6add1fd9783dd4e8401db"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model with safety settings and rate limiting
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Rate limiting variables
REQUEST_COUNT = 0
LAST_RESET = datetime.now()
MAX_REQUESTS_PER_MINUTE = 60  # Adjust based on your API quota

def check_rate_limit():
    global REQUEST_COUNT, LAST_RESET
    current_time = datetime.now()
    
    # Reset counter if a minute has passed
    if current_time - LAST_RESET > timedelta(minutes=1):
        REQUEST_COUNT = 0
        LAST_RESET = current_time
    
    # Check if we're within limits
    if REQUEST_COUNT >= MAX_REQUESTS_PER_MINUTE:
        return False
    
    REQUEST_COUNT += 1
    return True

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"The current temperature in {city} is {temp}°C with {description}."
        return None
    except:
        return None

def get_ai_response(user_input):
    if not check_rate_limit():
        raise Exception("Rate limit exceeded. Please try again in a minute.")
    
    try:
        safety_settings = {
            "HARASSMENT": "BLOCK_NONE",
            "HATE_SPEECH": "BLOCK_NONE",
            "SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "DANGEROUS_CONTENT": "BLOCK_NONE",
        }
        
        prompt = f"""You are a helpful AI assistant. Please provide a natural and friendly response to: {user_input}
        Keep the response concise and conversational."""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        if "429" in str(e):
            time.sleep(1)  # Wait for a second before retrying
            return "I'm currently experiencing high traffic. Please try again in a moment."
        raise e

@app.route('/')
def home():
    return send_from_directory('', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('', path)

@app.route('/process', methods=['POST'])
def process():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # 🎙️ Convert speech to text
        user_input = recognizer.recognize_google(audio)
        print(f"User said: {user_input}")

        try:
            # Check if it's a weather query
            if any(word in user_input.lower() for word in ['temperature', 'weather', 'how hot', 'how cold']):
                # Extract city name - improved implementation
                words = user_input.lower().split()
                city = None
                for i, word in enumerate(words):
                    if word in ['in', 'at', 'for']:
                        if i + 1 < len(words):
                            city = ' '.join(words[i+1:])
                            break
                
                if city:
                    weather_info = get_weather(city)
                    if weather_info:
                        ai_reply = weather_info
                    else:
                        ai_reply = get_ai_response(user_input)
                else:
                    ai_reply = "I couldn't determine which city you're asking about. Could you please specify the city?"
            else:
                ai_reply = get_ai_response(user_input)

            print(f"AI Response: {ai_reply}")

            # 🔊 Speak out response
            engine = pyttsx3.init()
            engine.say(ai_reply)
            engine.runAndWait()

            # ✅ Return response to frontend
            return jsonify({'user_input': user_input, 'response': ai_reply})

        except Exception as api_error:
            print(f"API Error: {api_error}")
            error_message = str(api_error)
            if 'rate limit' in error_message.lower():
                return jsonify({'error': 'Please wait a moment before trying again.'})
            elif '429' in error_message:
                return jsonify({'error': 'Service is currently busy. Please try again in a moment.'})
            elif 'api_key' in error_message.lower():
                return jsonify({'error': 'Invalid API key. Please check your API key.'})
            elif '404' in error_message:
                return jsonify({'error': 'Service unavailable. Please try again later.'})
            return jsonify({'error': f'Error: {error_message}'})

    except sr.UnknownValueError:
        error_msg = "Sorry, I couldn't understand what you said. Please try again."
        print(error_msg)
        return jsonify({'error': error_msg})
    except sr.RequestError as e:
        error_msg = f"Could not request results; {e}"
        print(error_msg)
        return jsonify({'error': error_msg})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
