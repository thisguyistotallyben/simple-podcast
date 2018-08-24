import sys
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *


class SimplePodcast(QtWidgets.QMainWindow):
    def __init__(self):
        # formalities
        super().__init__()

        # window variables
        self.title = 'Simple Podast'
        self.left = 10
        self.top = 10
        self.width = 650
        self.height = 500

        # other variables
        self.bots = {}

        # setup
        self.setupWindow()
        self.setupWidgets()
        self.setupLayouts()
        self.build()

        # show
        self.show()

    def setupWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def setupWidgets(self):
        self.widgets = {}

        # define
        self.widgets['main'] = QWidget()
        self.widgets['connserver'] = QPushButton('Connect to server')
        self.widgets['botlistbutt'] = QPushButton('Get list of bots')
        self.widgets['dothing'] = QPushButton('Do the thing')

        # connect
        self.widgets['connserver'].clicked.connect(self.connect_server)
        self.widgets['botlistbutt'].clicked.connect(self.botlistsig)
        self.widgets['dothing'].clicked.connect(self.dothing)

    def setupLayouts(self):
        self.layouts = {}

        # define
        self.layouts['main'] = QGridLayout()

    def build(self):
        # build main layout
        mainl = self.layouts['main']
        mainl.addWidget(self.widgets['connserver'], 0, 0)
        mainl.addWidget(self.widgets['dothing'], 0, 1)


        self.widgets['main'].setLayout(mainl)

        self.setCentralWidget(self.widgets['main'])

    # ## ACTIONS AND SIGNALS## #
    def dothing(self):
        # send
        self.sock.sendall(str('htm dothing').encode())

        # receive
        data = self.sock.recv(1024)

    def connect_server(self):
        HOST = '10.0.0.16'
        PORT = 50042
        self.sock = socket.create_connection((HOST, PORT))

    def botlistsig(self):
        # send
        self.sock.sendall(str('botlist').encode())

        # receive
        data = self.sock.recv(1024)

        # process
        print('Received', data.decode())
        self.bots = json.loads(data.decode())

# QT IT UP
app = QApplication(sys.argv)

# initalize classes
win = SimplePodcast()

# execute, clean up, and exit
sys.exit(app.exec_())
