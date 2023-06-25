FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install requests
RUN mkdir /script
COPY main.py /script
CMD ["python3","-u", "/script/main.py"]
