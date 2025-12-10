"""
OCR Service using EasyOCR
This module provides functionality to extract text from images using EasyOCR.
Compatible with Streamlit caching.
"""

import easyocr
import streamlit as st


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
