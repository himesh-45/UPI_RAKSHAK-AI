import re
import urllib.parse
from typing import Dict, Any, Optional, List
import cv2
import numpy as np
from PIL import Image
import io
from .url_scanner import url_scanner

INSTITUTIONAL_KEYWORDS = [
    "bank", "support", "care", "electricity", "bill", "official", "gov",
    "refund", "power", "helpdesk", "gpay", "google pay", "phonepe", "paytm", "reward", "cashback"
]
PERSONAL_PSP_HANDLES = ["@okhdfcbank", "@okaxis", "@okicici", "@oksbi", "@ybl", "@ibl", "@axl", "@paytm"]

class QRScanner:
    """
    Decodes QR codes without executing or visiting payloads.
    Parses UPI payment URIs (upi://pay) and flags payment anomalies.
    """

    def __init__(self):
        self.detector = cv2.QRCodeDetector()

    def decode_qr(self, image_input) -> Optional[str]:
        """
        Extracts QR code text using OpenCV QRCodeDetector.
        Supports PIL.Image, numpy ndarray, or raw bytes.
        """
        try:
            if isinstance(image_input, bytes):
                nparr = np.frombuffer(image_input, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            elif isinstance(image_input, Image.Image):
                rgb_img = image_input.convert("RGB")
                img = cv2.cvtColor(np.array(rgb_img, dtype=np.uint8), cv2.COLOR_RGB2BGR)
            elif isinstance(image_input, np.ndarray):
                if image_input.dtype == bool:
                    img = (image_input * 255).astype(np.uint8)
                    if len(img.shape) == 2:
                        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                else:
                    img = image_input
            else:
                return None

            if img is None:
                return None

            decoded_text, points, _ = self.detector.detectAndDecode(img)
            if decoded_text:
                return decoded_text.strip()
            
            # Try contrast enhancement if initial detect fails
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            decoded_text, _, _ = self.detector.detectAndDecode(enhanced)
            return decoded_text.strip() if decoded_text else None
        except Exception as e:
            print(f"[QRScanner Error] {e}")
            return None

    def parse_upi_uri(self, uri: str) -> Dict[str, Any]:
        """
        Parses upi://pay parameters: pa, pn, am, cu, tn, mc.
        """
        if not uri.lower().startswith("upi://pay"):
            return {
                "is_upi": False,
                "raw_uri": uri
            }

        # Parse query params
        parsed = urllib.parse.urlparse(uri)
        query_dict = urllib.parse.parse_qs(parsed.query)

        pa = query_dict.get("pa", [""])[0]  # Payee address / VPA
        pn = query_dict.get("pn", [""])[0]  # Payee name
        am = query_dict.get("am", [""])[0]  # Amount
        cu = query_dict.get("cu", ["INR"])[0] # Currency
        tn = query_dict.get("tn", [""])[0]  # Transaction note
        mc = query_dict.get("mc", [""])[0]  # Merchant code
        mode = query_dict.get("mode", [""])[0]

        return {
            "is_upi": True,
            "raw_uri": uri,
            "pa": pa,
            "pn": pn,
            "am": am,
            "cu": cu,
            "tn": tn,
            "mc": mc,
            "mode": mode
        }

    def analyze_qr_payload(self, payload: str) -> Dict[str, Any]:
        if not payload:
            return {
                "has_qr": False,
                "payload": "",
                "qr_score": 0.0,
                "signals": [],
                "upi_details": None
            }

        signals = []
        score = 0.0
        upi_details = None

        if payload.lower().startswith("upi://pay"):
            upi_details = self.parse_upi_uri(payload)
            pa = upi_details["pa"]
            pn = upi_details["pn"]
            am = upi_details["am"]
            tn = upi_details["tn"]

            # Anomaly 1: Payee Name claims official entity but VPA is personal
            pn_lower = pn.lower()
            is_claiming_institution = any(kw in pn_lower for kw in INSTITUTIONAL_KEYWORDS)
            has_personal_handle = any(pa.lower().endswith(h) for h in PERSONAL_PSP_HANDLES)
            digits_in_pa = len(re.findall(r'\d', pa.split("@")[0])) if "@" in pa else 0

            if is_claiming_institution and (has_personal_handle or digits_in_pa >= 4):
                score += 45.0
                signals.append({
                    "signal": f"Payee Name & VPA Mismatch: QR claims payee name '{pn}', but destination VPA '{pa}' belongs to an unverified personal handle.",
                    "source_module": "QR_PARSER",
                    "weight": 45.0,
                    "severity": "CRITICAL"
                })

            # Anomaly 2: Deceptive transaction note ("refund", "cashback", "prize")
            tn_lower = tn.lower()
            deceptive_tn_words = ["refund", "cashback", "reward", "lottery", "prize", "kyc", "claim", "bonus", "unblock"]
            matched_deceptive = [w for w in deceptive_tn_words if w in tn_lower]
            if matched_deceptive:
                score += 50.0
                signals.append({
                    "signal": f"Deceptive QR Payment Lure: Note claims '{tn}'. Scanning a QR code ALWAYS sends money; you can NEVER receive refunds or cashback by scanning a QR.",
                    "source_module": "QR_PARSER",
                    "weight": 50.0,
                    "severity": "CRITICAL"
                })

            # Anomaly 3: High pre-filled amount
            if am:
                try:
                    amount_val = float(am)
                    if amount_val >= 2000.0:
                        score += 30.0
                        signals.append({
                            "signal": f"Pre-filled High Payment Amount: QR code pre-authorizes Rs. {amount_val:,.2f} transfer.",
                            "source_module": "QR_PARSER",
                            "weight": 30.0,
                            "severity": "HIGH"
                        })
                except ValueError:
                    pass

        elif re.match(r'(?i)^https?://', payload):
            # QR contains a URL: run through static URL scanner
            url_res = url_scanner.analyze_url(payload)
            score = url_res["url_score"]
            signals = [
                {
                    "signal": f"QR Code Encodes URL: {s['signal']}",
                    "source_module": "QR_PARSER",
                    "weight": s["weight"],
                    "severity": s["severity"]
                }
                for s in url_res["signals"]
            ]
        else:
            # Generic text payload
            if any(kw in payload.lower() for kw in ["pin", "otp", "blocked", "kyc"]):
                score += 30.0
                signals.append({
                    "signal": f"Suspicious QR Text Content: QR contains text referencing payment credentials or blocks: '{payload[:60]}...'",
                    "source_module": "QR_PARSER",
                    "weight": 30.0,
                    "severity": "MEDIUM"
                })

        capped_score = max(0.0, min(100.0, score))

        return {
            "has_qr": True,
            "payload": payload,
            "qr_score": capped_score,
            "signals": signals,
            "upi_details": upi_details
        }

qr_scanner = QRScanner()
