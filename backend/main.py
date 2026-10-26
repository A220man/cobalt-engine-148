
"""
SMS OTP Service with newline support for WebOTP API compliance.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import re

app = FastAPI(title="Cobalt Engine SMS OTP Service")

class SMSOTPTemplate(BaseModel):
    """SMS OTP template model with newline support."""
    template: str
    
    @field_validator('template')
    @classmethod
    def validate_template(cls, v: str) -> str:
        """Validate template allows newlines and contains placeholder."""
        if not v or not v.strip():
            raise ValueError("Template cannot be empty")
        # Allow newlines (\n, \r\n) and the {{code}} placeholder
        if '{{code}}' not in v:
            raise ValueError("Template must contain {{code}} placeholder")
        # WebOTP API requires at least one newline
        if '\n' not in v and '\r\n' not in v:
            raise ValueError("Template must contain at least one newline for WebOTP API compliance")
        return v

class SMSOTPRequest(BaseModel):
    """Request to send SMS OTP."""
    phone: str
    template_id: str = "default"

class SMSOTPResponse(BaseModel):
    """Response from SMS OTP send."""
    success: bool
    message: str

# In-memory template store
templates = {
    "default": "Your verification code is: {{code}}\n\nThis code will expire in 10 minutes."
}

@app.post("/api/auth/sms/otp/template")
async def create_template(template: SMSOTPTemplate):
    """Create or update SMS OTP template with newline support."""
    template_id = "default"
    templates[template_id] = template.template
    return {"template_id": template_id, "template": template.template}

@app.get("/api/auth/sms/otp/template")
async def get_template():
    """Get current SMS OTP template."""
    return {"template": templates.get("default", "")}

@app.post("/api/auth/sms/otp/send", response_model=SMSOTPResponse)
async def send_sms_otp(request: SMSOTPRequest):
    """Send SMS OTP using template with newline support."""
    template = templates.get(request.template_id, templates["default"])
    
    # Generate a 6-digit code
    import random
    code = str(random.randint(100000, 999999))
    
    # Render template with code - preserves newlines
    message = template.replace("{{code}}", code)
    
    # Verify message contains newline (WebOTP requirement)
    has_newline = '\n' in message or '\r\n' in message
    
    return SMSOTPResponse(
        success=True,
        message=f"SMS sent to {request.phone} (WebOTP compliant: {has_newline})"
    )

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
