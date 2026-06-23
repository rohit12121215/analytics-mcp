import os
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")

# ⚠️ IMPORTANT: remove openid for now
SCOPES = quote("profile email")

auth_url = (
    "https://www.linkedin.com/oauth/v2/authorization"
    f"?response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri={quote(REDIRECT_URI, safe='')}"
    f"&scope={SCOPES}"
)

print("\nAUTH URL:\n")
print(auth_url)