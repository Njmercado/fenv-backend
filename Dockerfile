FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

LABEL Author="Nino Mercado"
LABEL version="1.0"

RUN mkdir -p /src
WORKDIR /src

COPY requirements.txt .

RUN pip3 install -r requirements.txt
