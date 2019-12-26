from irc import IRC
import os
import random
import json
from threadTest import ConstantLoop

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


print(config)
print(config["port"])


irc = IRC()
irc.connect(server, port, channel, botNick, password)

# Response loop
while True:
    response = irc.getResponse()
    print(response)

    if "PRIVMSG" in response:

        name = response.split("!", 1)[0][1:]
        message = response.split("PRIVMSG", 1)[1].split(":", 1)[1]

        if "hi " + botNick in response:
            irc.message("Herro " + name + "!")

        if "loop" in response:
            asd = ConstantLoop()
            irc.message("object created")
            asd.loopIt()

        if name.lower() == adminName.lower() and message.rstrip() == exitCode:
            # If we do get sent the exit code, then send a message (no target defined, so to the channel) saying we’ll do it, but making clear we’re sad to leave.
            irc.message("oh...okay. :'(")
            # Send the quit command to the IRC server so it knows we’re disconnecting.
            irc.quit()
            break
