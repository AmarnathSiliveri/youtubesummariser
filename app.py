import streamlit as st
from deep_translator import GoogleTranslator
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
import google.generativeai as genai
from streamlit_markmap import markmap

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize session state variables
if 'transcript_text' not in st.session_state:
    st.session_state['transcript_text'] = None
if 'summary' not in st.session_state:
    st.session_state['summary'] = None
if 'translated_text' not in st.session_state:
    st.session_state['translated_text'] = None
if 'mindmaptext' not in st.session_state:
    st.session_state['mindmaptext'] = None
if 'translated_text_mindmap' not in st.session_state:
    st.session_state['translated_text_mindmap'] = None

# Prompts for the AI model
prompt1 = """As a YouTube video summarizer, your task is to analyze the provided transcript text and generate a detailed and well-organized summary of the entire video. Your summary should:
1. Highlight the most important points, key insights, and significant details.
2. Be concise yet comprehensive, ranging between 300-500 words, adjusted for the video's length.
3. Include a final section with a summary in bullet points accompanied by emojis for easy understanding.
4. For code-related videos, include relevant code snippets and explain their significance.

Please produce the summary based on the following transcript:"""

promptM = """
Generate a detailed markdown code for the provided summary with the following elements:
A title suitable for the summary given below and a clear main topic and logically connected subtopics. Make sure every main topic has subtopics and every subtopic has appropriate content. Also, provide Hyperlinks for additional information on topics needing explanation. Use emojis to increase the readability of the code when executed.
Here is the provided summary:
"""

# Function to extract transcript details from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]
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

def generate_gemini_content_mindmap(summary, promptM):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(promptM + summary + " ")
    return response.text

# Function to translate text
def translate_text(text, target_language):
    translator = GoogleTranslator(source='auto', target=target_language)
    translated_text = translator.translate(text)
    return translated_text

# Streamlit app
st.title("YouTube Transcript to Detailed Notes Converter")
tab1, tab2, tab3 = st.tabs(["Summary Generation", "Mindmap Generation", "Try"])

with tab1:
    # Input fields
    youtube_link = st.text_input("Enter YouTube Video Link:")

    # Display thumbnail
    if youtube_link:
        video_id = youtube_link.split("v=")[1].split("&")[0]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    # Generate detailed notes
    if st.button("Get Detailed Notes"):
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt1)
            st.session_state['transcript_text'] = transcript_text
            st.session_state['summary'] = summary

    # Display the summary with custom font
    if st.session_state['summary']:
        st.markdown("## Detailed Notes:")
        st.markdown(
            f"""
            <div style="font-family: 'Arial', sans-serif; font-size: 16px; color: #ooo;">
                {st.session_state['summary']}
            </div>
            """,
            unsafe_allow_html=True
        )
        with st.expander("Translate"):
            language_names = {
                "en": "English", "hi": "Hindi", "bn": "Bengali", "gu": "Gujarati", "kn": "Kannada",
                "ml": "Malayalam", "mr": "Marathi", "pa": "Punjabi", "ta": "Tamil", "te": "Telugu",
                "as": "Assamese", "or": "Odia", "ur": "Urdu", "ne": "Nepali", "es": "Spanish", "fr": "French",
                "de": "German", "it": "Italian", "pt": "Portuguese", "ru": "Russian", "zh": "Chinese", 
                "ja": "Japanese", "ko": "Korean", "ar": "Arabic", "tr": "Turkish", "vi": "Vietnamese",
                "th": "Thai", "ms": "Malay", "id": "Indonesian", "fa": "Persian"
            }
            target_language = st.selectbox("Select target language:", list(language_names.values()))

            if st.button("Translate Summary"):
                target_language_code = list(language_names.keys())[list(language_names.values()).index(target_language)]
                translated_text = translate_text(st.session_state['summary'], target_language_code)
                st.session_state['translated_text'] = translated_text

            st.text_area("Translated Text", value=st.session_state['translated_text'], height=600)

with tab2:
    # Generate and display mind map
    if st.button("Generate Mind Map"):
        if st.session_state['summary']:
            mindmap_summary = generate_gemini_content_mindmap(st.session_state['summary'], promptM)
            st.session_state['mindmaptext'] = mindmap_summary
            data = f'''+{mindmap_summary}+'''
            st.sucess
 

    with st.container():
            language_names = {
            "en": "English 🇬🇧","te": "Telugu 🇮🇳", "hi": "Hindi 🇮🇳", "bn": "Bengali 🇧🇩", "gu": "Gujarati 🇮🇳", "kn": "Kannada 🇮🇳",
            "ml": "Malayalam 🇮🇳", "mr": "Marathi 🇮🇳", "pa": "Punjabi 🇮🇳", "ta": "Tamil 🇮🇳", 
            "as": "Assamese 🇮🇳", "or": "Odia 🇮🇳", "ur": "Urdu 🇵🇰", "ne": "Nepali 🇳🇵", "es": "Spanish 🇪🇸", "fr": "French 🇫🇷",
            "de": "German 🇩🇪", "it": "Italian 🇮🇹", "pt": "Portuguese 🇵🇹", "ru": "Russian 🇷🇺", "zh": "Chinese 🇨🇳", 
            "ja": "Japanese 🇯🇵", "ko": "Korean 🇰🇷", "ar": "Arabic 🇸🇦", "tr": "Turkish 🇹🇷", "vi": "Vietnamese 🇻🇳",
            "th": "Thai 🇹🇭", "ms": "Malay 🇲🇾", "id": "Indonesian 🇮🇩", "fa": "Persian 🇮🇷"
        }
            
            target_language = st.selectbox("Select language:", list(language_names.values()))

            if st.button("Translate Mindmap"):
                target_language_code = list(language_names.keys())[list(language_names.values()).index(target_language)]
                translated_mindmap = translate_text(st.session_state['mindmaptext'], target_language_code)
                st.session_state['translated_text_mindmap'] = translated_mindmap

                tdata = st.session_state['translated_text_mindmap']
                markmap(tdata, height=600)
