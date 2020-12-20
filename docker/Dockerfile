FROM library/python:3.8.6-slim-buster

RUN apt-get update \
    && apt-get install -y g++ \
    apt-utils \
    apt-transport-https \
    gcc \
    build-essential \
    tzdata \
    locales \
    fonts-takao-gothic \
    liblzma-dev \
    libpq-dev \
    && apt-get upgrade -y \
    && apt-get clean \
    && sed -i -E 's/(CipherString\s*=\s*DEFAULT@SECLEVEL=)2/\11/' /etc/ssl/openssl.cnf \
    && rm -rf /var/lib/apt/lists/*

# timezone setting
ENV TZ=Asia/Tokyo

RUN locale-gen ja_JP.UTF-8
RUN localedef -f UTF-8 -i ja_JP ja_JP
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:jp
ENV LC_ALL ja_JP.UTF-8
ENV PYTHONIOENCODIND utf_8

# set work directory
WORKDIR /usr/local/src/covid19-simulation
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/local/src/covid19-simulation

# copy project
COPY . /usr/local/src/covid19-simulation
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

CMD /bin/bash
