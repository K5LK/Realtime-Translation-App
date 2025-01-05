# Real-Time Language Translation App Using Groq & Whisper

This app translates speech in real-time using **Groq** for fast translation and **Whisper** for accurate speech-to-text. It also converts translated text back into speech using **gTTS**.

---

## Features

- **Speech-to-Text**: Convert spoken audio into text using Whisper.
- **Real-Time Translation**: Translate text into multiple languages using Groq.
- **Text-to-Speech**: Convert translated text into speech using gTTS.
- **User-Friendly Interface**: Built with Streamlit for easy use.

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/K5LK/Realtime-Translation-App.git
   cd Realtime-Translation-App
   
## Install Dependencies

```bash
pip install -r requirements.txt
```

## Set Up Environment Variables

Add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```
## Running the App

Start the Streamlit App:

```bash
streamlit run app.py

