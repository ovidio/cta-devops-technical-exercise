# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Takes in Github Secrets
ARG GIPHY_API_KEY=${GIPHY_API_KEY}
ENV GIPHY_API_KEY=${GIPHY_API_KEY}

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
