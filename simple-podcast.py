import sys
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

# import audio
import podbean

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

        # start podbean service
        with open('auth/podbean.txt', 'r') as f:
            lines = f.readlines()
            if len(lines) != 2:
                raise IOError()
            else:
                pbid = lines[0].strip()
                pbsecret = lines[1].strip()
                self.pb = podbean.Podbean(pbid, pbsecret)

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
        self.widgets['record-start'] = QPushButton('Start recording')
        self.widgets['record-stop'] = QPushButton('Stop recording')
        self.widgets['upload'] = QPushButton('Upload podcast')
        self.widgets['upload-stats'] = QWidget() # idk yet

        # connect
        self.widgets['record-start'].clicked.connect(self.record_start_sig)
        self.widgets['record-stop'].clicked.connect(self.record_stop_sig)
        self.widgets['upload'].clicked.connect(self.upload_sig)

    def setupLayouts(self):
        self.layouts = {}

        # define
        self.layouts['main'] = QGridLayout()

    def build(self):
        # build main layout
        mainl = self.layouts['main']
        mainl.addWidget(self.widgets['record-start'], 0, 0)
        mainl.addWidget(self.widgets['record-stop'], 0, 1)
        mainl.addWidget(self.widgets['upload'], 1, 0, 1, 2)


        self.widgets['main'].setLayout(mainl)

        self.setCentralWidget(self.widgets['main'])

    # ## ACTIONS AND SIGNALS ## #

    def record_start_sig(self):
        # start recording
        print("fake recording now")

    def record_stop_sig(self):
        # stop recording
        print('fake stopped')

    def upload_sig(self):
        # I don't even know yet
        print('fake uploading')

# QT IT UP
app = QApplication(sys.argv)

# initalize classes
win = SimplePodcast()

# execute, clean up, and exit
sys.exit(app.exec_())
