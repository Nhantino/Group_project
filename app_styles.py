import streamlit as st

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
