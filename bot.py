from irc import IRC
import os
import random
import json
import threading
import time




# Config
with open("config.json", mode="r", encoding="utf-8") as file:
    config = json.load(file)

server = config["server"]
port = config["port"]
channel = config["channel"]
botNick = config["botNick"]
password = config["password"]
adminName = config["adminName"]
exitCode = "bye " + botNick


# print(config)
# print(config["port"])

irc = IRC()
irc.connect(server, port, channel, botNick, password)

def randTimeMessage():
    while True:
        irc.message("Scheduled message")
        print("randTime started")
        time.sleep(3)

thread = threading.Thread(target=randTimeMessage)
thread.start()

# Response loop
while True:
    response = irc.getResponse()
    print(response)

    if "PRIVMSG" in response:
        name = response.split("!", 1)[0][1:]
        message = response.split("PRIVMSG", 1)[1].split(":", 1)[1]

        if "hi " + botNick in response:
            irc.message(f"Herro {name}!")


        if name.lower() == adminName.lower() and message.rstrip() == exitCode:
            irc.message("oh...okay. :'(")
            # Send the quit command to the IRC server so it knows we’re disconnecting.
            irc.quit()
            break