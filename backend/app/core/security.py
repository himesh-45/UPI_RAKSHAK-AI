import time
import html
from collections import defaultdict
from fastapi import Request, HTTPException, status

# In-memory IP rate limiter with sliding window and automatic prune
RATE_LIMIT_STORE = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 60
WINDOW_SECONDS = 60
_LAST_CLEANUP = time.time()

def _get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

def rate_limiter(request: Request):
    global _LAST_CLEANUP
    client_ip = _get_client_ip(request)
    now = time.time()
    
    # Periodically prune stale IPs every 5 minutes to prevent memory leak
    if now - _LAST_CLEANUP > 300:
        stale_keys = [k for k, v in RATE_LIMIT_STORE.items() if not v or (now - v[-1] >= WINDOW_SECONDS)]
        for k in stale_keys:
            del RATE_LIMIT_STORE[k]
        _LAST_CLEANUP = now

    # Filter out timestamps older than the window
    timestamps = RATE_LIMIT_STORE[client_ip]
    valid_timestamps = [ts for ts in timestamps if now - ts < WINDOW_SECONDS]
    
    if len(valid_timestamps) >= MAX_REQUESTS_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please wait a minute before submitting more requests."
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

# Allowed MIME types and max size for uploaded screenshots/QR (5 MB maximum)
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
