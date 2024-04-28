import streamlit as st
from dotenv import load_dotenv
from googletrans import Translator
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Import necessary modules
import os
import google.generativeai as genai

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for generating summary
prompt = """As a YouTube video summarizer, your task is to analyze the provided transcript text and generate a concise summary of the entire video. Your summary should highlight the most important points, key insights, and significant details within 250 words. Please produce a well-organized summary based on the following transcript: """

# Function to extract transcript details from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception:
        st.warning("Please provide a valid YouTube video URL.")

# Function to generate summary using Gemini model
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

# Streamlit app
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

# to print thumbnail onto screen
if youtube_link:
    video_link = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_link}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)

        # Text area for translation
        st.subheader("Translation")
        text_input = summary

        # Select target language
        language_names = {
            "en": "English", "hi": "Hindi", "bn": "Bengali", "gu": "Gujarati", "kn": "Kannada",
            "ml": "Malayalam", "mr": "Marathi", "pa": "Punjabi", "ta": "Tamil", "te": "Telugu",
            "as": "Assamese", "or": "Odia", "ur": "Urdu", "ne": "Nepali"
        }
        target_language = st.selectbox("Select target language:", list(language_names.values()))

        # Translate button
        if st.button("Translate"):
            if text_input:
                # Get language code corresponding to selected language
                target_language_code = [code for code, name in language_names.items() if name == target_language][0]
                translated_text = translate_text(text_input, target_language_code)
                st.write("Translated Text:")
                st.write(translated_text)
            else:
                st.warning("Please enter some text to translate.")
