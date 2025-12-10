import yake
from nltk.corpus import stopwords
import nltk
import streamlit as st
import difflib
import re
import unicodedata

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
