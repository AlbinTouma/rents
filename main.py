import requests as r
from datetime import datetime
import json
import logging


""""Current version collects rental listings for the Gothenburg area from HomeQ API and saves them into a JSON file."""

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename="homeq_scraper.log")
TODAY=datetime.now().strftime("%Y-%m-%d")
OUTPUT_DIR = "data"
BASE_URL = "https://api.homeq.se/api/v3/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8"
}
PAYLOAD={
    "amont": 10,
    "geo_bounds": {
        "max_lat": 57.97066106464624,
        "max_lng": 12.781249677520549,
        "min_lat": 57.28557252214253,
        "min_lng": 11.181280322477903
    },
    "page":None,
    "sorting": "proximity_map_center.asc",
    "zoom": 8.54
}

def fetch_data(page):
    PAYLOAD["page"] = page
    response = r.post(BASE_URL, headers=HEADERS, json=PAYLOAD)
    response.raise_for_status()
    return response.json(), response.status_code


def main():
    logging.info("Starting data fetch from HomeQ AP")
    page = 1    
    all_results = []

    while True:
        data, status_code = fetch_data(page)
        results = data.get("results", [])
        if not results:
            logging.info("No more data found. Exiting loop on page {}.".format(page))
            break
        all_results.extend(results)
        logging.info(f"Fetched page {page} with {len(results)} results.")
        page += 1

    result_json = {
        "status_code": status_code,
        "date": TODAY,
        "source": "homeq",
        "pages_fetched": page - 1,
        "nr_results": len(all_results),
        "results": all_results

    }

    with open(f"{OUTPUT_DIR}/homeq_data_{TODAY}.json", "w") as f:
        json.dump(result_json, f, indent=4)
    logging.info(f"Data fetching completed.")


if __name__ == "__main__":
    main()