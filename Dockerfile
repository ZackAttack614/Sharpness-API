FROM python:3.9

WORKDIR /app
ADD requirements.txt .

RUN pip install -r requirements.txt && pip install --upgrade flask-api-cache
ADD . .

ENTRYPOINT ["python", "app.py"]
