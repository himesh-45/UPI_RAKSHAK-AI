import pytest
from playwright.sync_api import sync_playwright

FRONTEND_URL = "http://127.0.0.1:5173"

def test_playwright_full_demo_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        page.on("console", lambda msg: print(f"[CONSOLE {msg.type}] {msg.text}"))

        # 1. Navigate to Frontend
        page.goto(FRONTEND_URL, wait_until="networkidle", timeout=15000)
        assert "UPI Rakshak" in page.title()

        # 2. Verify Hero Header
        hero_heading = page.locator("h1")
        assert hero_heading.is_visible()

        # 3. Enter a realistic scam message in the text area
        text_area = page.locator("textarea").first
        assert text_area.is_visible()
        text_area.fill("URGENT: Your SBI account is suspended! Update KYC immediately at http://sbi.co.in.fake-kyc.com or call 9876543210")

        # 4. Trigger Analysis
        analyze_btn = page.locator("button:has-text('Analyze Threat')").first
        if not analyze_btn.is_visible():
            analyze_btn = page.locator("button:has-text('खतरे की जांच करें')").first
        
        analyze_btn.click()

        # 5. Wait for Safety Report Card to appear
        page.wait_for_selector("text=Risk Score", timeout=10000)
        assert page.locator("text=Risk Score").first.is_visible()

        # 6. Verify Explainability Modules are present
        assert page.locator("text=Dial 1930").first.is_visible()

        # 7. Test Language Switcher
        hindi_btn = page.locator("button:has-text('हिंदी')").first
        if hindi_btn.is_visible():
            hindi_btn.click()
            page.wait_for_timeout(400)
            assert page.locator("text=धोखाधड़ी").first.is_visible() or page.locator("text=विश्लेषक").first.is_visible()

        browser.close()
