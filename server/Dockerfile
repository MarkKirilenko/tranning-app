FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/server

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["python","main.py"]