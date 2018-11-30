FROM python:3

ADD . /app
WORKDIR /app

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt



EXPOSE 5000

CMD ["python", "app.py"]