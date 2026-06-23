import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")

CODE = "AQRNFRAC8kNRDTSMKEBeiqg9em72mkf7qbntdURQ20dmGf6HK04L30kHaH_2_HzXpPGgX-38ehuq8itT555X4MfvB64D8KN0OBVnbbmKiA_UWyFAes9BybIL6fjfBxypjXilGLsZIgvVd51Prh7pVP65Ymv9DBa43f_mgSmXa1BnqB4Yj-qVy2FNjtOrGZDcYOZHGcpz5poQEs52U7s"

url = "https://www.linkedin.com/oauth/v2/accessToken"

data = {
    "grant_type": "authorization_code",
    "code": CODE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=data, headers=headers)

print("STATUS:", response.status_code)
print(response.json())