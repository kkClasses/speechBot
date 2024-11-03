# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%  install mini anaconda, open conda prompt follow the steps
# conda create -n kkenv python=3.9
# conda activate kkenv # go inside the environment
# pip google.generativeai
# pip install SpeechRecognition
# pip install streamlit
# pip install  pyttsx3

# !pip install pyngrok

# Create a Streamlit app
#%%writefile llm_bot.py
import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

# Set up the Gemini Flash model
GEMINI_API_KEY = "AIzaSyDveGX6_V5VDKUREQtGrh2Lwih06RgBcuI"
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Set up speech recognition
recognizer = sr.Recognizer()
# Set up text-to-speech
engine = pyttsx3.init()

def listen_to_speech():
    """Capture speech and return recognized text."""
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            st.write(f"Recognized speech: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            st.write("Sorry, there was a request error with the API.")
            return None

def generate_llm_response(prompt):
    """Send the prompt to the Gemini model and get the response."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.write(f"Error in generating response: {e}")
        return None

def speak_text(text):
    """Convert text to speech and speak it out."""
    engine.say(text)
    engine.runAndWait()

# Streamlit UI
st.title("Speech-to-Speech LLM Bot")

if st.button("Start Listening"):
    st.write("Please speak now...")
    input_text = listen_to_speech()
    if input_text:
        st.write("Processing your input...")
        response = generate_llm_response(input_text)

        if response:
            st.write("LLM Response: " + response)
            st.write("Speaking the response...")
            speak_text(response)

st.write("Click the button above to interact with the bot.")


