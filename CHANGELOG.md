# Changelog

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.2.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.1.0 — 2026-11-05

### Added
- **SMS OTP newline support for WebOTP API compliance** (`sms-otp-newlines`)
  - Template validation now accepts literal newlines (`\n`) and `\r\n` sequences
  - Templates must contain at least one newline to conform to WebOTP specification
  - New endpoints: `POST /api/auth/sms/otp/template`, `GET /api/auth/sms/otp/template`, `POST /api/auth/sms/otp/send`
  - Default template includes newlines and `{{code}}` placeholder
  - 7 comprehensive tests covering template validation, newline handling, and OTP sending

### Fixed
- N/A (first feature implementation)

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.
