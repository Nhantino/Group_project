import streamlit as st
from PIL import Image
import os
import tempfile
import urllib.parse
import html

# Import local modules
import app_styles
import ocr_service
import text_analysis
import web_search

# SerpAPI credentials
try:
    SERPAPI_API_KEY = st.secrets["SERPAPI_API_KEY"]
except (FileNotFoundError, KeyError):
    # Fallback for local development without secrets.toml
    # It is recommended to create .streamlit/secrets.toml locally
    SERPAPI_API_KEY = "8a7f63187c4434a378accb86f4dd104be846755eef9bf0a5a0802020721bc8b7"

# Page configuration
st.set_page_config(
    page_title="OCR & Search Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Custom CSS
app_styles.apply_custom_css()

# Header
st.markdown("<h1>05_EASYOCR_YAKE</h1>", unsafe_allow_html=True)
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
                        extracted_text = ocr_service.scan_image(tmp_path)
                        
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
                    f'<div class="chat-message user-message">{html.escape(message["content"])}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="chat-message assistant-message">{html.escape(message["content"])}</div>',
                    unsafe_allow_html=True
                )
    
    st.divider()
    
        # Display Extracted Text
    if st.session_state.extracted_text:
        with st.expander("📄 Extracted Text", expanded=True):
            st.markdown(
                f'<div class="extracted-text-box">{html.escape(st.session_state.extracted_text)}</div>',
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
                wer, accuracy = text_analysis.calculate_wer(original_text, st.session_state.extracted_text)
                
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
                    keywords = text_analysis.extract_keywords(text_to_extract)
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
                        results = web_search.search_google(query, SERPAPI_API_KEY, num_results=10)
                        st.session_state.search_results = results
                        
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": f"Found {len(results)} results for: {query}"
                        })
                        st.rerun()
                else:
                    st.warning("Please extract keywords first!")        # Display Keywords
        if st.session_state.keywords:
            st.markdown("**Keywords:**")
            keywords_html = "".join([f'<span class="keyword-badge">{html.escape(kw)}</span>' for kw in st.session_state.keywords])
            st.markdown(f'<div>{keywords_html}</div>', unsafe_allow_html=True)
        
        # Display Search Results
        if st.session_state.search_results:
            st.markdown("**Search Results:**")
            results_html = '<div class="search-results-container">'
            
            for idx, result in enumerate(st.session_state.search_results, 1):
                # Escape HTML special characters in title and snippet
                title = html.escape(result['title'])
                snippet = html.escape(result['snippet'])
                url = html.escape(result['url'])
                
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
