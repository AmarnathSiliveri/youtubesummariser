import streamlit as st
from deep_translator import GoogleTranslator
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
import google.generativeai as genai
import base64
from streamlit_option_menu import option_menu


# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#streamlit app
st.set_page_config(page_title="YOUTUBE VIDEO NOTES GENERATOR", page_icon='📜')  # page title
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1.0">', unsafe_allow_html=True)
#image is converted into base64 format as streamlit doest allow you to use static images from locals.
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()

img = get_img_as_base64("E:/pythonmlprojects/youtube_summariser/spring.jpg")

page_bg = f"""
<style>
[data-testid='stAppViewContainer'] {{
    background-image: url("data:image/jpg;base64,{img}");
    background-size: cover;
    background-repeat: no-repeat;
}}
[data-testid="stHeader"] {{
    background-color: rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg,unsafe_allow_html=True)




# Prompt for generating summary
prompt = """As a YouTube video summarizer, your task is to analyze the provided transcript text and generate a concise summary of the entire video. Your summary should highlight the most important points, key insights, and significant details within 300-500 words depending on the timelimit of youtube video. Please produce a well-organized summary based on the following transcript: ,at end provide a summary of entire text with bulleted points and emojis which can be understood by people easily also provide a code snippets for the code related videos if neccesarry and highlight its importance """


app = option_menu(
                menu_title='UTUBE TO NOTES ',
                options=['INTRO', 'YT NOTES', 'CREDITS'],
                icons=['house',"list-task" ,'person'],
                
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
                styles={
                    "container": {"padding": "2!important","background-color":'#434350'},
        "icon": {"color": "white", "font-size": "20px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#FDDE55"},
        "nav-link-selected": {"background-color": "#40A578"},
        } 
        )
if app =="INTRO":
    st.markdown("""# <span style='color:#FFFFFF'>Welcome to My Streamlit App *YOUTUBE VIDEO NOTES GENERATOR*</span>""", unsafe_allow_html=True)

    st.markdown("""### <span style='color:#FDDE55'> Based on Gemini-PRO LLM API FROM GOOGLE</span>""", unsafe_allow_html=True)
    
    st.markdown("""## <span style='color:#FFF5EE'>Introduction</span>""", unsafe_allow_html=True)

    st.markdown(""" > ##### <span style='color:#FDDE55'>This is YOUTUBE VIDEO NOTES GENERATOR converts youtube video into a notes generator also included with translation capabilities </span>""", unsafe_allow_html=True)

    st.markdown("""## <span style='color:#FFF5EE'>What is YOUTUBE VIDEO NOTES GENERATOR ? </span>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; font-size: 18px;'>
        An ATS is like your hiring assistant 🤵‍♂️, but in digital form! 
                <br>
        📝 It's software designed to manage the entire recruitment process for employers.
                <br>
        🖥️ From collecting and storing resumes to tracking candidate progress, it's your go-to tool for streamlining hiring tasks.
                <br>
        🚀 With features like resume parsing and keyword search, it helps sift through heaps of applications efficiently. 
                <br>
        💼 Plus, it keeps everything organized and accessible, making the hiring journey smoother for everyone involved. 🌟
    </div>
""", unsafe_allow_html=True)
    st.header(" ")
    st.success("Navigate to ATS_SCORE tab FOR insights")

if app == "YT NOTES":


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
    st.title("YouTube video  to Detailed Notes ")
    st.markdown("### <span style='color:#FDDE55'>Given a Youtube Video on clicking *Get Detailed Notes* summary/notes is generated</span>",unsafe_allow_html=True)
    st.warning("hey people ",icon="👋")
    st.warning("after note generation",icon="📝")
    st.warning("Click Translate to translate the summary  into a language of your comfort by clicking dropdown menu ",icon="⬇️")
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
            <div style="font-family: 'Arial', 'Roborto Mono',monospace; font-size: 22px; color: #ffff;">
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

if app == 'CREDITS':
    
    st.balloons()
    st.title("CRAFTED BY :")
    st.subheader("AMARNATH SILIVERI")

# Define your styles
    st.markdown("""
<style>
  .social-icons {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
  }

  .social-icon {
    text-align: center;
  }
</style>
""", unsafe_allow_html=True)

# Create a container for social icons
    st.markdown("""
<div class="social-icons">
  <div class="social-icon">
    <a href="https://www.github.com/SilverStark18" target="_blank" rel="noreferrer">
      <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/github.svg" width="32" height="32" alt="GitHub" />
    </a>
    <p>GitHub</p>
  </div>

  <div class="social-icon">
    <a href="http://www.instagram.com/itz..amar." target="_blank" rel="noreferrer">
      <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/instagram.svg" width="32" height="32" alt="Instagram" />
    </a>
    <p>Instagram</p>
  </div>

  <div class="social-icon">
    <a href="http://www.linkedin.com/in/amarnath-siliveri18" target="_blank" rel="noreferrer">
      <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/linkedin.svg" width="32" height="32" alt="LinkedIn" />
    </a>
    <p>LinkedIn</p>
  </div>

  <div class="social-icon">
    <a href="https://medium.com/@amartalks25603" target="_blank" rel="noreferrer">
      <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/medium.svg" width="32" height="32" alt="Medium" />
    </a>
    <p>Medium</p>
  </div>

  <div class="social-icon">
    <a href="https://www.x.com/Amarsiliveri" target="_blank" rel="noreferrer">
      <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/twitter.svg" width="32" height="32" alt="Twitter" />
    </a>
    <p>Twitter</p>
  </div>

  <div class="social-icon">
    <a href="https://www.threads.net/@itz..amar." target="_blank" rel="noreferrer">
      <img src="https://raw.githubusercontent.com/danielcranney/readme-generator/main/public/icons/socials/threads.svg" width="32" height="32" alt="Threads" />
    </a>
    <p>Threads</p>
  </div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.success(" Stay in the loop and level up your knowledge with every follow! ")
    st.success("Do you see icons , click to follow  on SOCIAL")


