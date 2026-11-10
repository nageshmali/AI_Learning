
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

if not SERPAPI_KEY:
    raise ValueError("SERPAPI API KEY NOT FOUND")


def get_iphone_17_price():

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_shopping",
        "q": "iPhone 17",
        "gl": "in",
        "hl": "en",
        "api_key": SERPAPI_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if "error" in data:
            print("SerpApi Error:", data["error"])
            return None

        results = data.get("shopping_results", [])

        for item in results:

            title = item.get("title", "").lower()
            source = item.get("source", "").lower()

            if (
                "amazon" in source
                and "iphone 17" in title
                and "17e" not in title
                and "pro" not in title
                and "refurbished" not in title
                and "renewed" not in title
                and "used" not in title
            ):

                price = item.get("extracted_price")

                if price is not None:
                    return float(price)

        return None

    except requests.exceptions.RequestException as error:
        print("API Request Error:", error)
        return None
