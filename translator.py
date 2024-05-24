import streamlit as st
from deep_translator import GoogleTranslator
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
import google.generativeai as genai
from streamlit_option_menu import option_menu
from streamlit_markmap import markmap

# Load environment variables
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#streamlit app
st.set_page_config(page_title="YOUTUBE VIDEO NOTES GENERATOR", page_icon='📜')  # page title
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1.0">', unsafe_allow_html=True)
#image is converted into base64 format as streamlit doest allow you to use static images from locals.
# Define CSS styling
page_bg = """
<style>
[data-testid='stAppViewContainer'] {
    background-image: url("https://images.unsplash.com/photo-1567201864585-6baec9110dac?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8d2hpdGV8ZW58MHx8MHx8fDA%3D");
    background-size: cover;
}
[data-testid="stHeader"] {
background-color: rgba(0,0,0,0);
}
</style>
"""

st.markdown(page_bg,unsafe_allow_html=True)

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
A title suitable for the summary given below and a clear main topic and logically connected subtopics. Make sure every main topic has subtopics and every subtopic has appropriate content make bullet points. Also, provide Hyperlinks for additional information on topics needing explanation. Use emojis to increase the readability of the code when executed
Here is the provided summary:
"""
app = option_menu(
                menu_title='YOUTUBE video  TO NOTES ',
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
    st.markdown("""# <span style='color:#FFFFFF'>Welcome to My Streamlit App *YOUTUBE VIDEO  TO NOTES GENERATOR*</span>""", unsafe_allow_html=True)

    st.markdown("""### <span style='color:#FDDE55'> Based on Gemini-PRO LLM API FROM GOOGLE</span>""", unsafe_allow_html=True)
    
    st.markdown("""## <span style='color:#FFF5EE'>Introduction</span>""", unsafe_allow_html=True)

    st.markdown(""" > ##### <span style='color:#FDDE55'>This is YOUTUBE VIDEO NOTES GENERATOR converts youtube video into a notes generator also included with translation capabilities </span>""", unsafe_allow_html=True)

    st.markdown("""## <span style='color:#FFF5EE'>What is YOUTUBE VIDEO NOTES GENERATOR ? </span>""", unsafe_allow_html=True)

    st.markdown("""
        <div style='font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; font-size: 20px;'>
            Our app acts as your digital assistant 🤖 for extracting and summarizing YouTube video content:
                    <br>
            📹 Provide a YouTube video link, and our app fetches the transcript automatically.
                    <br>
            📝 The transcript is analyzed using the Gemini-PRO LLM API to generate comprehensive notes.
                    <br>
            🚀 With features like detailed summaries and key insights, it transforms video content into easily digestible information.
                    <br>
            🌐 Supports multiple languages, making it accessible for a global audience.
                    <br>
            💡 Ideal for students, professionals, and anyone looking to convert video content into readable notes quickly.
        </div>
    """, unsafe_allow_html=True)

    st.header(" ")
    st.success("Navigate to   *YT NOTES*   tab for insights")

