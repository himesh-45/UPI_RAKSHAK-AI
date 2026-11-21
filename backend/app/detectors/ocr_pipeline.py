import io
import re
from typing import Dict, Any, List, Optional
import cv2
import numpy as np
from PIL import Image
import pytesseract
from .url_scanner import url_scanner
from .qr_scanner import qr_scanner

# Try importing RapidOCR fallback
RAPID_OCR_AVAILABLE = False
_rapid_ocr_instance = None
try:
    from rapidocr_onnxruntime import RapidOCR
    _rapid_ocr_instance = RapidOCR()
    RAPID_OCR_AVAILABLE = True
except Exception:
    RAPID_OCR_AVAILABLE = False

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
    Multilingual Image & QR OCR Pipeline.
    Supports Tesseract (eng+hin+tel) and RapidOCR ONNX fallback.
    Strictly HONEST: Never fabricates OCR results if no engine is available.
    """

    def __init__(self):
        self._tesseract_available = self._check_tesseract()

    def _check_tesseract(self) -> bool:
        try:
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False

    @property
    def active_engine(self) -> str:
        if self._tesseract_available:
            return "tesseract"
        if RAPID_OCR_AVAILABLE and _rapid_ocr_instance is not None:
            return "rapidocr"
        return "none"

    @property
    def is_ocr_available(self) -> bool:
        return self.active_engine != "none"

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        # Convert PIL to BGR OpenCV format
        cv_img = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        thresh = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        return thresh

    def extract_text_with_ocr(self, image: Image.Image) -> tuple[str, str]:
        """
        Extracts text using available real OCR engine.
        Returns: (extracted_text, engine_used)
        Never fabricates results.
        """
        # 1. Try Tesseract if binary is installed
        if self._tesseract_available:
            try:
                text = pytesseract.image_to_string(image, lang="eng+hin+tel")
                if text and text.strip():
                    return text.strip(), "tesseract"
            except Exception:
                pass

            try:
                text = pytesseract.image_to_string(image, lang="eng")
                if text and text.strip():
                    return text.strip(), "tesseract"
            except Exception:
                pass

        # 2. Try RapidOCR fallback
        if RAPID_OCR_AVAILABLE and _rapid_ocr_instance is not None:
            try:
                rgb_arr = np.array(image.convert("RGB"))
                ocr_results, _ = _rapid_ocr_instance(rgb_arr)
                if ocr_results:
                    lines = [res[1] for res in ocr_results if res and len(res) > 1 and res[1]]
                    text = "\n".join(lines).strip()
                    if text:
                        return text, "rapidocr"
            except Exception as e:
                print(f"[RapidOCR Error] {e}")

        return "", "none"

    def process_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        End-to-end image processing:
        1. QR code decode & analysis
        2. Real OCR text extraction (or honest notice if unavailable)
        3. Structured entity parsing
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            return {
                "success": False,
                "error": f"Invalid image format: {str(e)}",
                "extracted_text": "",
                "ocr_available": self.is_ocr_available,
                "ocr_engine": self.active_engine,
                "qr_analysis": None,
                "entities": {}
            }

        # 1. Decode QR code if present
        qr_payload = qr_scanner.decode_qr(image)
        qr_analysis = qr_scanner.analyze_qr_payload(qr_payload) if qr_payload else None

        # 2. Extract OCR text via real engine
        ocr_text, engine_used = self.extract_text_with_ocr(image)

        # Honest reporting
        ocr_status_message = None
        if not ocr_text and self.active_engine == "none":
            ocr_status_message = "OCR engine unavailable on host. Please paste message text directly or deploy via Docker."

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
            "ocr_available": self.is_ocr_available,
            "ocr_engine": engine_used if ocr_text else self.active_engine,
            "ocr_text": ocr_text,
            "ocr_status_message": ocr_status_message,
            "combined_text": combined_text,
            "entities": entities
        }

ocr_pipeline = OCRPipeline()
