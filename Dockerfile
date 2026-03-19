FROM python:3.11
LABEL authors="airsorpionk"

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app/main.py"]