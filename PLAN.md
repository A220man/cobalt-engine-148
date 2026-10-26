# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

sms-otp-newlines

## Roadmap

### sms-otp-newlines — Allow newlines in SMS OTP template

Status: done

Acceptance:
- SMS OTP template accepts literal newlines or \n escape sequences
- Generated SMS contains at least one newline to conform to WebOTP API
- Template validation permits newline characters

Implementation: `backend/main.py`, `tests/test_sms_otp.py`

Tests: `tests/test_sms_otp.py`

