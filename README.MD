# HTTP сервис для работы с импортируемыми данными

- реализована загрузка данных в формате файлов csv  с Kaggle.  
- Получение списка файлов с информацией о колонках  
- Возможность получения данных из конкретного файла с опциональными фильтрацией  
и сортировкой по одному или нескольким столбцам
- подключена база данных, для хранения (параметров файла с датасетом)
---
Реализованы три эндпоинта:
1. **"/file/download"**  -   для загрузки файла (дополнительно надо ввести два параметра {ownerSlug} и {datasetSlug})
их можно узнать выполнив команду в терминале, 
```
kaggle datasets list
```
при загрузке файла, в базу данных попадает запись о нем, а файл будет сохранен в директорию kaggle-service/files/  
2. **"/list"** - для получения списка скачанных файлов и информаций о колонках в них  
3. **"/dataset/detail/"** - для данных из конкретного файла с опциональными  
фильтрацией и сортировкой по одному или нескольким столбцам

___ 
### Чтобы запустить проект нeoбходимо

1. Клонировать репозиторий и перейти в него в командной строке

```
git@github.com:DmitryZdor/kaggle-service.git
```
2. Создать в корневом каталоге  файл .env
заполнить данными
```
ACCEPT = "..." # your accept
USER_AGENT = "..." # your user-agent
USER_NAME = "..." # your kaggle username 
TOKEN = "..." # your kaggle token
URL = "https://www.kaggle.com/api/v1/datasets/download"
```


3. Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv     
       или     
python -m venv venv
```
```
source venv/Scripts/activate
           или 
source venv/bin/activate           
```
```
python3 -m pip install --upgrade pip
            или 
python -m pip install --upgrade pip
```
4. Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```
5. Запустить сервер unicorn из директории kaggle-service/app/
```
uvicorn app:app --host 127.0.0.1 --port 8001 --reload
```
6. Перейти по адресу  

```
http://127.0.0.1:8001/docs
```
7. Чтобы запустить приложение c помощью Docker необходимо,
находясь в корневой папке, сначала собрать Docker image командой.
```
docker build . -t kaggle:latest
```
8. Затем запустить контейнер например на порту 2552 командой  
```
docker run -d -p 2552:8000 kaggle
```
9. Переходим по адресу
```
http://localhost:2552/docs
```