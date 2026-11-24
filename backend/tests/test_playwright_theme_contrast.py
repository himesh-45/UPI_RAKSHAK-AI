import os
import math
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import pytest
from playwright.sync_api import sync_playwright

def parse_rgb(rgb_str):
    nums = [float(x.strip()) for x in rgb_str.replace('rgba', '').replace('rgb', '').replace('(', '').replace(')', '').split(',')[:3]]
    return nums[0], nums[1], nums[2]

def srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else math.pow((c + 0.055) / 1.055, 2.4)

def relative_luminance(rgb):
    r, g, b = rgb
    return 0.2126 * srgb_to_linear(r) + 0.7152 * srgb_to_linear(g) + 0.0722 * srgb_to_linear(b)

def contrast_ratio(rgb1, rgb2):
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

class SpaHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.abspath("frontend/dist"), **kwargs)

    def do_GET(self):
        path = self.translate_path(self.path)
        if not os.path.exists(path):
            self.path = '/index.html'
        return super().do_GET()

def test_theme_wcag_contrast_and_elements():
    """Verify dark and light theme WCAG AA contrast compliance and instant theme toggling."""
    dist_dir = os.path.abspath("frontend/dist")
    if not os.path.exists(dist_dir):
        pytest.skip("frontend/dist does not exist. Run npm run build first.")

    port = 5188
    server = HTTPServer(('127.0.0.1', port), SpaHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1440, "height": 900})
            page = context.new_page()

            page.goto(f"http://127.0.0.1:{port}/", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(300)

            # 1. Dark Mode Contrast Check
            h1 = page.locator("h1")
            assert h1.is_visible()
            body_bg_dark = page.evaluate("window.getComputedStyle(document.body).backgroundColor")
            h1_color_dark = page.evaluate("window.getComputedStyle(document.querySelector('h1')).color")
            sub_color_dark = page.evaluate("window.getComputedStyle(document.querySelector('h1 + p')).color")

            ratio_h1_dark = contrast_ratio(parse_rgb(h1_color_dark), parse_rgb(body_bg_dark))
            ratio_sub_dark = contrast_ratio(parse_rgb(sub_color_dark), parse_rgb(body_bg_dark))

            assert ratio_h1_dark >= 3.0, f"Dark H1 contrast {ratio_h1_dark:.2f} failed 3.0:1 requirement"
            assert ratio_sub_dark >= 4.5, f"Dark Subtitle contrast {ratio_sub_dark:.2f} failed 4.5:1 requirement"

            # 2. Check Theme Toggle Button is present and functional
            toggle_btn = page.locator("button[aria-label*='mode']").first
            assert toggle_btn.is_visible(), "Theme toggle button must be present in Navbar"

            # Toggle to Light Mode
            toggle_btn.click()
            page.wait_for_timeout(300)

            # Ensure document now has 'light' class
            has_light = page.evaluate("document.documentElement.classList.contains('light')")
            assert has_light, "Document element should have class 'light' after toggling"

            body_bg_light = page.evaluate("window.getComputedStyle(document.body).backgroundColor")
            h1_color_light = page.evaluate("window.getComputedStyle(document.querySelector('h1')).color")
            sub_color_light = page.evaluate("window.getComputedStyle(document.querySelector('h1 + p')).color")

            ratio_h1_light = contrast_ratio(parse_rgb(h1_color_light), parse_rgb(body_bg_light))
            ratio_sub_light = contrast_ratio(parse_rgb(sub_color_light), parse_rgb(body_bg_light))

            assert ratio_h1_light >= 3.0, f"Light H1 contrast {ratio_h1_light:.2f} failed 3.0:1 requirement"
            assert ratio_sub_light >= 4.5, f"Light Subtitle contrast {ratio_sub_light:.2f} failed 4.5:1 requirement"

            # 3. Toggle back to Dark Mode
            toggle_btn.click()
            page.wait_for_timeout(300)
            has_dark = page.evaluate("document.documentElement.classList.contains('dark')")
            assert has_dark, "Document element should return to class 'dark'"

            # 4. Check idle gauge state
            assert page.locator("text=Waiting for input").first.is_visible()
            assert page.locator("text=--").first.is_visible()

            # 5. Check hero CTA buttons
            assert page.locator("button:has-text('Check a message')").is_visible()
            assert page.locator("button:has-text('How accurate is this?')").is_visible()
            assert page.locator("div.pt-2 >> text=Why Not Just Use an LLM?").count() == 0

            # 6. Check factual coverage list
            assert page.locator("text=Multilingual NLP classifier").first.is_visible()
            assert page.locator("text=7 Engines Active").count() == 0

            context.close()
            browser.close()
    finally:
        server.shutdown()
