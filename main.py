import streamlit as st
from PIL import Image
import os
import tempfile
import urllib.parse
import easyocr
import yake
from nltk.corpus import stopwords
import nltk
import difflib
import re
import unicodedata
from serpapi import GoogleSearch

# ============================================================================
# APP STYLES - tất cả CSS styling cho ứng dụng
# ============================================================================

def apply_custom_css():
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
    
    /* Uniform Font for all text inputs and textareas */
    textarea, input, .stTextArea, [data-testid="stTextInput"] {
        font-family: Arial, sans-serif !important;
    }
    
    /* Extracted text box - same font */
    .extracted-text-box {
        font-family: Arial, sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# OCR SERVICE - dùng EasyOCR để scan text từ ảnh
# ============================================================================

@st.cache_resource
def get_ocr():
    """
    Initialize and cache EasyOCR reader for Vietnamese and English languages.
    Uses Streamlit's caching to avoid reloading the model on every run.
    
    Returns:
        easyocr.Reader: Initialized EasyOCR reader
    """
    return easyocr.Reader(['vi', 'en'], gpu=False)


def scan_image(image_path: str) -> str:
    """
    Extract text from an image using EasyOCR.
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        str: Extracted text from the image (text separated by spaces)
    """
    try:
        reader = get_ocr()
        results = reader.readtext(image_path)
        
        extracted_text = ""
        if results:
            for detection in results:
                # Each detection is (bbox, text, confidence)
                text = detection[1]
                extracted_text += text + " "
        
        return extracted_text.strip()
    
    except Exception as e:
        print(f"Error scanning image: {str(e)}")
        return ""


def scan_image_with_confidence(image_path: str, confidence_threshold: float = 0.3) -> dict:
    """
    Extract text from an image with confidence scores filtered by threshold.
    
    Args:
        image_path (str): Path to the image file
        confidence_threshold (float): Minimum confidence threshold (0-1). Default: 0.3
    
    Returns:
        dict: Dictionary containing:
            - 'text': Full extracted text (space-separated)
            - 'details': List of detections with text, confidence, and bbox
    """
    try:
        reader = get_ocr()
        results = reader.readtext(image_path)
        
        extracted_text = ""
        filtered_results = []
        
        if results:
            for detection in results:
                # Each detection is (bbox, text, confidence)
                bbox = detection[0]
                text = detection[1]
                confidence = detection[2]
                
                if confidence >= confidence_threshold:
                    extracted_text += text + " "
                    filtered_results.append({
                        'text': text,
                        'confidence': float(confidence),
                        'bbox': bbox
                    })
        
        return {
            "text": extracted_text.strip(),
            "details": filtered_results
        }
    
    except Exception as e:
        print(f"Error scanning image with confidence: {str(e)}")
        return {"text": "", "details": []}


def scan_image_advanced(image_path: str) -> str:
    """
    Extract text from an image (advanced version).
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        str: Extracted text from the image
    """
    return scan_image(image_path)


# ============================================================================
# TEXT ANALYSIS - xử lý text, trích từ khóa, tính độ chính xác
# ============================================================================

# Initialize YAKE extractor
@st.cache_resource
def get_yake_extractor():
    return yake.KeywordExtractor(top_n=None, stopwords=None)

# Download stopwords
try:
    stopwords.words('english')
except:
    nltk.download('stopwords', quiet=True)


def calculate_wer(original_text, ocr_text):
    """
    Calculate Word Error Rate (WER) using Fuzzy Matching
    So sánh từ gần giống nhau, không chỉ từ chính xác 100%
    
    Version: 3.0 (Fuzzy Matching - so sánh từ gần giống)
    """
    
    # Normalize text - loại bỏ tất cả ký tự lạ, chỉ giữ a-z, 0-9, dấu cách và dấu tách từ
    def normalize_text(text):
        # Chuyển sang NFD form để tách dấu tiếng Việt
        text = unicodedata.normalize('NFD', text)
        # Loại bỏ dấu (combining marks)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        # Chuyển thành chữ thường
        text = text.lower()
        # Thay thế các ký tự đặc biệt bằng dấu cách (để tách từ)
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        # Normalize multiple spaces to single space
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    original_normalized = normalize_text(original_text)
    ocr_normalized = normalize_text(ocr_text)
    
    # Split into words
    original_words = original_normalized.split()
    ocr_words = ocr_normalized.split()
    
    Nw = len(original_words)  # Total words in original
    
    if Nw == 0:
        return 0.0, 100.0
    
    # Fuzzy matching: so sánh từ gần giống
    matched_words = 0
    used_indices = set()
    
    for orig_word in original_words:
        # Tìm từ trong OCR text giống nhất với từ gốc
        best_match_score = 0
        best_match_idx = -1
        
        for idx, ocr_word in enumerate(ocr_words):
            if idx in used_indices:
                continue
            
            # Dùng SequenceMatcher để tính độ khớp (0-1)
            matcher = difflib.SequenceMatcher(None, orig_word, ocr_word)
            similarity = matcher.ratio()
            
            # Chỉ tính là match nếu độ khớp >= 0.8 (80%)
            if similarity > best_match_score and similarity >= 0.8:
                best_match_score = similarity
                best_match_idx = idx
        
        # Nếu tìm được từ khớp >= 80%
        if best_match_idx >= 0:
            matched_words += 1
            used_indices.add(best_match_idx)
    
    # Calculate WER dựa trên từ khớp
    errors = Nw - matched_words
    wer = errors / Nw
    
    # Calculate Accuracy
    accuracy = (1 - wer) * 100
    accuracy = max(0.0, min(accuracy, 100.0))
    
    return float(wer), float(accuracy)


def extract_keywords(text, num_keywords=None):
    """Extract keywords from text using YAKE"""
    try:
        kw_extractor = get_yake_extractor()
        keywords = kw_extractor.extract_keywords(text)
        # keywords is list of tuples (keyword, score), sorted by score
        if num_keywords:
            keyword_list = [kw[0] for kw in keywords[:num_keywords]]
        else:
            keyword_list = [kw[0] for kw in keywords]
        return keyword_list if keyword_list else ["document"]
    except:
        # Fallback: use simple stopwords method
        try:
            stop_words = set(stopwords.words('english'))
            words = text.lower().split()
            keywords = [w for w in words if len(w) > 3 and w not in stop_words and w.isalpha()]
            if not keywords:
                keywords = [w for w in words if len(w) > 2]
            keywords = list(dict.fromkeys(keywords))
            return keywords if keywords else ["document"]
        except:
            words = text.split()
            keywords = [w for w in words if len(w) > 2]
            return keywords if keywords else ["document"]


# ============================================================================
# WEB SEARCH - tìm kiếm Google bằng SerpAPI
# ============================================================================

def search_google(query, api_key, num_results=5):
    """Search Google using SerpAPI"""
    results = []
    
    try:
        # Setup SerpAPI parameters
        params = {
            "q": query,
            "api_key": api_key,
            "num": num_results,
            "engine": "google"
        }
        
        # Execute the search
        search = GoogleSearch(params)
        result = search.get_dict()
        
        # Extract organic results
        if "organic_results" in result:
            for item in result["organic_results"][:num_results]:
                results.append({
                    'title': item.get('title', 'No title'),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', 'No snippet')
                })
        else:
            if "error" in result:
                pass
        
    except Exception as e:
        # Fallback: provide Google Search link
        results.append({
            'title': 'Google Search',
            'url': f'https://www.google.com/search?q={urllib.parse.quote(query)}',
            'snippet': 'Click to search on Google'
        })
    
    return results[:num_results]


# ============================================================================
# MAIN APP - giao diện Streamlit
# ============================================================================

# SerpAPI credentials
SERPAPI_API_KEY = "8a7f63187c4434a378accb86f4dd104be846755eef9bf0a5a0802020721bc8b7"

# Page configuration
st.set_page_config(
    page_title="OCR & Search Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Custom CSS
apply_custom_css()

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
                        extracted_text = scan_image(tmp_path)
                        
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
                f'<div class="extracted-text-box">{st.session_state.extracted_text}</div>',
                unsafe_allow_html=True
            )
        
        # OCR Accuracy Check Section
        st.markdown("### 🎯 Check OCR Accuracy")
        
        st.markdown("**👁️ Nhập Original Text (nhìn vào ảnh gõ tay):**")
        original_text = st.text_area(
            "Original Text:",
            height=120,
            placeholder="Nhìn vào ảnh và gõ/copy text chính xác từ ảnh...",
            label_visibility="collapsed",
            key="original_text_input"
        )
        
        if original_text and st.session_state.extracted_text:
            if st.button("📊 Tính Độ Chính Xác", use_container_width=True):
                wer, accuracy = calculate_wer(original_text, st.session_state.extracted_text)
                
                # Display result
                accuracy_text = f"Độ chính xác: {accuracy:.2f}%"
                
                # Color coding based on accuracy
                if accuracy >= 90:
                    color = "🟢"
                    status = "Xuất sắc"
                elif accuracy >= 70:
                    color = "🟡"
                    status = "Tốt"
                elif accuracy >= 50:
                    color = "🟠"
                    status = "Trung bình"
                else:
                    color = "🔴"
                    status = "Cần cải thiện"
                
                st.markdown(f"""
                <div style="background: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
                    <h2 style="color: #000; margin: 0;">{color} {accuracy_text}</h2>
                    <p style="color: #666; margin: 10px 0; font-size: 1rem;">Status: <strong>{status}</strong></p>
                    <p style="color: #666; margin-top: 10px; font-size: 0.9rem;">WER: {wer:.4f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": accuracy_text
                })
        
        st.divider()
        
        # Extract Keywords Button
        col_key1, col_key2 = st.columns(2)
        with col_key1:
            if st.button("🏷️ Extract Keywords", use_container_width=True):
                with st.spinner('Extracting keywords...'):
                    # Use original_text if provided, otherwise use extracted_text
                    text_to_extract = original_text if original_text and original_text.strip() else st.session_state.extracted_text
                    keywords = extract_keywords(text_to_extract)
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
                        results = search_google(query, SERPAPI_API_KEY, num_results=10)
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
                # Escape HTML special characters in title and snippet
                title = result['title'].replace('<', '&lt;').replace('>', '&gt;')
                snippet = result['snippet'].replace('<', '&lt;').replace('>', '&gt;')
                url = result['url']
                
                results_html += f'''<div class="search-item">
                    <div class="search-item-title">{idx}. {title}</div>
                    <a href="{url}" target="_blank" class="search-item-url">🔗 {url[:60]}...</a>
                    <div class="search-item-snippet">{snippet}</div>
                </div>'''
            
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
