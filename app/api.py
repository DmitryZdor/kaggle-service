import random
from time import sleep
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

session = requests.Session()
url = os.getenv("URL_LIST")
auth = (os.getenv("USER_NAME"), os.getenv("TOKEN"))
headers = {"Accept": os.getenv("ACCEPT"), "User-Agent": os.getenv("USER_AGENT")}

def read_urls_per_page(url, page, headers, auth):

    return {
        item["ownerName"]: item["url"] for item in session.get(url=(f"{url}?page={page}"
                                                                    ), headers=headers, auth=auth).json()
    }


json_data = []
for p in range(1, 2):
    json_page = read_urls_per_page(url, page=p, headers=headers, auth=auth)
    json_data.append({p: json_page})
    print(f"page # {p} is done..")
    sleep(random.randrange(1, 3))

with open('../data/all_datasets-1.json', "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=3, ensure_ascii=False)