if app == "YT NOTES":

    tab1,tab2=st.tabs(["Summary "," Mindmap "])
    with tab1:
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
        # Function to generate markdown code for markmap function to generate mindmap  using gemini model
        def generate_gemini_content_mindmap(summary, promptM):
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(promptM + summary + " ")
            return response.text

        # Function to generate translations
        def translate_text(text, target_language):
            translator = GoogleTranslator(source='auto', target=target_language)
            translated_text = translator.translate(text)
            return translated_text
        
        # Streamlit app
        st.title("YouTube video  to Detailed Notes ")
        st.markdown("### <span style='color:#FDDE55'>Convert  **Youtube Video**  to **TEXT** on clicking *Get Detailed Notes* summary/notes is generated</span>",unsafe_allow_html=True)
        with st.expander(" 👆 Click it"):
            st.warning("hey people ",icon="👋")
            st.warning("after note generation",icon="📝")
            st.warning("Click Translate to translate the summary  into a language of your comfort by clicking dropdown menu ",icon="⬇️")


        # Input fields
        youtube_link = st.text_input("Enter YouTube Video Link:")

        # Display thumbnail
        if youtube_link:
            video_link = youtube_link.split("=")[1]
            st.image(f"http://img.youtube.com/vi/{video_link}/0.jpg", use_column_width=True)

        # Generate detailed notes
        if st.button(" 🕹️ Generate Notes"):
            transcript_text = extract_transcript_details(youtube_link)
            if transcript_text:
                summary = generate_gemini_content(transcript_text, prompt1)
                st.session_state['transcript_text'] = transcript_text
                st.session_state['summary'] = summary
        with st.container():
            if st.session_state['summary']:
                st.markdown("## Detailed Notes:")
                st.markdown(
                f"""
                <div style="font-family: 'Arial', 'Roborto Mono',monospace; font-size: 22px; color: #0000;">
                    {st.session_state['summary']}
                </div>
                """,
                unsafe_allow_html=True
            )
                
            
                with st.expander("Translate"):
                    language_names = {
                        "en": "English", "te": "Telugu","hi": "Hindi", "bn": "Bengali", "gu": "Gujarati", "kn": "Kannada",
                        "ml": "Malayalam", "mr": "Marathi", "pa": "Punjabi", "ta": "Tamil",
                        "as": "Assamese", "or": "Odia", "ur": "Urdu", "ne": "Nepali","es":"Spanish","zh": "Chinese","fr": "French","de": "German",
                        "ja": "Japanese","ru": "Russian","ar": "Arabic","pt": "Portuguese",
                        "it": "Italian","ko": "Korean","tr": "Turkish","vi": "Vietnamese","fa": "Persian","th": "Thai"
                    }
                    target_language = st.selectbox("Select target language:", list(language_names.values()))

                    if st.button(" 🎛️ Translate Summary"):
                        target_language_code = list(language_names.keys())[list(language_names.values()).index(target_language)]
                        translated_text = translate_text(st.session_state['summary'], target_language_code)
                        st.session_state['translated_text'] = translated_text

                    st.text_area("Translated Text", value=st.session_state['translated_text'], height=500)
    with tab2:
         # Generate and display mind map

        # Display thumbnail
        if youtube_link:
            video_id = youtube_link.split("v=")[1].split("&")[0]
            st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)


        if st.button(" 🕹️ Generate Mind Map"):
            if st.session_state['summary']:
                mindmap_summary = generate_gemini_content_mindmap(st.session_state['summary'], promptM)
                
                st.session_state['mindmaptext'] = mindmap_summary
                data = f'''+{mindmap_summary}+'''
                st.success("mindmap is Generated",icon="✅")
                st.warning("Click Translate Mindmap to get mindmap in various formats",icon="🎛️")
                st.balloons()


 

        with st.container():
            language_names = {
                "en": "English","te": "Telugu", "hi": "Hindi", "bn": "Bengali", "gu": "Gujarati", "kn": "Kannada",
                "ml": "Malayalam", "mr": "Marathi", "pa": "Punjabi", "ta": "Tamil", 
                "as": "Assamese", "or": "Odia", "ur": "Urdu", "ne": "Nepali", "es": "Spanish", "fr": "French",
                "de": "German", "it": "Italian", "pt": "Portuguese", "ru": "Russian", "zh": "Chinese", 
                "ja": "Japanese", "ko": "Korean", "ar": "Arabic", "tr": "Turkish", "vi": "Vietnamese",
                "th": "Thai", "ms": "Malay", "id": "Indonesian", "fa": "Persian"
            }
            target_language = st.selectbox("Select language:", list(language_names.values()))

            if st.button(" 🎛️ Translate Mindmap"):
                target_language_code = list(language_names.keys())[list(language_names.values()).index(target_language)]
                translated_mindmap = translate_text(st.session_state['mindmaptext'], target_language_code)
                st.session_state['translated_text_mindmap'] = translated_mindmap
               
                tdata = st.session_state['translated_text_mindmap']
                markmap(tdata,height=1080) 
        


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


