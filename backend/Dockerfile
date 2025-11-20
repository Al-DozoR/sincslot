FROM python:3.12-slim

WORKDIR /syncslot/backend


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update
RUN apt-get install -y python3-dev gcc libc-dev libffi-dev
RUN apt-get -y install libpq-dev gcc

COPY requirements.txt /syncslot/backend
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /syncslot/backend
EXPOSE 10004
ENV PYTHONPATH="${PYTHONPATH}:/syncslot"


RUN chmod a+x ./start.sh

ENTRYPOINT ["./start.sh"]
