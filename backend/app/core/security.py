import time
import html
from collections import defaultdict
from fastapi import Request, HTTPException, status

# In-memory IP rate limiter: max_requests per window_seconds
RATE_LIMIT_STORE = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 60
WINDOW_SECONDS = 60

def rate_limiter(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    
    # Filter out timestamps older than the window
    timestamps = RATE_LIMIT_STORE[client_ip]
    valid_timestamps = [ts for ts in timestamps if now - ts < WINDOW_SECONDS]
    
    if len(valid_timestamps) >= MAX_REQUESTS_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please wait before submitting more requests."
        )
    
    valid_timestamps.append(now)
    RATE_LIMIT_STORE[client_ip] = valid_timestamps

def sanitize_text(text: str) -> str:
    """
    Sanitizes string inputs to prevent XSS and control character injection.
    """
    if not text:
        return ""
    # Strip null bytes and non-printable characters except newline/tab
    cleaned = "".join(ch for ch in text if ch.isprintable() or ch in "\n\r\t")
    # HTML escape
    return html.escape(cleaned.strip())

# Allowed MIME types and max size for uploaded screenshots/QR
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
