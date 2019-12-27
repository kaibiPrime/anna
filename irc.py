import socket
import time
import sys


class IRC:


    def __init__(self):
        # Define socket
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def message(self, msg, target=None):
        if target is None:
            target = self.defaultChan
        # Transfer data
        self.irc.send(bytes("PRIVMSG " + target + " :" + msg + "\n", "UTF-8"))

    def getResponse(self):
        response = self.irc.recv(2048).decode("UTF-8")
        response = response.strip("\n\r")

        if response.find("PING :") != -1:
            pong = response.split("PING :", -1)[1]
            print("It's a ping: " + pong)

            self.irc.send(bytes("PONG :" + pong + "\n", "UTF-8"))

        return response

    def connect(self, server, port, channel, botNick, password):
        self.defaultChan = channel

        print("Connecting to: " + server)
        self.irc.connect((server, port))

        # Perform user authentication
        self.irc.send(
            bytes(
                "USER "
                + botNick
                + " "
                + botNick
                + " "
                + botNick
                + " :python\n",
                "UTF-8",
            )
        )
        self.irc.send(bytes("NICK " + botNick + "\n", "UTF-8"))
        self.irc.send(bytes("AUTH " + botNick + " " + password + "\n", "UTF-8"))
        time.sleep(2)

        # join channel
        endMotd = ""
        keepLooping = True

        while keepLooping:
            query = self.getResponse()
            print(query)

            if query.find("End of /MOTD command.") != -1:
                print("Found end of MOTD, attempting to join channel")
                self.irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))
                keepLooping = False
                time.sleep(1)

    def quit(self):
        self.irc.send(bytes("QUIT \n", "UTF-8"))
