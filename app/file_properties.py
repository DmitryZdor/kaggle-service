import csv
import pandas as pd

from models import File


def get_names_and_column(file: File):
    try:
        with open(f"../files/{file.name}", "r", encoding="utf-8") as f:
            data = csv.DictReader(f).fieldnames
        return {"name": file.name, "columns": data}
    except Exception as ex:
        return {"name": file.name, "error": f"{ex}"}

def get_file_details(file_name: str, filter_col: list[str], sort_col: list[str]):
    try:
        with open(f"../files/{file_name}", "r", encoding="utf-8") as f:
            if filter_col and sort_col:
                data = pd.read_csv(f).sort_values(sort_col).filter(items=filter_col)
            elif filter_col and not sort_col:
                data = pd.read_csv(f).filter(items=filter_col)
            elif sort_col and not filter_col:
                data = pd.read_csv(f).sort_values(sort_col)
            else:
                data = pd.read_csv(f)
        return data.to_dict(index=True, orient="records")
    except Exception as ex:
        return {"name": file_name, "error": f"{ex}"}


# def open_file(file_name):
#     with open(f"../files/{file_name}", "r", encoding="utf-8") as f:
#         return csv.DictReader(f)