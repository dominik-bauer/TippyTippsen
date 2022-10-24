FROM golang:1.19.2-bullseye
WORKDIR /usr/app/src
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* 
COPY *.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN go install github.com/karalabe/go-threema/cmd/threema@latest 


CMD [ "python3", "./main.py"]