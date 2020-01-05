from irc import IRC
import os
import random
import json
import threading
import time


# Loads a config file from the current directory
with open("config.json", mode="r", encoding="utf-8") as file:
    config = json.load(file)

# Declarations
server = config["server"]
port = config["port"]
channel = config["channel"]
botNick = config["botNick"]
password = config["password"]
adminName = config["adminName"]
exitCode = "bye " + botNick

stopThreads: bool = False

# print(config)
# print(config["port"])


# Connect to IRC
irc = IRC()
irc.connect(server, port, channel, botNick, password)


def randTimeMessage(stop):
    while stop() is False:
        irc.message("Scheduled message")
        print("randTime started")
        time.sleep(3)

# Creates a new thread, thread's target function will just spam the channel at an interval
# Gets passed an argument so the thread can be killed safely, and set as a Daemon so the
# thread is guaranteed to terminate when the main thread terminates
spamThread = threading.Thread(target=randTimeMessage, args=(lambda: stopThreads,), daemon=True)
spamThread.start()

# Response loop
while True:
    response = irc.getResponse()
    print(response)

    if "PRIVMSG" in response:
        name = response.split("!", 1)[0][1:]
        message = response.split("PRIVMSG", 1)[1].split(":", 1)[1]

        if "hi " + botNick in message:
            irc.message(f"Herro {name}!")

        if "$threads" in message:
            irc.message(f"Active threads: {threading.active_count()}")

        # Kills the thread safely
        if name.lower() == adminName.lower() and message.rstrip() == "$stop":
            print("Stopping repeated message")
            stopThreads = True
            spamThread.join()

        if name.lower() == adminName.lower() and message.rstrip() == exitCode:
            irc.message("oh...okay. :'(")
            stopThreads = True
            # Send the quit command to the IRC server so it knows we’re disconnecting.
            irc.quit()
            break
