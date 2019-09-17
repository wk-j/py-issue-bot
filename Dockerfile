# FROM ubuntu:19.10
# FROM ubuntu:18.04
FROM ubuntu:18.10

RUN apt-get update -y
RUN apt-get install -y libsm6 libxext6
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev build-essential

RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY .keys/ /app
COPY .trained-issues/ /app
COPY app.py /app
COPY jwt/   /app

CMD python3 app.py 5555