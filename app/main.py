from app.services.linkedin_service import get_linkedin_summary
import os
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest


# =========================================
# OAUTH SETTINGS
# =========================================

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = FastAPI()

SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly"
]

CLIENT_SECRETS_FILE = "credentials/oauth_client.json"


# =========================================
# GLOBAL CREDENTIALS
# =========================================

creds = None

# LOAD SAVED TOKEN
if os.path.exists("token.json"):

    creds = Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
    )


# =========================================
# GOOGLE OAUTH FLOW
# =========================================

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

    return {
        "message": "Google Analytics MCP Running"
    }


# =========================================
# LOGIN
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
# AUTH CALLBACK
# =========================================

@app.get("/auth/callback")
def auth_callback(request: Request):

    global creds

    code = request.query_params.get("code")

    flow.fetch_token(code=code)

    # SAVE CREDENTIALS
    creds = flow.credentials

    # SAVE TOKEN
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    analytics = build(
        "analyticsadmin",
        "v1beta",
        credentials=creds
    )

    accounts = analytics.accounts().list().execute()

    return accounts


# =========================================
# GET PROPERTIES
# =========================================

@app.get("/properties")
def get_properties():

    global creds

    if creds is None:

        return {
            "error": "Please login first at /login"
        }

    analytics = build(
        "analyticsadmin",
        "v1beta",
        credentials=creds
    )

    properties = analytics.properties().list(
        filter="parent:accounts/395276861"
    ).execute()

    return properties


# =========================================
# REAL GA4 INSIGHTS
# =========================================

@app.get("/insights")
def get_insights(property_id: str):

    global creds

    if creds is None:

        return {
            "error": "Please login first at /login"
        }

    client = BetaAnalyticsDataClient(
        credentials=creds
    )

    request = RunReportRequest(
        property=f"properties/{property_id}",

        dimensions=[
            {"name": "date"}
        ],

        metrics=[
            {"name": "activeUsers"},
            {"name": "newUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"}
        ],

        date_ranges=[
            {
                "start_date": "7daysAgo",
                "end_date": "today"
            }
        ]
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


# =========================================
# SUMMARY
# =========================================

@app.get("/summary")
def get_summary(property_id: str):

    global creds

    if creds is None:

        return {
            "error": "Please login first at /login"
        }

    client = BetaAnalyticsDataClient(
        credentials=creds
    )

    request = RunReportRequest(
        property=f"properties/{property_id}",

        metrics=[
            {"name": "activeUsers"},
            {"name": "newUsers"},
            {"name": "sessions"},
            {"name": "screenPageViews"}
        ],

        date_ranges=[
            {
                "start_date": "7daysAgo",
                "end_date": "today"
            }
        ]
    )

    response = client.run_report(request)

    row = response.rows[0]

    return {
        "totalActiveUsers": row.metric_values[0].value,
        "totalNewUsers": row.metric_values[1].value,
        "totalSessions": row.metric_values[2].value,
        "totalPageViews": row.metric_values[3].value
    }


# =========================================
# TRAFFIC SOURCES
# =========================================

@app.get("/traffic-sources")
def traffic_sources(property_id: str):

    global creds

    if creds is None:

        return {
            "error": "Please login first at /login"
        }

    client = BetaAnalyticsDataClient(
        credentials=creds
    )

    request = RunReportRequest(
        property=f"properties/{property_id}",

        dimensions=[
            {"name": "sessionDefaultChannelGroup"}
        ],

        metrics=[
            {"name": "sessions"},
            {"name": "activeUsers"}
        ],

        date_ranges=[
            {
                "start_date": "7daysAgo",
                "end_date": "today"
            }
        ]
    )

    response = client.run_report(request)

    data = []

    for row in response.rows:

        data.append({
            "channel": row.dimension_values[0].value,
            "sessions": row.metric_values[0].value,
            "activeUsers": row.metric_values[1].value
        })

    return data
# =========================================
# LINKEDIN SUMMARY
# =========================================
@app.get("/linkedin-summary")
@app.post("/linkedin-summary")
def linkedin_summary():
    return get_linkedin_summary()