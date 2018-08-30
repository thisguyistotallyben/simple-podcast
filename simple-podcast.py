import time
import sys
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

from modules import audio, podbean, menubuilder


class SimplePodcast(QtWidgets.QMainWindow):
    def __init__(self):
        # formalities
        super().__init__()

        # window variables
        self.title = 'Simple Podcast'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 100

        # start audio
        self.audio = audio.Audio()

        # setup menu
        self.mb = menubuilder.MenuBuilder()
        self.menub = self.menuBar()
        self.menu = self.mb.generate(self, 'config/menu.json')
        self.mb.set(self.menu, self.menub)

        # start podbean service
        with open('config/podbean.txt', 'r') as f:
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

        # episode box
        self.widgets['episode-box'] = QGroupBox('Step 1: Episode Info')
        self.widgets['episode-title'] = QLabel('Title')
        self.widgets['episode-title-text'] = QLineEdit()
        self.widgets['episode-desc'] = QLabel('Description')
        self.widgets['episode-desc-text'] = QPlainTextEdit()

        # record box
        self.widgets['record-box'] = QGroupBox('Step 2: Get Audio')
        self.widgets['record-start'] = QPushButton('Start recording')
        self.widgets['record-stop'] = QPushButton('Stop recording')

        # upload box
        self.widgets['upload-box'] = QGroupBox('Step 3: Upload')
        self.widgets['upload'] = QPushButton('Upload podcast')
        self.widgets['upload-prog'] = QProgressBar()
        self.widgets['upload-text'] = QLabel()

        # connect
        self.widgets['record-start'].clicked.connect(self.record_start_sig)
        self.widgets['record-stop'].clicked.connect(self.record_stop_sig)
        self.widgets['upload'].clicked.connect(self.upload_sig)

        # options
        self.widgets['record-stop'].setDisabled(True)
        self.widgets['upload-prog'].setDisabled(True)

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
        mainl.addWidget(self.widgets['episode-box'], 0, 0)
        mainl.addWidget(self.widgets['record-box'], 1, 0)
        mainl.addWidget(self.widgets['upload-box'], 2, 0)

        # build record box layout
        recl = self.layouts['record']
        recl.addWidget(self.widgets['record-start'], 0, 0)
        recl.addWidget(self.widgets['record-stop'], 0, 1)

        # build upload box layout
        upl = self.layouts['upload']
        upl.addWidget(self.widgets['upload'], 0, 0)
        upl.addWidget(self.widgets['upload-prog'], 1, 0)
        upl.addWidget(self.widgets['upload-text'], 2, 0)

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
        # dictionaries are long to type
        butt = self.widgets['upload']
        prog = self.widgets['upload-prog']
        text = self.widgets['upload-text']

        # set disabilities
        butt.setDisabled(True)
        prog.setDisabled(False)

        # login
        text.setText('Logging in ...')
        text.repaint()
        if self.pb.auth():
            prog.setValue(33)
        else:
            text.setText('Login ... Failed')

        # upload audio file
        text.setText('Uploading audio ...')
        text.repaint()
        self.pb.upload_file('testaudio.mp3')
        prog.setValue(66)

        # publish
        title = self.widgets['episode-title-text'].text()
        desc = self.widgets['episode-desc-text'].toPlainText()
        print(title, desc)
        prog.setDisabled(True) # not really for anything
        # self.pb.publish_episode(title, desc, None, None)


        '''
        self.pb.auth()
        '''

# QT IT UP
app = QApplication(sys.argv)

# initalize classes
win = SimplePodcast()

# execute, clean up, and exit
sys.exit(app.exec_())
