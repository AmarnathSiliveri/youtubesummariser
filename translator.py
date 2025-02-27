import streamlit as st
from deep_translator import GoogleTranslator
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from streamlit_option_menu import option_menu
from streamlit_markmap import markmap
from streamlit_lottie import st_lottie
import json
import re
from urllib.parse import urlparse, parse_qs

# Configure Google API

genai.configure(api_key=st.secrets['API_KEY'])
#streamlit app
st.set_page_config(page_title="YOUTUBE VIDEO NOTES GENERATOR", page_icon='📜')  # page title
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1.0">', unsafe_allow_html=True)




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

promptM = """Generate a detailed markdown code for the provided summary with the following elements:
A title suitable for the summary given below and a clear main topic and logically connected subtopics. Make sure every main topic has subtopics and every subtopic has appropriate content make bullet points. Also, provide Hyperlinks for additional information
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
                    "container": {"padding": "2!important","background-color":'#grey'},
        "icon": {"color": "white", "font-size": "20px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#FDDE55"},
        "nav-link-selected": {"background-color": "#40A578"},
        } 
        )

def load_lottiefiles(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

if app =="INTRO":
    st.markdown("""# <span style='color:#022302'>Welcome to My Streamlit App *YOUTUBE VIDEO  TO NOTES GENERATOR*</span>""", unsafe_allow_html=True)

    st.markdown("""> ### <span style='color:#0DB386'> Based on Gemini-PRO LLM API FROM GOOGLE</span>""", unsafe_allow_html=True)
    
    st.markdown("""## <span style='color:#022302'>Introduction</span>""", unsafe_allow_html=True)

    st.markdown(""" > #### <span style='color:#0DB386'>This is YOUTUBE VIDEO NOTES GENERATOR converts youtube video into a notes generator also included with translation capabilities </span>""", unsafe_allow_html=True)

    st.markdown("""## <span style='color:#22302'>What is YOUTUBE VIDEO NOTES GENERATOR ? </span>""", unsafe_allow_html=True)

    st.markdown("""
        <div style='font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; font-size: 20px;'>
            Our app acts as your digital assistant 🤖 for extracting and summarizing YouTube video content:
                    <br>
            📹 Provide a YouTube video link, and our app fetches the transcript automatically.
                    <br>
            📝 The transcript is analyzed using the Gemini-PRO LLM API to generate comprehensive notes.
                    <br>
            🚀 With features like detailed summaries and key insights, it transforms video content into easily digestible information and 
                mindmaps.
                    <br>
            🌐 Supports multiple languages, making it accessible for a global audience.
                    <br>
            💡 Ideal for students, professionals, and anyone looking to convert video content into readable notes quickly.
        </div>
    """, unsafe_allow_html=True)

    st.header(" ")
    st.success("Navigate to   *YT NOTES*   tab for insights")

