from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class PasteData(BaseModel):
    text: str

SECRET_PATTERNS = {
    "OpenAI API Key": r"sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}",
    "Anthropic API Key": r"sk-ant-[A-Za-z0-9_-]{40,}",
    "Google Cloud / Gemini API Key": r"AIza[0-9A-Za-z\-_]{35}",
    "GitHub Personal Access Token": r"gh[pousr]_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}",
    "AWS Access Key": r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
    "Stripe Secret Key": r"[sr]k_live_[0-9a-zA-Z]{24}",
    "Slack Token": r"xox[pbOa]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}",
    "HuggingFace Token": r"hf_[a-zA-Z]{34}",
    "Discord Bot Token": r"M[A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}",
    "JSON Web Token (JWT)": r"eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]{43,}",
    "RSA Private Key": r"-----BEGIN RSA PRIVATE KEY-----",
    "Generic Private Key": r"-----BEGIN PRIVATE KEY-----"
}

@app.post("/scan")
async def scan_clipboard(data: PasteData):
    redacted_text = data.text
    was_redacted = False
    detected_keys = []
    
    # Check text against all patterns and replace the exact matches
    for platform, pattern in SECRET_PATTERNS.items():
        if re.search(pattern, redacted_text):
            was_redacted = True
            detected_keys.append(platform)
            # Replace the actual key with a placeholder text
            redacted_text = re.sub(pattern, f"[*** HIDDEN {platform} ***]", redacted_text)
            
    return {
        "sanitized_text": redacted_text, 
        "was_redacted": was_redacted, 
        "detected": detected_keys
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)