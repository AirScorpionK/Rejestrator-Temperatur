FROM python:3.14
LABEL authors="airsorpionk"

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
CMD ["python", "-m", "app.main"]
