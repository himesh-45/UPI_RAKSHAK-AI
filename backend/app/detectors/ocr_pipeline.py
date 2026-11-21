import io
import re
from typing import Dict, Any, List, Optional
import cv2
import numpy as np
from PIL import Image
import pytesseract
from .url_scanner import url_scanner
from .qr_scanner import qr_scanner

PHONE_REGEX = re.compile(r'(?<!\d)(?:\+91[-\s]?)?[6-9]\d{9}(?!\d)')
UPI_VPA_REGEX = re.compile(r'\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z0-9.\-_]{2,}\b')
AMOUNT_REGEX = re.compile(r'(?i)(?:Rs\.?|INR|₹)\s*([\d,]+(?:\.\d{2})?)')
KEYWORDS = [
    "kyc", "verify", "block", "suspend", "disconnect", "electricity",
    "otp", "pin", "cvv", "refund", "cashback", "reward", "lottery",
    "kbc", "bill", "urgent", "anydesk", "teamviewer"
]

class OCRPipeline:
    """
    Multilingual Image & QR OCR Pipeline with preprocessing and robust fallback.
    """

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        # Convert PIL to BGR OpenCV format
        cv_img = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2BGR)
        
        # Convert to Grayscale
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        
        # Contrast Limited Adaptive Histogram Equalization (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Adaptive Thresholding for crisp text edges
        thresh = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        return thresh

    def extract_text_with_ocr(self, image: Image.Image) -> str:
        """
        Attempts Tesseract OCR across en, hi, te languages, with fallback.
        """
        try:
            # Try multilingual packs
            text = pytesseract.image_to_string(image, lang="eng+hin+tel")
            if text and text.strip():
                return text.strip()
        except Exception:
            pass

        try:
            # Try english only
            text = pytesseract.image_to_string(image, lang="eng")
            if text and text.strip():
                return text.strip()
        except Exception:
            pass

        # Graceful fallback: return empty string or metadata text if available
        # This ensures the pipeline never crashes even on systems without tesseract binaries
        return ""

    def process_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        End-to-end image processing:
        1. QR code decode & analysis
        2. Image preprocessing & OCR text extraction
        3. Structured entity parsing (URLs, phones, VPAs, amounts, keywords)
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            return {
                "success": False,
                "error": f"Invalid image format: {str(e)}",
                "extracted_text": "",
                "qr_analysis": None,
                "entities": {}
            }

        # 1. Decode QR code if present
        qr_payload = qr_scanner.decode_qr(image)
        qr_analysis = qr_scanner.analyze_qr_payload(qr_payload) if qr_payload else None

        # 2. Extract OCR text
        ocr_text = self.extract_text_with_ocr(image)

        # Combine text from QR and OCR
        full_text_parts = []
        if qr_payload:
            full_text_parts.append(f"QR_PAYLOAD: {qr_payload}")
        if ocr_text:
            full_text_parts.append(ocr_text)
        
        combined_text = "\n".join(full_text_parts)

        # 3. Extract entities
        urls = url_scanner.extract_urls(combined_text)
        phones = list(set(PHONE_REGEX.findall(combined_text)))
        vpas = list(set(UPI_VPA_REGEX.findall(combined_text)))
        amounts = AMOUNT_REGEX.findall(combined_text)
        matched_keywords = [kw for kw in KEYWORDS if kw in combined_text.lower()]

        entities = {
            "urls": urls,
            "phone_numbers": phones,
            "upi_vpas": vpas,
            "amounts": amounts,
            "keywords": matched_keywords
        }

        return {
            "success": True,
            "has_qr": qr_analysis["has_qr"] if qr_analysis else False,
            "qr_analysis": qr_analysis,
            "ocr_text": ocr_text,
            "combined_text": combined_text,
            "entities": entities
        }

ocr_pipeline = OCRPipeline()
