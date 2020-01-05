from irc import IRC
import os
import random
import json
import threading
import time

try:
    from sensors import DHT
    dht = DHT()
except:
    print("Sensors not imported")


# Loads a config file from the current directory
with open("config.json", mode="r", encoding="utf-8") as file:
    config: dict = json.load(file)

# Declarations
server: str = config["server"]
port: int = config["port"]
channel: str = config["channel"]
botNick: str = config["botNick"]
password: str = config["password"]
adminName: str = config["adminName"]
exitCode: str = "bye " + botNick

stopThreads: bool = False

# print(config)
# print(config["port"])


# Connect to IRC
irc = IRC()
irc.connect(server, port, channel, botNick, password)


def randTimeMessage(stop):
    while stop() is False:
        randInt: int = random.randint(2,7)
        irc.message("Spam >:)")
        print("randTime started")
        time.sleep(randInt)


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
        
        if "$sensors" in message:
            try:
                data = dht.getTempHumidity()
                print("Sensor data:", data)
                if data is not False:
                    irc.message(f"Temperature: {data[0]:.1f}, Humidity: {data[1]:.1f}")
                else:
                    irc.message("Failed to retrieve data")
            except:
                irc.message("Sensor module not loaded!")

        # Kills the thread safely
        if name.lower() == adminName.lower() and message.rstrip() == "$stop":
            print("Stopping repeated message")
            irc.message(f"S-sorry {name} I'll stop spamming...")
            stopThreads = True
            spamThread.join()

        if name.lower() == adminName.lower() and message.rstrip() == exitCode:
            irc.message("oh...okay. :'(")
            stopThreads = True
            # Send quit command to the server
            irc.quit()
            break
