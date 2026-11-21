import os
import pytest
from PIL import Image
from backend.app.detectors.qr_scanner import qr_scanner
from backend.app.detectors.ocr_pipeline import ocr_pipeline

@pytest.fixture
def demo_assets_dir():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "app", "data", "demo_assets")

def test_qr_decode_and_analyze_fake_cashback(demo_assets_dir):
    qr_path = os.path.join(demo_assets_dir, "qr_fake_cashback.png")
    assert os.path.exists(qr_path)
    
    with open(qr_path, "rb") as f:
        img_bytes = f.read()

    decoded = qr_scanner.decode_qr(img_bytes)
    assert decoded is not None
    assert decoded.startswith("upi://pay")

    analysis = qr_scanner.analyze_qr_payload(decoded)
    assert analysis["has_qr"] is True
    assert analysis["qr_score"] >= 70.0
    assert analysis["upi_details"]["pa"] == "scammer891@okhdfcbank"
    assert "Cashback" in analysis["upi_details"]["pn"]
    assert any("Payee Name & VPA Mismatch" in s["signal"] for s in analysis["signals"])
    assert any("Deceptive QR Payment Lure" in s["signal"] for s in analysis["signals"])

def test_qr_decode_electricity_scam(demo_assets_dir):
    qr_path = os.path.join(demo_assets_dir, "qr_electricity_scam.png")
    assert os.path.exists(qr_path)

    with open(qr_path, "rb") as f:
        img_bytes = f.read()

    decoded = qr_scanner.decode_qr(img_bytes)
    assert decoded is not None

    analysis = qr_scanner.analyze_qr_payload(decoded)
    assert analysis["has_qr"] is True
    assert analysis["qr_score"] >= 45.0
    assert any("Pre-filled High Payment Amount" in s["signal"] for s in analysis["signals"])

def test_qr_decode_safe_merchant(demo_assets_dir):
    qr_path = os.path.join(demo_assets_dir, "qr_safe_merchant.png")
    assert os.path.exists(qr_path)

    with open(qr_path, "rb") as f:
        img_bytes = f.read()

    decoded = qr_scanner.decode_qr(img_bytes)
    assert decoded is not None

    analysis = qr_scanner.analyze_qr_payload(decoded)
    assert analysis["has_qr"] is True
    assert analysis["qr_score"] == 0.0
    assert len(analysis["signals"]) == 0

def test_ocr_pipeline_end_to_end(demo_assets_dir):
    qr_path = os.path.join(demo_assets_dir, "qr_fake_cashback.png")
    with open(qr_path, "rb") as f:
        img_bytes = f.read()

    result = ocr_pipeline.process_image(img_bytes)
    assert result["success"] is True
    assert result["has_qr"] is True
    assert result["qr_analysis"]["qr_score"] >= 70.0
    assert len(result["entities"]["upi_vpas"]) >= 1

def test_ocr_pipeline_on_screenshot(demo_assets_dir):
    screenshot_path = os.path.join(demo_assets_dir, "screenshot_sbi_kyc.png")
    assert os.path.exists(screenshot_path)
    
    with open(screenshot_path, "rb") as f:
        img_bytes = f.read()

    result = ocr_pipeline.process_image(img_bytes)
    assert result["success"] is True
    # Graceful: OCR text extracted or empty without throwing exception
    assert isinstance(result["ocr_text"], str)
