FROM ubuntu:latest

WORKDIR /zadanie
ADD . /zadanie

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install python3 python3-pip python3-dev build-essential cron python3-setuptools apt-utils -y

RUN pip3 install -r requirements.txt

ADD cron/task_runner.py task_runner.py
ADD cron/crontab /etc/cron.d/task-cron
RUN chmod 0644 /etc/cron.d/task-cron
RUN crontab /etc/cron.d/task-cron

RUN touch /var/log/cron.log



EXPOSE 5000
ADD worker.py worker.py


CMD cron &
CMD flask run --host=0.0.0.0
