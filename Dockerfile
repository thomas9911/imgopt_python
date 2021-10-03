FROM rust:latest

WORKDIR /usr/src/app

RUN apt update 
RUN apt install -y python3 python3-dev python3-pip

COPY . .

RUN pip install -v .

CMD [ "bash" ]
