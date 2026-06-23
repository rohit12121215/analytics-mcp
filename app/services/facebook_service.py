import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_facebook_summary():

    page_id = os.getenv("FACEBOOK_PAGE_ID")
    access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")

    if not page_id or not access_token:
        return {
            "error": "FACEBOOK_PAGE_ID or FACEBOOK_ACCESS_TOKEN missing"
        }

    url = f"https://graph.facebook.com/v23.0/{page_id}"

    params = {
        "fields": "name,followers_count,fan_count,link",
        "access_token": access_token
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {
            "error": response.json()
        }

    data = response.json()

    return {
        "pageName": data.get("name"),
        "followers": data.get("followers_count"),
        "fans": data.get("fan_count")
    }