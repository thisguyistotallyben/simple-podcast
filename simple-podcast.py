import time
import sys
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

import audio
import podbean


class SimplePodcast(QtWidgets.QMainWindow):
    def __init__(self):
        # formalities
        super().__init__()

        # window variables
        self.title = 'Simple Podast'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 100

        # start audio
        self.audio = audio.Audio()

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

        # main widget
        self.widgets['main'] = QWidget()

        # record box
        self.widgets['record-box'] = QGroupBox('Step 1: Record')
        self.widgets['record-start'] = QPushButton('Start recording')
        self.widgets['record-stop'] = QPushButton('Stop recording')

        # upload box
        self.widgets['upload-box'] = QGroupBox('Step 2: Upload')
        self.widgets['upload'] = QPushButton('Upload podcast')
        self.widgets['upload-login'] = QLabel('Login')
        self.widgets['upload-audio'] = QLabel('Uploading audio')

        # episode box
        self.widgets['episode-box'] = QGroupBox('Episode Info')
        self.widgets['episode-title'] = QLabel('Title')
        self.widgets['episode-title-text'] = QLineEdit()
        self.widgets['episode-desc'] = QLabel('Description')
        self.widgets['episode-desc-text'] = QPlainTextEdit()

        # connect
        self.widgets['record-start'].clicked.connect(self.record_start_sig)
        self.widgets['record-stop'].clicked.connect(self.record_stop_sig)
        self.widgets['upload'].clicked.connect(self.upload_sig)

        # options
        self.widgets['record-stop'].setDisabled(True)
        self.widgets['upload-login'].setDisabled(True)
        self.widgets['upload-audio'].setDisabled(True)

    def setupLayouts(self):
        self.layouts = {}

        # define
        self.layouts['main'] = QGridLayout()
        self.layouts['record'] = QGridLayout()
        self.layouts['upload'] = QGridLayout()
        self.layouts['episode'] = QGridLayout()

    def build(self):
        # build main layout
        mainl = self.layouts['main']
        mainl.addWidget(self.widgets['record-box'], 0, 0)
        mainl.addWidget(self.widgets['upload-box'], 1, 0)

        # build record box layout
        recl = self.layouts['record']
        recl.addWidget(self.widgets['record-start'], 0, 0)
        recl.addWidget(self.widgets['record-stop'], 0, 1)

        # build upload box layout
        upl = self.layouts['upload']
        upl.addWidget(self.widgets['episode-box'], 0, 0)
        upl.addWidget(self.widgets['upload'], 1, 0)
        upl.addWidget(self.widgets['upload-login'], 2, 0)
        upl.addWidget(self.widgets['upload-audio'], 3, 0)
        upl.setRowStretch(4,4)

        # build episode box layout
        epl = self.layouts['episode']
        epl.addWidget(self.widgets['episode-title'], 0, 0)
        epl.addWidget(self.widgets['episode-title-text'], 0, 1)
        epl.addWidget(self.widgets['episode-desc'], 1, 0)
        epl.addWidget(self.widgets['episode-desc-text'], 1, 1)

        # set layouts
        self.widgets['main'].setLayout(mainl)
        self.widgets['record-box'].setLayout(recl)
        self.widgets['upload-box'].setLayout(upl)
        self.widgets['episode-box'].setLayout(epl)

        self.setCentralWidget(self.widgets['main'])

    # ## ACTIONS AND SIGNALS ## #

    def record_start_sig(self):
        self.audio.start()
        self.widgets['record-start'].setDisabled(True)
        self.widgets['record-stop'].setDisabled(False)

    def record_stop_sig(self):
        self.audio.stop()
        self.widgets['record-start'].setDisabled(False)
        self.widgets['record-stop'].setDisabled(True)

    def upload_sig(self):
        # I don't even know yet
        print('fake uploading')

        # login
        self.widgets['upload-login'].setDisabled(False)
        self.widgets['upload-login'].setText('Login ...')
        self.widgets['upload-login'].repaint()
        if self.pb.auth():
            self.widgets['upload-login'].setText('Login ... Success')
            self.widgets['upload-login'].setDisabled(True)
        else:
            self.widgets['upload-login'].setText('Login ... Failed')

        # upload audio file
        self.widgets['upload-audio'].setDisabled(False)
        self.widgets['upload-audio'].setText('Uploading audio ...')
        self.widgets['upload-audio'].repaint()


        '''
        self.pb.auth()
        '''

# QT IT UP
app = QApplication(sys.argv)

# initalize classes
win = SimplePodcast()

# execute, clean up, and exit
sys.exit(app.exec_())
