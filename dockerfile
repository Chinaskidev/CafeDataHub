FROM python:3.11.8
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD ["uvicorn", "app_rf:app", "--host", "0.0.0.0", "--port", "8000"]