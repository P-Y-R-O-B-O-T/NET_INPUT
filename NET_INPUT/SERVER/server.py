#!/usr/bin/python3

from CYPHER_PROTOCOL.CYPHER_SERVER.cypher_server import CYPHER_SERVER
import os
import threading
import time

#$$$$$$$$$$#

RECV_BUFFER = 1024*64
TRANSMISSION_BUFFER = 1024*64

KEY = input("Enter Key :")
for _ in KEY :
    if not _.isalnum() :
        exit()
if len(KEY) < 32 :
    KEY = KEY+"a"*(32-len(KEY))
else :
    KEY = KEY[:32]

ENCRYPTION_KEY = KEY
DECRYPTION_KEY = KEY


TIMEOUT = 60*1

SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920

#$$$$$$$$$$#

class SERVER :
    def __init__(self) :
        self.EVENT_QUEUE = []
        self.STATUS = True

        self.SERVER = CYPHER_SERVER(host="0.0.0.0",
                                    port=55555,
                                    recv_buffer=RECV_BUFFER,
                                    transmission_buffer=TRANSMISSION_BUFFER,
                                    encryption_key=ENCRYPTION_KEY,
                                    decryption_key=DECRYPTION_KEY,
                                    request_handler=self.handle_request,
                                    timeout=TIMEOUT,
                                    debug1=True,
                                    debug2=True)
        self.THREAD = threading.Thread(target=self.event_processing_loop)

    def handle_request(self,
                       request: dict,
                       ip_port: tuple) :
        print(ip_port)
        if request["PATH"] == "EVENT" :
            self.EVENT_QUEUE.append(request["DATA"])

        return request

    def event_processing_loop(self) -> None :
        while self.STATUS :
            time.sleep(1/60)
            if self.EVENT_QUEUE != [] :
                print("PROCESSING EVENT")
                event = self.EVENT_QUEUE.pop(0)
                print(event)
                self.process_using_xdotool(event)

    def process_using_xdotool(self, event) -> None :
        if type(event[0]) is tuple or type(event[0]) is list :
            os.system("xdotool mousemove {0} {1}".format(int(SCREEN_WIDTH*event[0][0]),
                                                         int(SCREEN_HEIGHT*event[0][1])))
        elif type(event[0]) is str :
            if event[0] not in ("m1", "m2", "m3", "m4", "m5") :
                print("IS NORMAL KEY")
                if event[1] == "up" :
                    print("RELEASE")
                    os.system("xdotool keyup {0}".format(event[0]))
                else :
                    print("PRESS")
                    os.system("xdotool keydown {0}".format(event[0]))
            else :
                if event[1] == "up" :
                    os.system("xdotool mouseup {0}".format(event[0][1:]))
                if event[1] == "down" :
                    os.system("xdotool mousedown {0}".format(event[0][1:]))

    def start_server(self) :
        self.SERVER.start_server()
        self.THREAD.start()
        input()
        self.STATUS = False
        self.SERVER.destroy_all_connections()
        self.SERVER.stop_server()

if __name__ == "__main__" :
    S = SERVER()
    S.start_server()
