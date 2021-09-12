# Discord CTFBot

## Introduction
This bot is designed to fetch [ctftime.org](https://ctftime.org/) events and updates a text-channel in your Discord server. <br />

## Requirements
- [Docker](https://www.docker.com/get-started)
- [Discord API Application](https://discord.com/developers/applications) which will allow you to create a bot and generate a private token. <br />

## Get Started
1. Clone this repository
2. Create a bot with Discord [here](https://discord.com/developers/applications) and copy the private token: <br /> <br />
![image](https://user-images.githubusercontent.com/59978921/132972500-cdcfb8ed-4bd6-4698-9f92-d64894fcfd92.png)  <br /> 
  <p align="center"><b>⚠️⚠️⚠️KEEP YOUR TOKEN PRIVATE⚠️⚠️⚠️</b></p><br />

3. In order to send CTF updates to your Discord server, you will need a designated `#text-channel` for the bot. Before you are able to get the text-channel ID needed for the bot, you will need to enable `Developer Mode` through your Discord settings: <br /> <br />
![image](https://user-images.githubusercontent.com/59978921/132972739-a3bcd57f-1a0e-4ccf-b8a7-782a67d30b46.png) <br /> <br />
4. Once Developer Mode is enabled, right-click on the text-channel you want the bot to send updates to and select Copy ID: <br /> <br />
![image](https://user-images.githubusercontent.com/59978921/132972974-a97587d3-2215-4e99-a9f0-fad94588cc28.png) <br /> <br />
5. Open up `src/pwnbot.py` in your desired text editor and set the values for `BOT_TOKEN` and `BOT_CHANNEL` with your own token and bot channel ID: <br /> <br />
![image](https://user-images.githubusercontent.com/59978921/132973115-fbc1da7f-ea9c-448d-add3-99db050f7a5c.png) <br />
<p align="center"><i>Note: TOKEN is a string and BOT_CHANNEL is an integer.</i></p><br />

6. After saving `src/pwnbot.py`, you will need to run the following command in this repository:
```
$ docker build -t discord .
```
7. Finally, you can run this last command to run the Docker image and have it running in the background of your server:
```
$ docker run discord &
```
8. You should now be able to run `!help` to get started. 🤖
<br />

## Bot Commands
```
Usage: !<command>

Event Commands:
 * !events - Displays ongoing ctf events within the week.
 * !events all - Displays ctf events for the past and next week.
 * !events next - Displays upcoming ctf events for next week.
 * !events past - Displays finished ctf events from the past week.

Clear Commands:
 * !clear - Clears the last 20 messages from pwnbot in current channel.
 * !clear all - Clears all messages from pwnbot in current channel.
 * !clear last - Clears last message from pwnbot in current channel.

Util Commands:
 * !ping - Checks the latency for pwnbot with date/time

Misc Commands:
 * !celebrate - Celebration!!
 * !facepalm - Sometimes you just have to facepalm ...
```
