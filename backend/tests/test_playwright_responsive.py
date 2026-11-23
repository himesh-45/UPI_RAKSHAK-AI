import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import pytest
from playwright.sync_api import sync_playwright

class SpaHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.abspath("frontend/dist"), **kwargs)

    def do_GET(self):
        path = self.translate_path(self.path)
        if not os.path.exists(path):
            self.path = '/index.html'
        return super().do_GET()

BREAKPOINTS = [
    {"name": "budget_phone", "width": 320, "height": 568},
    {"name": "common_android", "width": 360, "height": 740},
    {"name": "ipad_portrait", "width": 768, "height": 1024},
    {"name": "ipad_landscape", "width": 1024, "height": 768},
    {"name": "desktop_1440", "width": 1440, "height": 900},
    {"name": "desktop_4k", "width": 2560, "height": 1440},
]

def test_cross_device_viewports_no_overflow():
    dist_dir = os.path.abspath("frontend/dist")
    if not os.path.exists(dist_dir):
        pytest.skip("frontend/dist does not exist. Run npm run build first.")

    port = 5192
    server = HTTPServer(('127.0.0.1', port), SpaHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for bp in BREAKPOINTS:
                context = browser.new_context(viewport={"width": bp["width"], "height": bp["height"]})
                page = context.new_page()
                page.goto(f"http://127.0.0.1:{port}/", wait_until="networkidle", timeout=15000)
                page.wait_for_timeout(200)

                # 1. Verify zero horizontal overflow
                scroll_w = page.evaluate("() => document.documentElement.scrollWidth")
                inner_w = page.evaluate("() => window.innerWidth")
                assert scroll_w <= inner_w, f"Viewport {bp['name']} ({bp['width']}px) has horizontal overflow: scrollWidth {scroll_w} > innerWidth {inner_w}"

                # 2. Verify checker input is rendered and visible
                input_elem = page.locator("textarea, input[type='text'], input[type='url']").first
                assert input_elem.is_visible(), f"Checker input not visible at {bp['name']}"

                # 3. Verify interactive elements exist
                btn = page.locator("button:has-text('Check a message'), button:has-text('Analyze Threat')").first
                assert btn.is_visible()

                context.close()
            browser.close()
    finally:
        server.shutdown()
