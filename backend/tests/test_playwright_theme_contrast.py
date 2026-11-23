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
    """Verify light and dark theme contrast compliance and key element visibility."""
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

            for theme in ['light', 'dark']:
                context = browser.new_context(viewport={"width": 1440, "height": 900})
                page = context.new_page()

                page.add_init_script(f"""
                    localStorage.setItem('theme', '{theme}');
                    document.documentElement.className = '{theme}';
                """)

                page.goto(f"http://127.0.0.1:{port}/", wait_until="networkidle", timeout=15000)

                # Ensure class set properly
                page.evaluate(f"""
                    if ('{theme}' === 'light') {{
                        document.documentElement.classList.remove('dark');
                        document.documentElement.classList.add('light');
                    }} else {{
                        document.documentElement.classList.remove('light');
                        document.documentElement.classList.add('dark');
                    }}
                """)
                page.wait_for_timeout(300)

                # 1. Headline visibility and contrast
                h1 = page.locator("h1")
                assert h1.is_visible()
                body_bg = page.evaluate("window.getComputedStyle(document.body).backgroundColor")
                h1_color = page.evaluate("window.getComputedStyle(document.querySelector('h1')).color")
                sub_color = page.evaluate("window.getComputedStyle(document.querySelector('h1 + p')).color")

                ratio_h1 = contrast_ratio(parse_rgb(h1_color), parse_rgb(body_bg))
                ratio_sub = contrast_ratio(parse_rgb(sub_color), parse_rgb(body_bg))

                assert ratio_h1 >= 3.0, f"{theme} H1 contrast {ratio_h1:.2f} failed 3.0:1 requirement"
                assert ratio_sub >= 4.5, f"{theme} Subtitle contrast {ratio_sub:.2f} failed 4.5:1 requirement"

                # 2. Check idle gauge state
                assert page.locator("text=Waiting for input").first.is_visible()
                assert page.locator("text=--").first.is_visible()

                # 3. Check hero CTA buttons
                assert page.locator("button:has-text('Check a message')").is_visible()
                assert page.locator("button:has-text('How accurate is this?')").is_visible()
                # Verify LLM button is NOT in hero
                assert page.locator("div.pt-2 >> text=Why Not Just Use an LLM?").count() == 0

                # 4. Check factual coverage list
                assert page.locator("text=Multilingual NLP classifier").first.is_visible()
                assert page.locator("text=7 Engines Active").count() == 0

                context.close()

            browser.close()
    finally:
        server.shutdown()
