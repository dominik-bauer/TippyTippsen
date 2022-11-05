FROM python:3.10-slim
ENV TZ="Europe/Berlin"
WORKDIR /usr/app/src
COPY *.py ./
COPY threema_* ./
COPY requirements.txt ./
RUN apt-get update && apt-get install -y \
    vim 
RUN pip install -r requirements.txt
RUN chmod +x threema_linux
CMD [ "python3.10", "./main.py"]