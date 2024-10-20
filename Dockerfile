FROM ubuntu:latest

RUN apt-get update -y

RUN apt-get install -y python3.9 python3-pip


WORKDIR /app

COPY backend ./backend
COPY frontend/dist ./frontend/dist

RUN pip3 install -r backend/requirements.txt

EXPOSE 5000

CMD [ "python3","backend/app.py" ]