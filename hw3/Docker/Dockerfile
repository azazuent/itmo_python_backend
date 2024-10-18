FROM python:latest
LABEL authors="Azazuent"

COPY ../. /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0"]
