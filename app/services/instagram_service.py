import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_instagram_posts():

    instagram_id = os.getenv("INSTAGRAM_BUSINESS_ID")
    access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")

    if not instagram_id or not access_token:
        return {
            "error": "INSTAGRAM_BUSINESS_ID or FACEBOOK_ACCESS_TOKEN missing"
        }

    url = f"https://graph.facebook.com/v23.0/{instagram_id}/media"

    params = {
        "fields": "id,caption,timestamp,media_type,permalink",
        "access_token": access_token
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {
            "error": response.json()
        }

    return response.json()


def get_instagram_summary():

    instagram_id = os.getenv("INSTAGRAM_BUSINESS_ID")
    access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")

    if not instagram_id or not access_token:
        return {
            "error": "INSTAGRAM_BUSINESS_ID or FACEBOOK_ACCESS_TOKEN missing"
        }

    url = f"https://graph.facebook.com/v23.0/{instagram_id}"

    params = {
        "fields": "username,followers_count,media_count",
        "access_token": access_token
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {
            "error": response.json()
        }

    return response.json()


def get_instagram_insights():

    instagram_id = os.getenv("INSTAGRAM_BUSINESS_ID")
    access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")

    if not instagram_id or not access_token:
        return {
            "error": "INSTAGRAM_BUSINESS_ID or FACEBOOK_ACCESS_TOKEN missing"
        }

    url = f"https://graph.facebook.com/v23.0/{instagram_id}/insights"

    params = {
        "metric": "reach",
        "period": "day",
        "access_token": access_token
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {
            "error": response.json()
        }

    data = response.json()

    insights = []

    for item in data.get("data", []):
        if item.get("name") == "reach":
            for value in item.get("values", []):
                insights.append({
                    "date": value.get("end_time"),
                    "reach": value.get("value")
                })

    return {
        "account_id": instagram_id,
        "metric": "reach",
        "data": insights
    }