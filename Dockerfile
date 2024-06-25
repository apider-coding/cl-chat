FROM python:3.11-slim-buster

RUN cp -r -f /usr/share/zoneinfo/Europe/Stockholm /etc/localtime

ADD . /app

WORKDIR /app

RUN pip3 --no-cache install -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3"]
CMD ["app.py"]