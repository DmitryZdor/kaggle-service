import os
from typing import Annotated
from zipfile import ZipFile

import models
import requests
from db_connect import Base, SessionLocal, engine
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Query
from file_properties import get_file_details, get_names_and_column
from sqlalchemy.orm import Session

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


url = os.getenv("URL")
headers = {
    "Accept": os.getenv("ACCEPT"),
    "User-Agent": os.getenv("USER_AGENT")
}
auth = (os.getenv("USER_NAME"), os.getenv("TOKEN"))


@app.get("/dataset/detail/")
def detail(file_name: Annotated[str, Query(description="csv file name")],
           sort_col: Annotated[list[str], Query(description="columns for sort")] = None,
           filter_col: Annotated[list[str], Query(description="columns for filter")] = None
           ):
    return get_file_details(file_name=file_name, filter_col=filter_col, sort_col=sort_col)


@app.get("/list")
def get_file_list(db: Session = Depends(get_db)):
    return [get_names_and_column(item) for item in db.query(models.File).all()]


@app.get("/file/download")
def download_file(ownerSlug, datasetSlug, db: Session = Depends(get_db)):
    try:
        data = []
        req = requests.get(url=f"{url}/{ownerSlug}/{datasetSlug}", headers=headers, auth=auth)
        with open(f"{datasetSlug}.zip", "wb") as f:
            f.write(req.content)
        with ZipFile(f"{datasetSlug}.zip") as zf:
            for item in zf.filelist:
                new_file = models.File(
                    name=item.filename,
                    size=item.file_size,
                    zip_arch=datasetSlug,
                    owner=ownerSlug,
                )

                db.add(new_file)
                db.commit()
                db.refresh(new_file)
                data.append(new_file.id)
                zf.extract(item.filename, "../files/")
        os.remove(f"{datasetSlug}.zip")
        return [db.query(models.File).get(id) for id in data]

    except Exception as err:
        print(f"Что-то пошло не так (: //{err}//")
