# SafeC 🛡️

A browser extension that intercepts clipboard pastes and blocks sensitive API keys and credentials from being uploaded to chatbots (ChatGPT, Claude, etc.) and code repositories (GitHub, GitLab).

## How it Works
The frontend is a Chrome/Brave Manifest V3 extension that intercepts the `paste` event. It uses a background Service Worker to bypass Content Security Policies (CSP) and sends the clipboard text to a local Python FastAPI backend. The Python backend scans the text using Regex patterns for major API keys (AWS, OpenAI, Stripe, etc.) and blocks the paste if a secret is detected.

## Installation Instructions

### 1. Start the Python Backend
1. Clone this repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment.
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `python scanner.py`

### 2. Load the Extension
1. Open Chrome or Brave and navigate to `chrome://extensions/`.
2. Turn on **Developer mode** (top right).
3. Click **Load unpacked** and select the folder containing this code.
4. Try pasting a dummy API key (e.g., `AKIAIOSFODNN7EXAMPLE`) into a target site!