FROM python:3

WORKDIR /app

# Python не будет пытаться создавать файлы .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Включение буферизации вывода (output)
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install netcat-openbsd -y
RUN apt-get upgrade -y

RUN pip install --upgrade pip
COPY req.txt ./
RUN pip install -r req.txt

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
