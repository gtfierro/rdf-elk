FROM python:3.7-slim-bullseye

RUN pip install "poetry==1.1.13"
RUN apt-get update && apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash
RUN apt-get install -y nodejs

ADD . /app
WORKDIR /app
RUN poetry install
RUN npm install
ENTRYPOINT ["poetry", "run", "python", "app.py"]
