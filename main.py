import streamlit as st
from PIL import Image
import pytesseract
import io
import time
import os
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Cấu hình Tesseract cho Windows (uncomment và sửa đường dẫn nếu cần)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Cấu hình trang
st.set_page_config(
    page_title="AI Image Text Search",
    page_icon="🔍",
    layout="wide"
)

# CSS để tạo giao diện giống Claude/ChatGPT
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main {
        background-color: #f7f7f8;
    }
    
    .stChatMessage {
        background-color: white;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .stChatInputContainer {
        border-top: 1px solid #e5e5e5;
        background-color: white;
        padding: 16px 0;
    }
    
    h1 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d2d2d;
        text-align: center;
        padding: 20px 0;
        margin: 0;
    }
    
    .extracted-text {
        background-color: #f0f4f8;
        border-left: 4px solid #4a90e2;
        padding: 12px;
        border-radius: 8px;
        margin: 12px 0;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    
    .search-result-item {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        transition: box-shadow 0.3s;
    }
    
    .search-result-item:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .result-title {
        color: #1a73e8;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    .result-url {
        color: #5f6368;
        font-size: 0.85rem;
        margin-bottom: 8px;
    }
    
    .result-snippet {
        color: #3c4043;
        font-size: 0.95rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

def search_duckduckgo(query, num_results=5):
    """Tìm kiếm trên DuckDuckGo (không cần API key)"""
    try:
        search_url = "https://html.duckduckgo.com/html/"
        params = {
            'q': query,
            'kl': 'vn-vn'  # Region Vietnam
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.post(search_url, data=params, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        result_divs = soup.find_all('div', class_='result', limit=num_results)
        
        for div in result_divs:
            title_tag = div.find('a', class_='result__a')
            snippet_tag = div.find('a', class_='result__snippet')
            
            if title_tag:
                title = title_tag.get_text(strip=True)
                url = title_tag.get('href', '')
                snippet = snippet_tag.get_text(strip=True) if snippet_tag else "Không có mô tả"
                
                results.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet
                })
        
        return results
    except Exception as e:
        st.error(f"Lỗi khi tìm kiếm: {str(e)}")
        return []

def search_google_custom(query, num_results=5):
    """Tìm kiếm trên Google bằng cách scrape (backup method)"""
    try:
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&hl=vi&num={num_results}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        search_results = soup.find_all('div', class_='g', limit=num_results)
        
        for result in search_results:
            title_tag = result.find('h3')
            link_tag = result.find('a')
            snippet_tag = result.find('div', class_=['VwiC3b', 'yXK7lf'])
            
            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                url = link_tag.get('href', '')
                snippet = snippet_tag.get_text(strip=True) if snippet_tag else "Không có mô tả"
                
                if url.startswith('http'):
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet
                    })
        
        return results
    except Exception as e:
        return []

# Khởi tạo session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.title("🔍 AI Image Text Search")

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "image":
            st.image(message["content"], width=300)
        elif message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "extracted":
            st.markdown(f'<div class="extracted-text"><strong>📝 Text trích xuất:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
        elif message["type"] == "search_results":
            st.markdown("### 🔎 Kết quả tìm kiếm:")
            for idx, result in enumerate(message["content"], 1):
                st.markdown(f"""
                <div class="search-result-item">
                    <div class="result-title">{idx}. {result['title']}</div>
                    <div class="result-url">🔗 {result['url']}</div>
                    <div class="result-snippet">{result['snippet']}</div>
                </div>
                """, unsafe_allow_html=True)

# Input area với file uploader
uploaded_file = st.file_uploader(
    "📷 Tải lên hình ảnh để trích xuất text và tìm kiếm",
    type=["png", "jpg", "jpeg", "bmp", "tiff"],
    help="Hỗ trợ các định dạng: PNG, JPG, JPEG, BMP, TIFF"
)

if uploaded_file is not None:
    # Hiển thị hình ảnh người dùng upload
    st.session_state.messages.append({
        "role": "user",
        "type": "image",
        "content": uploaded_file
    })
    
    with st.chat_message("user"):
        st.image(uploaded_file, width=300)
    
    # Xử lý OCR và tìm kiếm
    with st.chat_message("assistant"):
        with st.spinner("🔄 Đang phân tích hình ảnh..."):
            try:
                # Đọc và xử lý hình ảnh
                image = Image.open(uploaded_file)
                
                # Thực hiện OCR
                extracted_text = pytesseract.image_to_string(image, lang='vie+eng')
                
                if extracted_text.strip():
                    # Hiển thị text trích xuất được
                    st.markdown(f'<div class="extracted-text"><strong>📝 Text trích xuất:</strong><br>{extracted_text}</div>', unsafe_allow_html=True)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "type": "extracted",
                        "content": extracted_text
                    })
                    
                    # Tìm kiếm trên web
                    with st.spinner("🌐 Đang tìm kiếm trên web..."):
                        # Lấy 100 ký tự đầu để tìm kiếm
                        search_query = extracted_text.strip()[:200]
                        
                        # Thử tìm kiếm DuckDuckGo trước
                        search_results = search_duckduckgo(search_query, num_results=5)
                        
                        # Nếu không có kết quả, thử Google
                        if not search_results:
                            search_results = search_google_custom(search_query, num_results=5)
                        
                        if search_results:
                            st.markdown("### 🔎 Kết quả tìm kiếm:")
                            for idx, result in enumerate(search_results, 1):
                                st.markdown(f"""
                                <div class="search-result-item">
                                    <div class="result-title">{idx}. {result['title']}</div>
                                    <div class="result-url">🔗 <a href="{result['url']}" target="_blank">{result['url']}</a></div>
                                    <div class="result-snippet">{result['snippet']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.session_state.messages.append({
                                "role": "assistant",
                                "type": "search_results",
                                "content": search_results
                            })
                        else:
                            st.warning("⚠️ Không tìm thấy kết quả tìm kiếm. Vui lòng thử lại sau.")
                else:
                    st.warning("⚠️ Không tìm thấy text trong hình ảnh. Vui lòng thử hình ảnh khác có chứa text rõ ràng hơn.")
                    
            except Exception as e:
                st.error(f"❌ Lỗi khi xử lý: {str(e)}")
                st.info("💡 Đảm bảo bạn đã cài đặt Tesseract OCR và các thư viện cần thiết.")

# Sidebar với hướng dẫn
with st.sidebar:
    st.markdown("### 📖 Hướng dẫn sử dụng")
    st.markdown("""
    1. **Tải lên hình ảnh** có chứa text
    2. Hệ thống sẽ **trích xuất text** bằng OCR
    3. **Tự động tìm kiếm** text đó trên web
    4. Hiển thị **kết quả tìm kiếm** từ DuckDuckGo/Google
    
    ---
    
    ### ⚙️ Cài đặt thêm
    
    ```bash
    pip install beautifulsoup4 requests
    ```
    
    ### 🔧 Tesseract OCR
    - Tải: [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
    - Nhớ chọn ngôn ngữ Vietnamese khi cài
    
    ---
    
    ### 🌐 Nguồn tìm kiếm
    - ✅ DuckDuckGo (primary)
    - ✅ Google (backup)
    - ✅ Kết quả thời gian thực
    """)
    
    if st.button("🗑️ Xóa lịch sử chat"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 0.9rem;'>Made with ❤️ using Streamlit | Real-time Image Search</p>",
    unsafe_allow_html=True
)