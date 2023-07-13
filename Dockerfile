FROM python:3.10

RUN mkdir /kaggle

WORKDIR /kaggle

COPY ./requirements.txt /kaggle/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /kaggle/requirements.txt

COPY ./app /kaggle/app
COPY ./.env /kaggle/.env

WORKDIR /kaggle/app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
