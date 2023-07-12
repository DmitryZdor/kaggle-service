import requests
from zipfile import ZipFile
import os
from dotenv import load_dotenv

load_dotenv()

ownerSlug = "bulentesen"
datasetSlug = "cardiac-arrhythmia-database"


url = f'https://www.kaggle.com/api/v1/datasets/download/{ownerSlug}/{datasetSlug}'
headers = {
        "Accept": os.getenv("ACCEPT"),
        "User-Agent": os.getenv("USER_AGENT")
        }
auth = (os.getenv("USER_NAME"), os.getenv("TOKEN"))
try:
    req = requests.get(url=url, headers=headers, auth=auth)
    with open(f'../req.zip', 'wb') as f:
        f.write(req.content)
    with ZipFile(f'../req.zip') as zf:
        zf.extractall(f'../')
    os.remove(f'../req.zip')

except Exception as err:
    print(f"Что-то пошло не так: //{err}//")