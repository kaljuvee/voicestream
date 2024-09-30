import streamlit as st
import requests
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
ELEVENLABS_VOICE_ID = "Xb7hH8MSUJpSbSDYk0k2"
ELEVENLABS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"

def text_to_speech(text):
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    response = requests.post(ELEVENLABS_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

st.title("Finespresso Voice Stream!")

default_text = "In a thrilling move, the company announces a buyback of up to 1,334,087 shares at DKK 3.28 from September 24-27, 2024! They now hold 881,938 shares—1.88% of the total capital. The program wraps up, building excitement for investors! Stay tuned!"
text_input = st.text_area("Enter the text you want to convert to speech:", default_text)

if st.button("Generate Speech"):
    audio_content = text_to_speech(text_input)
    
    if audio_content:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(audio_content)
            tmp_file_path = tmp_file.name
        
        st.audio(tmp_file_path, format="audio/mp3")
        
        with open(tmp_file_path, "rb") as file:
            btn = st.download_button(
                label="Download audio",
                data=file,
                file_name="elevenlabs_audio.mp3",
                mime="audio/mp3"
            )
        
        os.unlink(tmp_file_path)
