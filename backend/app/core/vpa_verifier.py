import re
from typing import Dict, Any, List, Optional
try:
    from ..models.schemas import VpaAnalysisResponse
except (ImportError, ValueError):
    from backend.app.models.schemas import VpaAnalysisResponse

# Verified UPI PSP Handles
PSP_HANDLES = {
    "okhdfcbank": "Google Pay (HDFC Bank)",
    "okaxis": "Google Pay (Axis Bank)",
    "okicici": "Google Pay (ICICI Bank)",
    "oksbi": "Google Pay (State Bank of India)",
    "ybl": "PhonePe (Yes Bank)",
    "ibl": "PhonePe (ICICI Bank)",
    "axl": "PhonePe (Axis Bank)",
    "paytm": "Paytm Payments Bank",
    "upi": "BHIM / NPCI Official",
    "sbi": "SBI YONO / BHIM SBI",
    "icici": "iMobile (ICICI Bank)",
    "hdfcbank": "HDFC Bank MobileBanking",
    "axisbank": "Axis Mobile",
    "kotak": "Kotak 811",
    "pnb": "PNB ONE",
    "barodampay": "Bank of Baroda",
    "aubank": "AU Small Finance Bank",
    "federal": "FedMobile",
    "indus": "IndusInd Bank",
    "airtel": "Airtel Payments Bank",
    "jio": "Jio Payments Bank"
}

# Suspicious keywords in consumer handles that impersonate institutions
SUSPICIOUS_HANDLE_PREFIXES = [
    "sbi", "hdfc", "icici", "axis", "pnb", "rbi", "cybercrime", "police",
    "refund", "cashback", "customer", "care", "support", "helpline", "lottery",
    "kbc", "electricity", "bescom", "uppcl", "tsspdcl", "customs", "delivery"
]

class VpaVerifier:
    """
    Validates UPI VPAs, detects institutional impersonation in consumer handles,
    and analyzes collect request risk.
    """

    def analyze(
        self,
        vpa: str,
        payee_name: Optional[str] = "",
        amount: Optional[float] = None,
        is_collect: bool = False
    ) -> VpaAnalysisResponse:
        vpa_clean = vpa.strip().lower()
        parts = vpa_clean.split("@")

        reasons = []
        risk_score = 0

        # 1. Format check
        is_valid_format = bool(re.match(r'^[a-zA-Z0-9.\-_]{2,}@[a-zA-Z0-9.\-_]{2,}$', vpa_clean))
        if not is_valid_format:
            return VpaAnalysisResponse(
                vpa=vpa,
                handle="",
                provider="Invalid",
                is_valid_format=False,
                is_collect_request=is_collect,
                risk_score=90,
                verdict="HIGH RISK",
                reasons=["Malformed UPI ID: Does not conform to standard username@handle format."],
                warning_notice="This UPI ID is malformed and cannot be safely verified."
            )

        username = parts[0]
        handle = parts[1]
        provider = PSP_HANDLES.get(handle, f"Third-Party Bank Handle (@{handle})")

        # 2. Collect Request Trap Check
        if is_collect:
            risk_score += 65
            reasons.append("Collect Request Alert: You are being asked to authorize an outgoing payment or debit mandate.")
            reasons.append("Crucial Security Rule: In UPI architecture, receiving money NEVER requires you to accept a collect request or enter a PIN.")

        # 3. Institutional Impersonation Check in Username
        # e.g., 'sbi-refund@paytm' or 'electricity-officer@ybl'
        matched_impersonations = [kw for kw in SUSPICIOUS_HANDLE_PREFIXES if kw in username]
        is_retail_psp = handle in ["paytm", "ybl", "ibl", "axl", "okhdfcbank", "okaxis", "okicici", "oksbi"]
        
        if matched_impersonations and is_retail_psp:
            risk_score += 50
            reasons.append(
                f"Institutional Brand Impersonation: UPI ID username contains '{matched_impersonations[0]}', "
                f"but is hosted on a retail consumer handle (@{handle}). Legitimate institutions use verified corporate merchant IDs."
            )

        # 4. Payee Name & VPA Mismatch
        if payee_name:
            clean_name = payee_name.lower().strip()
            # If name claims to be "SBI Customer Care" but VPA username is a personal phone number or random string
            if any(kw in clean_name for kw in ["sbi", "hdfc", "bank", "electricity", "support", "refund"]) and is_retail_psp:
                risk_score += 40
                reasons.append(
                    f"Payee Identity Mismatch: Display name '{payee_name}' claims to be an official service, "
                    f"but payment routes to personal handle '{vpa}'."
                )

        # 5. High-Value Alert
        if amount and amount >= 25000.0:
            risk_score += 15
            reasons.append(f"High-Value Transaction: Amount of Rs. {amount:,.2f} exceeds standard peer-to-peer threshold.")

        # Determine Verdict
        capped_score = max(0, min(100, risk_score))
        if capped_score <= 34:
            verdict = "SAFE"
            warning_notice = "UPI ID format is valid and routes to a standard PSP provider. Verify payee name before approving."
        elif capped_score <= 69:
            verdict = "SUSPICIOUS"
            warning_notice = "Caution: Anomalies detected in payment request. Confirm payee identity independently."
        else:
            verdict = "HIGH RISK"
            warning_notice = "CRITICAL WARNING: High probability of digital payment fraud. Do NOT enter your UPI PIN."

        if not reasons:
            reasons.append(f"Valid UPI handle registered with {provider}.")

        return VpaAnalysisResponse(
            vpa=vpa,
            handle=handle,
            provider=provider,
            is_valid_format=True,
            is_collect_request=is_collect,
            risk_score=capped_score,
            verdict=verdict,
            reasons=reasons,
            warning_notice=warning_notice
        )

vpa_verifier = VpaVerifier()
