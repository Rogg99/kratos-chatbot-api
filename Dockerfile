FROM python:3.12-slim-bullseye
LABEL maintainer="Franck ETAPE <franck.etape@afreetech.com>"

# images dependecy
RUN apt-get update
RUN apt-get install -y gcc libpq-dev python3-dev musl-dev

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 7898
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:7898" ]