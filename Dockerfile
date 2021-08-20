FROM ubuntu:20.04

RUN apt update && apt install python3.8 -y && apt-get install python3-pip -y && \
pip3 install discord.py && \
pip3 install datetime && \
pip3 install pytz && \
pip3 install requests

COPY pwnbot.py ctftime.py /discord/

ENTRYPOINT python3 /discord/pwnbot.py