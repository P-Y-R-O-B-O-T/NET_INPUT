#!/usr/bin/python3

from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QFrame, QLabel, QGraphicsBlurEffect
from PyQt5.QtGui import QGuiApplication, QIcon, QFont, QPixmap, QPainterPath, QRegion
from PyQt5.QtCore import Qt, QPoint, QRectF, QObject, QThread, pyqtSignal
from PyQt5 import QtWidgets

import threading

from PyQt5.QtWidgets import QApplication

from CYPHER_PROTOCOL.CYPHER_CLIENT.cypher_client import CYPHER_CLIENT, threading
import time
import sys

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

REQ_TIME = time.time()
INIT_TIME = time.time()

#$$$$$$$$$$#

EVENT_MAP = {49:"1",
             81:"q",
             65:"a",
             90:"z",
             50:"2",
             87:"w",
             83:"s",
             88:"x",
             51:"3",
             69:"e",
             68:"d",
             67:"c",
             52:"4",
             82:"r",
             70:"f",
             86:"v",
             53:"5",
             84:"t",
             71:"g",
             66:"b",
             54:"6",
             89:"y",
             72:"h",
             78:"n",
             55:"7",
             85:"u",
             74:"j",
             77:"m",
             56:"8",
             73:"i",
             75:"k",
             57:"9",
             79:"o",
             76:"l",
             48:"0",
             80:"p",
             96:"`",
             32:"Space",
             16777217:"Tab",
             16777252:"Caps_Lock",
             16777248:"Shift",
             16777249:"Ctrl",
             16777251:"Alt",
             16777235:"Up",
             16777237:"Down",
             16777234:"Left",
             16777236:"Right",
             45:"minus",
             61:"plus",
             16777219:"BackSpace",
             91:"bracketleft",
             93:"bracketright",
             92:"backslash",
             59:"colon",
             39:"quoteright",
             16777220:"Return",
             44:"comma",
             46:"period",
             47:"slash",
             16777264:"F1",
             16777265:"F2",
             16777266:"F3",
             16777267:"F4",
             16777268:"F5",
             16777269:"F6",
             16777270:"F7",
             16777271:"F8",
             16777273:"F10",
             16777274:"F11",
             16777275:"F12"
             }

class CLIENT :
    def __init__(self) -> None:
        global IP
        print(IP)
        self.EVENT_QUEUE = [((0.5, 0.5), "mouse move")]
        self.FIRST_QUERY = False
        self.STATUS = True
        self.FAILED_QUERIES = 0
        self.FAILED_QUERIES_THREASHOLD = 3
        self.LOCK = threading.Lock()
        self.CLIENT = CYPHER_CLIENT(ip=IP,
                                    port=55555,
                                    recv_buffer=RECV_BUFFER,
                                    transmission_buffer=TRANSMISSION_BUFFER,
                                    encryption_key=ENCRYPTION_KEY,
                                    decryption_key=DECRYPTION_KEY,
                                    responce_handler=self.responce_handler,
                                    offline_signal_processor=self.offline_proecssor,
                                    timeout=1)
        self.THREAD = threading.Thread(target=self.send_events)

    def responce_handler(self, responce) -> None :
        self.FAILED_QUERIES = 0
        if not self.FIRST_QUERY :
            self.FIRST_QUERY = True

    def send_events(self) :
        while self.STATUS :
            time.sleep(1/60)
            if self.EVENT_QUEUE != [] :
                self.LOCK.acquire()
                event = self.EVENT_QUEUE.pop(0)
                self.LOCK.release()
                self.CLIENT.make_request(path="EVENT", data=event)

    def add_event(self, event, event_type) -> None :
        self.LOCK.acquire()
        self.EVENT_QUEUE.append((event, event_type))
        self.LOCK.release()

    def start_client(self) -> None :
        self.THREAD.start()

    def stop_client(self) -> None :
        while self.EVENT_QUEUE != [] and self.FAILED_QUERIES < self.FAILED_QUERIES_THREASHOLD :
            time.sleep(1)
        self.STATUS = False

    def online_processor(self) :
        self.FAILED_QUERIES = 0

    def offline_proecssor(self) :
        self.FAILED_QUERIES += 1
        if self.FAILED_QUERIES > self.FAILED_QUERIES_THREASHOLD :
            try :
                self.CLIENT.close_connection()
            except : pass

class SCREEN(QMainWindow) :
    def __init__(self) :
        super().__init__()
        global IP
        global C
        global EVENT_MAP

        self.C = C
        self.EVENT_MAP = EVENT_MAP

        self.setAttribute(Qt.WA_DeleteOnClose)
        flags = Qt.WindowFlags(Qt.FramelessWindowHint |
                               Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        self.setStyleSheet("background-color: rgb(0,0,0)")
        self.resize(QtWidgets.QDesktopWidget().screenGeometry(-1).width(),
                    QtWidgets.QDesktopWidget().screenGeometry(-1).height())
        self.LABEL = QLabel(self)
        self.LABEL.setText(IP)
        self.LABEL.setFont(QFont("Times", self.width()//60))
        self.LABEL.resize(self.width(),self.width()//50)
        self.LABEL.setAlignment(Qt.AlignCenter)
        self.LABEL.setStyleSheet("color: rgba(0, 200, 0, 1)")
        self.setMouseTracking(True)

    def keyPressEvent(self, event) -> None :
        self.C.add_event(self.EVENT_MAP[event.key()],
                         "down")

    def keyReleaseEvent(self, event) -> None :
        self.C.add_event(self.EVENT_MAP[event.key()],
                         "up")

    def mouseMoveEvent(self, event) -> None :
        self.C.add_event((event.x()/self.width(), event.y()/self.height()), "mouse move")

    def mousePressEvent(self, event) -> None :
        self.C.add_event("m{0}".format(event.button()), "down")

    def mouseReleaseEvent(self, event) -> None :
        self.C.add_event("m{0}".format(event.button()), "up")

if __name__ == "__main__" :
    IP = input("Enter IP :")
    C = CLIENT()
    C.CLIENT.connect()
    C.start_client()

    init_time = time.time()
    while not C.FIRST_QUERY :
        time.sleep(1/60)
        print(C.FIRST_QUERY, time.time() - init_time, C.FAILED_QUERIES)
        if time.time() - init_time > 5 :
            C.stop_client()
            sys.exit(0)
    App = QApplication(sys.argv)
    S = SCREEN()
    S.showFullScreen()
    App.exec()
    C.stop_client()
    sys.exit()
