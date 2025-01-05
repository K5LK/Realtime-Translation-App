import streamlit as st
from audio_recorder_streamlit import audio_recorder
from faster_whisper import WhisperModel
import os
from gtts import gTTS
import json
from typing import Optional
from decouple import config
from groq import Groq
from pydantic import BaseModel

# Set page config
st.set_page_config(page_title='Groq Translator', page_icon='🎤')

# Set page title
st.title('Groq Translator')

# Load whisper model
model = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=int(os.cpu_count() / 2))

# Set up the Groq client
client = Groq(api_key=config("GROQ_API_KEY"))

# Model for the translation
class Translation(BaseModel):
    text: str
    comments: Optional[str] = None

# Speech to text
def speech_to_text(audio_chunk):
    segments, info = model.transcribe(audio_chunk, beam_size=5)
    speech_text = " ".join([segment.text for segment in segments])
    return speech_text

# Text to speech
def text_to_speech(translated_text, language):
    file_name = "speech.mp3"
    my_obj = gTTS(text=translated_text, lang=language)
    my_obj.save(file_name)
    return file_name

# Translate text using the Groq API
def groq_translate(query, from_language, to_language):
    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant that translates text from {from_language} to {to_language}."
                           f"You will only reply with the translation text and nothing else in JSON."
                           f"The JSON object must use the schema: {json.dumps(Translation.model_json_schema(), indent=2)}",
            },
            {
                "role": "user",
                "content": f"Translate '{query}' from {from_language} to {to_language}."
            }
        ],
        model="mixtral-8x7b-32768",
        temperature=0.2,
        max_tokens=1024,
        stream=False,
        response_format={"type": "json_object"},
    )
    # Return the translated text
    return Translation.model_validate_json(chat_completion.choices[0].message.content)

# Supported languages
languages = {
   "Portuguese": "pt",
   "Spanish": "es",
   "German": "de",
   "French": "fr",
   "Italian": "it",
   "Dutch": "nl",
   "Russian": "ru",
   "Japanese": "ja",
   "Chinese": "zh",
   "Korean": "ko"
}

# Language selection
option = st.selectbox(
   "Language to translate to:",
   languages,
   index=None,
   placeholder="Select language...",
)

# Record audio
audio_bytes = audio_recorder()
if audio_bytes and option:
    # Display audio player
    st.audio(audio_bytes, format="audio/wav")

    # Save audio to file
    with open('audio.wav', mode='wb') as f:
        f.write(audio_bytes)

    # Speech to text
    st.divider()
    with st.spinner('Transcribing...'):
        text = speech_to_text('audio.wav')
    st.subheader('Transcribed Text')
    st.write(text)

    # Groq translation
    st.divider()
    with st.spinner('Translating...'):
        translation = groq_translate(text, 'en', option)
    st.subheader('Translated Text to ' + option)
    st.write(translation.text)

    # Text to speech
    audio_file = text_to_speech(translation.text, languages[option])
    st.audio(audio_file, format="audio/mp3")
