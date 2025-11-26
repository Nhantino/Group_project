import streamlit as st
from PIL import Image
import easyocr
import requests
import urllib.parse
import yake
from nltk.corpus import stopwords
import nltk
from googlesearch import search
import time
import os
import tempfile

# Initialize EasyOCR
@st.cache_resource
def get_ocr():
    return easyocr.Reader(['vi', 'en'], gpu=False)

# Initialize YAKE extractor
@st.cache_resource
def get_yake_extractor():
    return yake.KeywordExtractor(top_n=5, stopwords=None)

# Download stopwords
try:
    stopwords.words('english')
except:
    nltk.download('stopwords', quiet=True)

# Page configuration
st.set_page_config(
    page_title="OCR & Search Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - ChatGPT Style
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #42a5f5;
    }
    
    [data-testid="stMain"] {
        background: #42a5f5;
    }
    
    h1 {
        color: #000;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: #333;
        font-size: 1rem;
        margin-bottom: 30px;
    }
    
    /* Chat Message Styling */
    .chat-message {
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        display: flex;
        gap: 12px;
        animation: slideIn 0.3s ease-in;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: #0d47a1;
        color: white;
        justify-content: flex-end;
        border-radius: 18px;
        padding: 12px 16px;
    }
    
    .assistant-message {
        background: #f3f3f3;
        color: #000;
        border-left: 4px solid #0d47a1;
        border-radius: 12px;
        padding: 16px;
    }
    
    .extracted-text-box {
        background: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        font-family: 'Courier New', monospace;
        font-size: 0.95rem;
        line-height: 1.6;
        max-height: 300px;
        overflow-y: auto;
        color: #000;
    }
    
    .search-results-container {
        margin-top: 16px;
        padding: 12px;
        background: #f3f3f3;
        border-radius: 8px;
    }
    
    .search-item {
        background: white;
        border-left: 4px solid #0d47a1;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        transition: all 0.2s ease;
    }
    
    .search-item:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .search-item-title {
        font-weight: 600;
        color: #0d47a1;
        margin-bottom: 4px;
    }
    
    .search-item-url {
        color: #0d47a1;
        text-decoration: none;
        font-size: 0.9rem;
    }
    
    .search-item-url:hover {
        text-decoration: underline;
    }
    
    .search-item-snippet {
        color: #666;
        font-size: 0.85rem;
        margin-top: 4px;
    }
    
    .keyword-badge {
        display: inline-block;
        background: #0d47a1;
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    
    .stButton > button {
        background-color: #0d47a1 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
    }
    
    .stButton > button:hover {
        background-color: #0a3d91 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>05_EASYOCR_KEYBERT</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Upload ảnh → Scan text → Trích từ khóa → Search Google</p>", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

if "keywords" not in st.session_state:
    st.session_state.keywords = []

if "search_results" not in st.session_state:
    st.session_state.search_results = []


def extract_keywords(text, num_keywords=5):
    """Extract keywords from text using YAKE"""
    try:
        kw_extractor = get_yake_extractor()
        keywords = kw_extractor.extract_keywords(text)
        # keywords is list of tuples (keyword, score), sorted by score
        keyword_list = [kw[0] for kw in keywords[:num_keywords]]
        return keyword_list if keyword_list else ["document"]
    except:
        # Fallback: use simple stopwords method
        try:
            stop_words = set(stopwords.words('english'))
            words = text.lower().split()
            keywords = [w for w in words if len(w) > 3 and w not in stop_words and w.isalpha()]
            if not keywords:
                keywords = [w for w in words if len(w) > 2]
            keywords = list(dict.fromkeys(keywords))[:num_keywords]
            return keywords if keywords else ["document"]
        except:
            words = text.split()
            keywords = [w for w in words[:num_keywords] if len(w) > 2]
            return keywords if keywords else ["document"]


def search_google(query, num_results=5):
    """Search Google and return results"""
    results = []
    
    try:
        google_results = list(search(query, num_results=num_results, stop=num_results, pause=1))
        for idx, url in enumerate(google_results, 1):
            if url and url.startswith('http'):
                try:
                    domain = url.split('/')[2] if '/' in url else url
                    results.append({
                        'title': domain,
                        'url': url,
                        'snippet': 'Search result'
                    })
                except:
                    pass
    except Exception as e:
        pass
    
    # Fallback
    if len(results) == 0:
        results.append({
            'title': 'Google Search',
            'url': f'https://www.google.com/search?q={urllib.parse.quote(query)}',
            'snippet': 'Click to search on Google'
        })
    
    return results[:num_results]


# Main Layout
col1, col2 = st.columns([1, 1], gap="large")

# Left column - Upload and Process
with col1:
    st.markdown("### 📸 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image with text",
        type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True, caption="Uploaded Image")
        
        # OCR Button
        if st.button("🔎 Scan Text", use_container_width=True, key="scan_btn"):
            with st.spinner('Scanning text...'):
                try:
                    # Save uploaded file to temporary location
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                        tmp_file.write(uploaded_file.getbuffer())
                        tmp_path = tmp_file.name
                    
                    try:
                        reader = get_ocr()
                        results = reader.readtext(tmp_path)
                        
                        extracted_text = ""
                        if results:
                            for detection in results:
                                # Each detection is (bbox, text, confidence)
                                text = detection[1]
                                extracted_text += text + " "
                        
                        extracted_text = extracted_text.strip()
                        
                        if extracted_text:
                            st.session_state.extracted_text = extracted_text
                            st.session_state.chat_history.append({
                                "role": "user",
                                "content": f"Uploaded image: {uploaded_file.name}"
                            })
                            st.success("✅ Text scanned successfully!")
                        else:
                            st.error("❌ No text found in image")
                    finally:
                        # Clean up temporary file
                        if os.path.exists(tmp_path):
                            os.remove(tmp_path)
                except Exception as e:
                    st.error(f"Error scanning: {str(e)}")

# Right column - Chat and Results
with col2:
    st.markdown("### 💬 Conversation")
    
    # Chat History
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(
                    f'<div class="chat-message user-message">{message["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="chat-message assistant-message">{message["content"]}</div>',
                    unsafe_allow_html=True
                )
    
    st.divider()
    
    # Display Extracted Text
    if st.session_state.extracted_text:
        with st.expander("📄 Extracted Text", expanded=True):
            st.markdown(
                f'<div class="extracted-text-box">{st.session_state.extracted_text[:500]}{"..." if len(st.session_state.extracted_text) > 500 else ""}</div>',
                unsafe_allow_html=True
            )
        
        # Extract Keywords Button
        col_key1, col_key2 = st.columns(2)
        with col_key1:
            if st.button("🏷️ Extract Keywords", use_container_width=True):
                with st.spinner('Extracting keywords...'):
                    keywords = extract_keywords(st.session_state.extracted_text, num_keywords=5)
                    st.session_state.keywords = keywords
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"Keywords: {', '.join(keywords)}"
                    })
                    st.rerun()
        
        # Search Button
        with col_key2:
            if st.button("🔗 Search Results", use_container_width=True):
                if st.session_state.keywords:
                    with st.spinner('Searching...'):
                        query = ' '.join(st.session_state.keywords)
                        results = search_google(query, num_results=5)
                        st.session_state.search_results = results
                        
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": f"Found {len(results)} results for: {query}"
                        })
                        st.rerun()
                else:
                    st.warning("Please extract keywords first!")
        
        # Display Keywords
        if st.session_state.keywords:
            st.markdown("**Keywords:**")
            keywords_html = "".join([f'<span class="keyword-badge">{kw}</span>' for kw in st.session_state.keywords])
            st.markdown(f'<div>{keywords_html}</div>', unsafe_allow_html=True)
        
        # Display Search Results
        if st.session_state.search_results:
            st.markdown("**Search Results:**")
            results_html = '<div class="search-results-container">'
            
            for idx, result in enumerate(st.session_state.search_results, 1):
                results_html += f'''
                <div class="search-item">
                    <div class="search-item-title">{idx}. {result['title']}</div>
                    <a href="{result['url']}" target="_blank" class="search-item-url">🔗 {result['url'][:60]}...</a>
                    <div class="search-item-snippet">{result['snippet']}</div>
                </div>
                '''
            
            results_html += '</div>'
            st.markdown(results_html, unsafe_allow_html=True)
        
        # Clear Button
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.extracted_text = ""
            st.session_state.keywords = []
            st.session_state.search_results = []
            st.rerun()

# Footer
st.divider()
st.markdown(
    "<p style='text-align: center; color: #fff; font-size: 0.85rem;'>Built with Streamlit | OCR: EasyOCR | Search: Google</p>",
    unsafe_allow_html=True
)