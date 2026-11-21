import re

# Regex patterns for sensitive data
PHONE_REGEX = re.compile(r'(?<!\d)(?:\+91[-\s]?)?[6-9]\d{9}(?!\d)')
CARD_ACC_REGEX = re.compile(r'(?<!\d)\d{4}[-\s]?\d{4}[-\s]?\d{4}(?:[-\s]?\d{4})?(?!\d)')
OTP_PATTERNS = [
    re.compile(r'(?i)\b(?:otp|one[- ]time[- ]password|pin|code|verification code|secret)\s*(?:is|:|=|-)?\s*(\d{4,6})\b'),
    re.compile(r'\b(\d{4,6})\s*(?:is your (?:otp|pin|verification code|secret))\b', re.IGNORECASE)
]
UPI_VPA_REGEX = re.compile(r'\b([a-zA-Z0-9.\-_]{2,})@([a-zA-Z0-9.\-_]{2,})\b')

def mask_phone_number(match: re.Match) -> str:
    val = match.group(0).strip()
    # Keep last 3 digits, mask rest
    if len(val) >= 10:
        return val[:2] + "******" + val[-2:]
    return "[PHONE_REDACTED]"

def mask_card_acc(match: re.Match) -> str:
    val = match.group(0).strip()
    digits_only = re.sub(r'\D', '', val)
    if len(digits_only) >= 11:
        return "XXXX-XXXX-" + digits_only[-4:]
    return "[ACCOUNT_REDACTED]"

def mask_sensitive_data(text: str) -> str:
    """
    Sanitizes raw user input by masking phone numbers, bank accounts,
    credit/debit cards, OTPs, and private UPI IDs before persisting to DB.
    """
    if not text:
        return text

    masked = text

    # Mask OTP occurrences first
    for otp_regex in OTP_PATTERNS:
        def replace_otp(m):
            full_match = m.group(0)
            target_otp = m.group(1)
            return full_match.replace(target_otp, "[OTP_REDACTED]")
        masked = otp_regex.sub(replace_otp, masked)

    # Mask Card / Account numbers
    masked = CARD_ACC_REGEX.sub(mask_card_acc, masked)

    # Mask Phone numbers
    masked = PHONE_REGEX.sub(mask_phone_number, masked)

    return masked
