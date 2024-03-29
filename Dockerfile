FROM ubuntu:20.04

# Installing recent packages for python3.8
RUN apt-get update; apt-get install software-properties-common -y; add-apt-repository ppa:deadsnakes/ppa; apt-get install python3-9 -y; apt-get install python3-pip -y && \
pip3 install discord.py && \
pip3 install datetime && \
pip3 install pytz && \
pip3 install requests

COPY src/ /discord/

ENTRYPOINT python3 /discord/pwnbot.py
