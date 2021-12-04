FROM python

WORKDIR /app
ADD . .

RUN pip install -r requirements.txt

ENTRYPOINT ['python', 'app.py']
