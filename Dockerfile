FROM python:3.12

LABEL authors="Danyil Bazarov"

WORKDIR /StarBook

COPY ./requirements.txt /StarBook/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /StarBook/requirements.txt

COPY ./backend/app /StarBook/app

CMD ["fastapi", "run", "app/main.py", "--port", "8080"]