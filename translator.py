import streamlit as st
from deep_translator import GoogleTranslator
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for generating summary
prompt = """As a YouTube video summarizer, your task is to analyze the provided transcript text and generate a concise summary of the entire video. Your summary should highlight the most important points, key insights, and significant details within 300-500 words depending on the timelimit of youtube video. Please produce a well-organized summary based on the following transcript: ,at end provide a summary of entire text with bulleted points and emojis which can be understood by people easily also provide a code snippets for the code related videos if neccesarry and highlight its importance """


# Function to extract transcript details from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript

    except Exception:
        st.warning("Please provide a valid YouTube video URL.")
        return None

# Function to generate summary using Gemini model
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text + " ")
    return response.text

def translate_text(text, target_language):
    translator = GoogleTranslator(source='auto', target=target_language)
    translated_text = translator.translate(text)
    return translated_text

# Streamlit app
st.title("YouTube Transcript to Detailed Notes Converter")

# Session state management
if 'transcript_text' not in st.session_state:
    st.session_state['transcript_text'] = ""
if 'summary' not in st.session_state:
    st.session_state['summary'] = ""
if 'translated_text' not in st.session_state:
    st.session_state['translated_text'] = ""

# Input fields
youtube_link = st.text_input("Enter YouTube Video Link:")

# Display thumbnail
if youtube_link:
    video_link = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_link}/0.jpg", use_column_width=True)

# Generate detailed notes
if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.session_state['transcript_text'] = transcript_text
        st.session_state['summary'] = summary
with st.container():
    if st.session_state['summary']:
        st.markdown("## Detailed Notes:")
        st.markdown(
        f"""
        <div style="font-family: 'Arial', sans-serif; font-size: 20px; color: #fff;">
            {st.session_state['summary']}
        </div>
        """,
        unsafe_allow_html=True
    )
        
    
        with st.expander("Translate"):
            language_names = {
                "en": "English", "hi": "Hindi", "bn": "Bengali", "gu": "Gujarati", "kn": "Kannada",
                "ml": "Malayalam", "mr": "Marathi", "pa": "Punjabi", "ta": "Tamil", "te": "Telugu",
                "as": "Assamese", "or": "Odia", "ur": "Urdu", "ne": "Nepali","es":"Spanish","zh": "Chinese","fr": "French","de": "German",
                "ja": "Japanese","ru": "Russian","ar": "Arabic","pt": "Portuguese",
                "it": "Italian","ko": "Korean","tr": "Turkish","vi": "Vietnamese","fa": "Persian","th": "Thai"
            }
            target_language = st.selectbox("Select target language:", list(language_names.values()))

            if st.button("Translate Summary"):
                target_language_code = list(language_names.keys())[list(language_names.values()).index(target_language)]
                translated_text = translate_text(st.session_state['summary'], target_language_code)
                st.session_state['translated_text'] = translated_text

            st.text_area("Translated Text", value=st.session_state['translated_text'], height=500)

