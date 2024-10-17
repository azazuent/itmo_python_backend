FROM python:latest
LABEL authors="Azazuent"

COPY ./main.py /app/
COPY ./database /app/
COPY ./routers /app/
COPY ../requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

ENTRYPOINT ["main.py"]
