import os

from dotenv import load_dotenv

from google.analytics.data_v1beta import (
    BetaAnalyticsDataClient
)

from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Metric,
    Dimension
)

from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow

from google.auth.transport.requests import Request


load_dotenv()

GA4_PROPERTY_ID = os.getenv("GA4_PROPERTY_ID")

SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly"
]

TOKEN_FILE = "token.json"


def get_credentials():

    creds = None

    # Load existing token
    if os.path.exists(TOKEN_FILE):

        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    # If token invalid or missing
    if not creds or not creds.valid:

        # Refresh expired token
        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            # First-time login
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save token
        with open(TOKEN_FILE, "w") as token:

            token.write(creds.to_json())

    return creds

async def run_ga4_report(
    metrics: list,
    dimensions: list = None,
    days: int = 30
):

    creds = get_credentials()

    client = BetaAnalyticsDataClient(
        credentials=creds,
        transport="rest"
    )

    ga_dimensions = []

    if dimensions:

        ga_dimensions = [
            Dimension(name=d)
            for d in dimensions
        ]

    ga_metrics = [
        Metric(name=m)
        for m in metrics
    ]

    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",

        dimensions=ga_dimensions,

        metrics=ga_metrics,

        date_ranges=[
            DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )
        ]
    )

    response = client.run_report(request)

    results = []

    for row in response.rows:

        item = {}

        # dimensions
        for i, dimension in enumerate(dimensions or []):

            item[dimension] = row.dimension_values[i].value

        # metrics
        for i, metric in enumerate(metrics):

            item[metric] = row.metric_values[i].value

        results.append(item)

    return results


async def get_top_sources_service(days: int = 30):

    return await run_ga4_report(
        metrics=["sessions"],
        dimensions=["country"],
        days=days
    )

    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",

        dimensions=[
            Dimension(name="country")
        ],

        metrics=[
            Metric(name="sessions")
        ],

        date_ranges=[
            DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )
        ]
    )

    response = client.run_report(request)

    results = []

    for row in response.rows:

        results.append({
            "country": row.dimension_values[0].value,
            "sessions": row.metric_values[0].value
        })

    return results

async def get_users_service(days: int = 30):

    results = await run_ga4_report(
        metrics=["totalUsers"],
        days=days
    )

    if not results:

        return {
            "users": 0
        }

    return {
        "users": results[0]["totalUsers"]
    }
    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",

        metrics=[
            Metric(name="totalUsers")
        ],

        date_ranges=[
            DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )
        ]
    )

    response = client.run_report(request)

    if not response.rows:

        return {
            "users": 0
        }

    return {
        "users": response.rows[0].metric_values[0].value
    }

async def get_sessions_service(days: int = 30):

    results = await run_ga4_report(
        metrics=["sessions"],
        days=days
    )

    if not results:

        return {
            "sessions": 0
        }

    return {
        "sessions": results[0]["sessions"]
    }
    request = RunReportRequest(
        property=f"properties/{GA4_PROPERTY_ID}",

        metrics=[
            Metric(name="sessions")
        ],

        date_ranges=[
            DateRange(
                start_date=f"{days}daysAgo",
                end_date="today"
            )
        ]
    )

    response = client.run_report(request)

    if not response.rows:

        return {
            "sessions": 0
        }

    return {
        "sessions": response.rows[0].metric_values[0].value
    }