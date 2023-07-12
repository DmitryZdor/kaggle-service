from typing import List, Annotated, Union
from pydantic.v1 import Required
import requests
from fastapi import FastAPI, Depends, Query, HTTPException, status
import os
from zipfile import ZipFile
from dotenv import load_dotenv


import models
from file_properties import get_names_and_column, get_file_details
from db_connect import engine, SessionLocal, Base
from sqlalchemy.orm import Session

load_dotenv()

# создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()


# определяем зависимость
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


@app.get("/file/detail/")
def detail(file_name: Annotated[str, Query(description="csv file name")],
           sort_col: Annotated[list[str], Query(description="columns for sort")] = None,
           filter_col: Annotated[list[str], Query(description="columns for filter")] = None
           ):

    # query_items = {"sort": sort, "filter": filter_col}
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
                zf.extract(item.filename, f"../files/")
        os.remove(f"{datasetSlug}.zip")
        return [db.query(models.File).get(id) for id in data]

    except Exception as err:
        print(f"Что-то пошло не так (: //{err}//")
