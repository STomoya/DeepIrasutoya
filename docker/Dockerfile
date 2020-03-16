FROM python:3.7

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    wget \
    curl \
    unzip \
    git

# install chrome
WORKDIR /tmp
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get install -fy
# install chrome driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

WORKDIR /usr/src
COPY ./docker/requirements.txt requirements.txt

RUN pip install --default-timeout=100 -r requirements.txt