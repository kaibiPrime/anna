from functools import *
import time

class ConstantLoop:
    def __init__(self, whaddap="heyo"):
        self.whaddap = whaddap
        print("__init__")

    def loopIt(self):
        while True:
            print("looping")
            time.sleep(1)
            
