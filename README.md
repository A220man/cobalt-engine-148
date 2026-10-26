

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.

# Cobalt Engine - SMS OTP Service

A FastAPI-based SMS OTP service with WebOTP API compliance (newline support in templates).

## Features

- **SMS OTP Template Management**: Create and manage SMS templates with placeholder support
- **WebOTP API Compliance**: Templates must contain at least one newline character (`\n` or `\r\n`) to conform to the [WebOTP API specification](https://wicg.github.io/sms-one-time-codes/#origin-bound-one-time-code-message)
- **Newline Support**: Full support for literal newlines and escape sequences in templates
- **Validation**: Template validation ensures `{{code}}` placeholder and newline requirements

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/sms/otp/template` | Create/update SMS OTP template |
| GET | `/api/auth/sms/otp/template` | Get current SMS OTP template |
| POST | `/api/auth/sms/otp/send` | Send SMS OTP using template |
| GET | `/health` | Health check |

## Template Requirements

Templates must:
1. Contain the `{{code}}` placeholder (replaced with 6-digit OTP)
2. Contain at least one newline (`\n` or `\r\n`) for WebOTP API compliance

Example valid template:
```
Your verification code is: {{code}}

This code will expire in 10 minutes.
```

## Running the Service

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the server
python -m backend.main
```

Server runs on `http://localhost:8000`

## Running Tests

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run tests
python -m pytest tests/ -v
```

## WebOTP API Format

For WebOTP API to automatically fill OTP codes, the SMS message must follow this format:

```
<optional text>
<code>
<optional text>

@<origin> #<code>
```

The newline is required to separate the code from the origin-bound one-time code line. Our validation enforces at least one newline in the template.

Maintainer: Ryan Vo <ryandtvo@gmail.com>
