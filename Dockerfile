FROM python:3.11-slim-buster

RUN cp -r -f /usr/share/zoneinfo/Europe/Stockholm /etc/localtime

ADD . /app

WORKDIR /app

RUN pip3 --no-cache install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["chainlit", "run", "/app/app.py"]