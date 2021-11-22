FROM python:3.8.2-alpine

RUN apk update && apk upgrade && \
    apk add --no-cache make g++ bash git openssh postgresql-dev curl

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/
RUN python -m pip install -U --force-reinstall pip
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ /usr/src/app

EXPOSE 80

CMD ["python", "main.py"]