if app == "YT NOTES":

    def extract_video_id(youtube_url):
        """
        Extract the video ID from various YouTube URL formats.
        
        Supported formats include:
        - Standard: https://www.youtube.com/watch?v=VIDEO_ID
        - Short: https://youtu.be/VIDEO_ID
        - Mobile: https://m.youtube.com/watch?v=VIDEO_ID
        - Embedded: https://www.youtube.com/embed/VIDEO_ID
        - With playlist: https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID
        - Mobile app share: youtube://VIDEO_ID
        
        Returns:
            str: YouTube video ID if successful, None otherwise
        """
        if not youtube_url:
            return None
        
        # Clean the URL (remove extra spaces, etc.)
        youtube_url = youtube_url.strip()
        
        # Case 1: youtu.be/VIDEO_ID format
        if 'youtu.be' in youtube_url:
            parsed_url = urlparse(youtube_url)
            video_id = parsed_url.path.lstrip('/')
            return video_id.split('?')[0]  # Remove any query parameters
        
        # Case 2: youtube://VIDEO_ID format (from mobile app)
        elif youtube_url.startswith('youtube://'):
            return youtube_url.split('youtube://')[1].split('?')[0]
        
        # Case 3: /embed/ format
        elif '/embed/' in youtube_url:
            parsed_url = urlparse(youtube_url)
            video_id = parsed_url.path.split('/embed/')[1]
            return video_id.split('?')[0]  # Remove any query parameters
        
        # Case 4: Standard v= parameter format
        elif 'youtube.com' in youtube_url or 'm.youtube.com' in youtube_url:
            parsed_url = urlparse(youtube_url)
            query_params = parse_qs(parsed_url.query)
            
            if 'v' in query_params:
                return query_params['v'][0]
        
        # Case 5: Try regex as fallback for any other format
        else:
            regex_patterns = [
                r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
                r'(?:youtube\.com\/watch\?v=)([^&]+)',
                r'(?:youtu\.be\/)([^?]+)'
            ]
            
            for pattern in regex_patterns:
                match = re.search(pattern, youtube_url)
                if match:
                    return match.group(1)
        
        # If no pattern matches, return None
        return None

    tab1,tab2=st.tabs([" 🔑📝Summary "," 💡🌿Mindmap "])
    with tab1:
        # Import the extract_video_id function or include it in your code
        
        # Function to extract transcript details from YouTube video
        def extract_transcript_details(youtube_video_url):
            try:
                video_id = extract_video_id(youtube_video_url)
                if not video_id:
                    st.warning("Could not extract video ID. Please provide a valid YouTube video URL.")
                    return None
                    
                transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
                transcript = " ".join([i["text"] for i in transcript_text])
                return transcript
            except Exception as e:
                st.warning(f"Error extracting transcript: Please provide a valid YouTube video URL. {str(e)}")
                return None

        # Function to generate summary using Gemini model
        def generate_gemini_content(transcript_text, prompt):
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt + transcript_text + " ")
            return response.text
            
        # Function to generate markdown code for markmap function to generate mindmap using gemini model
        def generate_gemini_content_mindmap(summary, promptM):
            model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
            response = model.generate_content(promptM + summary + " ")
            return response.text

        # Function to generate translations
        def translate_text(text, target_language):
            try:
                translator = GoogleTranslator(source='auto', target=target_language)
                
                # Check if text is longer than the 5000 character limit
                if len(text) <= 5000:
                    # If text is within limits, translate it directly
                    return translator.translate(text)
                else:
                    # If text is too long, split it into chunks of 4500 characters
                    # (leaving some margin below the 5000 limit)
                    chunks = []
                    chunk_size = 4500
                    
                    # Split by sentences to avoid cutting in the middle of sentences when possible
                    import re
                    sentences = re.split('(?<=[.!?])\s+', text)
                    
                    current_chunk = ""
                    for sentence in sentences:
                        # If adding this sentence would exceed chunk size, add current chunk to results
                        if len(current_chunk) + len(sentence) + 1 > chunk_size and current_chunk:
                            chunks.append(current_chunk)
                            current_chunk = sentence
                        else:
                            if current_chunk:
                                current_chunk += " " + sentence
                            else:
                                current_chunk = sentence
                    
                    # Add the last chunk if it's not empty
                    if current_chunk:
                        chunks.append(current_chunk)
                    
                    # If we couldn't split by sentences properly, fall back to character chunking
                    if not chunks:
                        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
                    
                    # Translate each chunk and join them
                    translated_chunks = []
                    for chunk in chunks:
                        translated_chunk = translator.translate(chunk)
                        translated_chunks.append(translated_chunk)
                    
                    # Join all translated chunks
                    return " ".join(translated_chunks)

    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return f"Error translating text: {str(e)}"
        
        # Streamlit app
        st.title("YouTube video  to Detailed Notes ")
        st.markdown("### <span style='color:#0DB386'>Convert  **Youtube Video**  to **TEXT** on clicking *Get Detailed Notes* summary/notes is generated</span>",unsafe_allow_html=True)
        with st.expander(" 👆 Click it"):
            st.warning("hey people ",icon="👋")
            st.warning("after note generation",icon="📝")
            st.warning("Click Translate to translate the summary  into a language of your comfort by clicking dropdown menu ",icon="⬇️")

        # Input fields
        youtube_link = st.text_input("Enter YouTube Video Link:")
        
        # Display video - safely handling all types of YouTube links
        if youtube_link:
            video_id = extract_video_id(youtube_link)
            if video_id:
                st.video(f"https://www.youtube.com/watch?v={video_id}")
            else:
                st.warning("Could not extract video ID from the provided link.")

        # Generate detailed notes
        if st.button(" 🕹️ Generate Notes",use_container_width=True):
            with st.spinner("Extracting transcript and generating notes..."):
                transcript_text = extract_transcript_details(youtube_link)
                if transcript_text:
                    summary = generate_gemini_content(transcript_text, prompt1)
                    st.session_state['transcript_text'] = transcript_text
                    st.session_state['summary'] = summary
                else:
                    st.error("Could not extract transcript. Please check your YouTube link.")

        with st.container():
            if 'summary' in st.session_state and st.session_state['summary']:
                st.markdown("## Detailed Notes:")
                st.markdown(
                f"""
                <div style="font-family: 'Arial', 'Roborto Mono',monospace; font-size: 22px; color: #000;">
                    {st.session_state['summary']}
                </div>
                """,
                unsafe_allow_html=True
            )
            if 'summary' in st.session_state and st.session_state['summary']:
                st.download_button(
                label="⬇️Download summary",
                data=(st.session_state["summary"].encode('utf-8')),
                file_name="summary.txt",
                mime="text/plain",use_container_width=True,help="🥁Downloads the entire generated summary"
            )
        
        # Initialize session state variables if they don't exist
        if 'translated_text' not in st.session_state:
            st.session_state['translated_text'] = ""
            
        with st.expander("Translate"):
                    language_names = {
                        "en": "English", "te": "Telugu","hi": "Hindi", "bn": "Bengali", "gu": "Gujarati", "kn": "Kannada",
                        "ml": "Malayalam", "mr": "Marathi", "pa": "Punjabi", "ta": "Tamil",
                        "as": "Assamese", "or": "Odia", "ur": "Urdu", "ne": "Nepali","es":"Spanish","zh": "Chinese","fr": "French","de": "German",
                        "ja": "Japanese","ru": "Russian","ar": "Arabic","pt": "Portuguese",
                        "it": "Italian","ko": "Korean","tr": "Turkish","vi": "Vietnamese","fa": "Persian","th": "Thai"
                    }
                    target_language = st.selectbox("Select target language:", list(language_names.values()),help="Choose a Language of Your Comfort")
                    
                    if st.button(" 🎛️ Translate NOTES", use_container_width=True):
                        if 'summary' in st.session_state and st.session_state['summary']:
                            target_language_code = list(language_names.keys())[list(language_names.values()).index(target_language)]
                            translated_text = translate_text(st.session_state['summary'], target_language_code)
                            st.session_state['translated_text'] = translated_text
                        else:
                            st.warning("Please generate notes first before translating.")

                    if st.session_state['translated_text']:
                        st.markdown(st.session_state['translated_text'])
                        st.download_button(
                            label="⬇️Download Translated Summary",
                            data=st.session_state['translated_text'].encode('utf-8'),
                            file_name=f"{target_language} translated_summary.txt",
                            mime="text/plain",
                            use_container_width=True,
                            help="🥁 Downloads the entire Translated summary",
                        )

    with tab2:
        # Initialize mindmap session state if needed
        if 'mindmaptext' not in st.session_state:
            st.session_state['mindmaptext'] = ""
        if 'translated_text_mindmap' not in st.session_state:
            st.session_state['translated_text_mindmap'] = ""
             
        # Display thumbnail safely 
        if youtube_link:
            video_id = extract_video_id(youtube_link)
            if video_id:
                st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
            else:
                st.warning("Could not extract video ID from the provided link.")

        if st.button("🕹️ Generate Mind Map", use_container_width=True, help="🥁 CLICK TO GENERATE MINDMAP"):
            if 'summary' in st.session_state and st.session_state.get('summary'):
                with st.spinner("Generating mind map..."):
                    mindmap_summary = generate_gemini_content_mindmap(st.session_state['summary'], promptM)
                    st.session_state['mindmaptext'] = mindmap_summary
                    data = f'{{"nodes": ["{mindmap_summary}"]}}'
                    st.success("Mindmap is Generated", icon="✅")
                    st.warning("Click Translate Mindmap to get mindmap in various formats", icon="🎛️")
                    st.balloons()
            else:
                st.warning("Please generate notes first in the Summary tab.")

        with st.container():
                language_names = {
                    "en": "English", "te": "Telugu", "hi": "Hindi", "bn": "Bengali", "gu": "Gujarati", "kn": "Kannada",
                    "ml": "Malayalam", "mr": "Marathi", "pa": "Punjabi", "ta": "Tamil",
                    "as": "Assamese", "or": "Odia", "ur": "Urdu", "ne": "Nepali", "es": "Spanish", "fr": "French",
                    "de": "German", "it": "Italian", "pt": "Portuguese", "ru": "Russian", "zh": "Chinese",
                    "ja": "Japanese", "ko": "Korean", "ar": "Arabic", "tr": "Turkish", "vi": "Vietnamese",
                    "th": "Thai", "ms": "Malay", "id": "Indonesian", "fa": "Persian"
                }
                target_language = st.selectbox("Select language:", list(language_names.values()), help="choose language of your comfort")

        if st.button("🎛️ Translate Mindmap"):
                if 'mindmaptext' in st.session_state and st.session_state['mindmaptext']:
                    target_language_code = list(language_names.keys())[list(language_names.values()).index(target_language)]
                    translated_mindmap = translate_text(st.session_state['mindmaptext'], target_language_code)
                    st.session_state['translated_text_mindmap'] = translated_mindmap

                    tdata = st.session_state['translated_text_mindmap']
                    
                    markmap(tdata, height=800)
                else:
                    st.warning("Please generate a mind map first before translating.")


if app == 'CREDITS':
    lottie_credit = load_lottiefiles(r"thankyou bymonkeymoji (1).json")
    st_lottie(lottie_credit, loop=True,quality="high", speed=1.45, key=None, height=350)
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

hide_st_style= """
       <style>
       #mainmenu {visibility:hidden;}
       footer {visibility:hidden;}
       header {visibility:hidden;}
       </style>
 """
st.markdown(hide_st_style,unsafe_allow_html=True)

