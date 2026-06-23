import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest

from app.services.linkedin_service import get_linkedin_summary
from app.services.facebook_service import get_facebook_summary
from app.services.instagram_service import (
    get_instagram_posts,
    get_instagram_summary,
    get_instagram_insights
)

# =========================================
# INIT
# =========================================

load_dotenv()
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = FastAPI()

# =========================================
# GOOGLE CONFIG
# =========================================

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
CLIENT_SECRETS_FILE = "credentials/oauth_client.json"

creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri="http://127.0.0.1:8000/auth/callback"
)

# =========================================
# HOME
# =========================================

@app.get("/")
def home():
    return {"message": "MCP Server Running"}

# =========================================
# GOOGLE LOGIN
# =========================================

@app.get("/login")
def login():
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    return RedirectResponse(auth_url)

# =========================================
# GOOGLE CALLBACK
# =========================================

@app.get("/auth/callback")
def auth_callback(request: Request):
    global creds

    code = request.query_params.get("code")

    flow.fetch_token(code=code)
    creds = flow.credentials

    with open("token.json", "w") as token:
        token.write(creds.to_json())

    analytics = build("analyticsadmin", "v1beta", credentials=creds)
    accounts = analytics.accounts().list().execute()

    return accounts

# =========================================
# LINKEDIN LOGIN
# =========================================

@app.get("/login/linkedin")
def login_linkedin():
    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={os.getenv('LINKEDIN_CLIENT_ID')}"
        f"&redirect_uri={os.getenv('LINKEDIN_REDIRECT_URI')}"
        f"&scope=profile%20email"
    )

    return {"auth_url": auth_url}

# =========================================
# LINKEDIN CALLBACK
# =========================================

@app.get("/auth/linkedin/callback")
async def linkedin_callback(request: Request):
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    if error:
        return {"error": error}

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": os.getenv("LINKEDIN_CLIENT_ID"),
        "client_secret": os.getenv("LINKEDIN_CLIENT_SECRET"),
        "redirect_uri": os.getenv("LINKEDIN_REDIRECT_URI"),
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code != 200:
        return {
            "error": "LinkedIn token exchange failed",
            "details": response.text
        }

    token_data = response.json()

    if "access_token" in token_data:
        with open("linkedin_token.json", "w") as f:
            json.dump(token_data, f, indent=2)

    return {
        "message": "LinkedIn login successful",
        "token_data": token_data
    }

# =========================================
# LINKEDIN FOLLOWERS (REAL API)
# =========================================

@app.get("/linkedin/followers")
def linkedin_followers():

    if not os.path.exists("linkedin_token.json"):
        return {"error": "LinkedIn token not found. Login first."}

    with open("linkedin_token.json", "r") as f:
        token_data = json.load(f)

    access_token = token_data.get("access_token")

    org_id = "134734258"

    url = "https://api.linkedin.com/v2/organizationalEntityFollowerStatistics"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    params = {
        "q": "organizationalEntity",
        "organizationalEntity": f"urn:li:organization:{org_id}"
    }

    response = requests.get(url, headers=headers, params=params)

    try:
        return {
            "status_code": response.status_code,
            "data": response.json()
        }
    except Exception:
        return {
            "status_code": response.status_code,
            "raw": response.text
        }

# =========================================
# LINKEDIN SUMMARY
# =========================================

@app.get("/linkedin-summary")
@app.post("/linkedin-summary")
def linkedin_summary():
    return get_linkedin_summary()

# =========================================
# FACEBOOK
# =========================================

@app.get("/facebook-summary")
@app.post("/facebook-summary")
def facebook_summary():
    return get_facebook_summary()

# =========================================
# INSTAGRAM
# =========================================

@app.get("/instagram-posts")
@app.post("/instagram-posts")
def instagram_posts():
    return get_instagram_posts()

@app.get("/instagram-summary")
@app.post("/instagram-summary")
def instagram_summary():
    return get_instagram_summary()

@app.get("/instagram-insights")
@app.post("/instagram-insights")
def instagram_insights():
    return get_instagram_insights()

# =========================================
# GOOGLE ANALYTICS
# =========================================

@app.get("/insights")
def get_insights(property_id: str):

    global creds
    if creds is None:
        return {"error": "Login first"}

    client = BetaAnalyticsDataClient(credentials=creds)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[{"name": "date"}],
        metrics=[
            {"name": "activeUsers"},
            {"name": "newUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"}
        ],
        date_ranges=[{"start_date": "7daysAgo", "end_date": "today"}]
    )

    response = client.run_report(request)

    data = []

    for row in response.rows:
        raw_date = row.dimension_values[0].value

        formatted_date = datetime.strptime(
            raw_date,
            "%Y%m%d"
        ).strftime("%d %b %Y")

        data.append({
            "date": formatted_date,
            "activeUsers": row.metric_values[0].value,
            "newUsers": row.metric_values[1].value,
            "sessions": row.metric_values[2].value,
            "pageViews": row.metric_values[3].value
        })

    return data