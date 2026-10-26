
"""
Tests for SMS OTP newline support (WebOTP API compliance).
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_default_template_has_newline():
    """Default template should contain at least one newline for WebOTP."""
    response = client.get("/api/auth/sms/otp/template")
    assert response.status_code == 200
    data = response.json()
    assert '\n' in data["template"] or '\r\n' in data["template"]

def test_template_accepts_literal_newlines():
    """Template should accept literal newlines in the template string."""
    template_text = "Your code is: {{code}}\n\nPlease verify."
    response = client.post("/api/auth/sms/otp/template", json={"template": template_text})
    assert response.status_code == 200
    data = response.json()
    assert data["template"] == template_text

def test_template_accepts_actual_newlines_from_json():
    """Template should accept newlines (which JSON \\n becomes)."""
    # In JSON, \\n becomes actual newline, so this tests that newlines are accepted
    template_text = "Code: {{code}}\n\nExpires in 5 min."
    response = client.post("/api/auth/sms/otp/template", json={"template": template_text})
    assert response.status_code == 200
    data = response.json()
    assert '\n' in data["template"]
    assert data["template"].count('\n') >= 2

def test_template_rejects_no_newline():
    """Template without newline should be rejected (WebOTP requirement)."""
    template_text = "Code: {{code}} No newline here."
    response = client.post("/api/auth/sms/otp/template", json={"template": template_text})
    assert response.status_code == 422  # Validation error

def test_template_requires_code_placeholder():
    """Template must contain {{code}} placeholder."""
    template_text = "No placeholder here\n"
    response = client.post("/api/auth/sms/otp/template", json={"template": template_text})
    assert response.status_code == 422

def test_send_otp_preserves_newlines():
    """Sending OTP should preserve newlines in rendered message."""
    template_text = "Verify: {{code}}\n\nExpires soon."
    client.post("/api/auth/sms/otp/template", json={"template": template_text})
    response = client.post("/api/auth/sms/otp/send", json={"phone": "+15551234567"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "WebOTP compliant: True" in data["message"]

def test_multiple_newlines_accepted():
    """Multiple newlines should be accepted."""
    template_text = "Code: {{code}}\n\n\n\nExpires soon."
    response = client.post("/api/auth/sms/otp/template", json={"template": template_text})
    assert response.status_code == 200
    data = response.json()
    assert data["template"].count('\n') >= 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
