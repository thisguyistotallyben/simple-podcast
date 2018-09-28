import time
import sys
import json
import calendar
from datetime import datetime
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

from modules import podbean, menubuilder


class Settings(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        # parental issues
        self.parent = parent

        # setup window
        self.title = 'Settings'
        self.left = 60
        self.top = 50
        self.width = 300
        self.height = 300
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # widgets
        self.main = QWidget()
        self.authbox = QGroupBox('Podbean Authentication')
        self.authidl = QLabel('Client ID')
        self.authid = QLineEdit()
        self.authsecretl = QLabel('Client Secret')
        self.authsecret = QLineEdit()
        self.authbutt = QPushButton('Update')

        self.authid.setDisabled(True)
        self.authsecret.setDisabled(True)
        self.authid.setText(self.parent.config['podbean']['id'])
        self.authsecret.setText(self.parent.config['podbean']['secret'])

        self.authbutt.clicked.connect(self.cred_update_sig)

        # layouts
        self.authlay = QGridLayout()
        self.lay = QGridLayout()
        self.authbox.setLayout(self.authlay)
        self.main.setLayout(self.lay)

        # put things in the stuff
        self.authlay.addWidget(self.authidl, 0, 0)
        self.authlay.addWidget(self.authid, 0, 1, 1, 2)
        self.authlay.addWidget(self.authsecretl, 1, 0)
        self.authlay.addWidget(self.authsecret, 1, 1, 1, 2)
        self.authlay.addWidget(self.authbutt, 2, 0)

        self.lay.addWidget(self.authbox)
        self.lay.setRowStretch(1, 4)

        self.setCentralWidget(self.main)

        # to get it on top
        self.raise_()

    def cred_update_sig(self):
        state = self.authbutt.text()

        if state == 'Update':
            self.authid.setDisabled(False)
            self.authsecret.setDisabled(False)
            self.authbutt.setText('Set')

        if state == 'Set':
            self.authid.setDisabled(True)
            self.authsecret.setDisabled(True)
            self.authbutt.setText('Update')
        '''
        id = self.authid.text()
        secret = self.authsecret.text()
        self.parent.pb.update_credentials(id, secret)
        '''


class SimplePodcast(QtWidgets.QMainWindow):
    def __init__(self):
        # formalities
        super().__init__()

        # window variables
        self.title = 'Simple Podcast'
        self.left = 50
        self.top = 50
        self.width = 400
        self.height = 100

        # setup menu
        self.mb = menubuilder.MenuBuilder()
        self.menub = self.menuBar()
        self.menu = self.mb.generate(self, 'config/menu.json')
        self.mb.set(self.menu, self.menub)

        # load config file
        with open('config/config.json') as f:
            self.config = json.load(f)
        print(self.config)

        # start podbean service
        pbid = self.config['podbean']['id']
        pbsecret = self.config['podbean']['secret']
        self.pb = podbean.Podbean(pbid, pbsecret)

        # audio file
        self.audio_file = ''

        # setup
        self.setupWindow()
        self.setupWidgets()
        self.setupLayouts()
        self.build()

        # settings dialog
        self.settings = Settings(self)

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
        self.widgets['record-file'] = QPushButton('Choose file')
        self.widgets['record-text'] = QLabel('No audio selected')

        # upload box
        self.widgets['upload-box'] = QGroupBox('Step 3: Upload')
        self.widgets['upload-publish'] = QRadioButton('Publish')
        self.widgets['upload-draft'] = QRadioButton('Draft')
        self.widgets['upload'] = QPushButton('Upload podcast')
        self.widgets['upload-prog'] = QProgressBar()
        self.widgets['upload-text'] = QLabel()

        # connect
        self.widgets['upload'].clicked.connect(self.upload_sig)
        self.widgets['record-file'].clicked.connect(self.file_sig)

        # setup
        self.widgets['upload-publish'].setChecked(True)

        '''
        THIS PART IS SPECIFIC TO A CHURCH PODCAST AUTO NAMING SCHEME
        IF YOU DO NOT WANT THIS, REMOVE THIS SECTION
        '''

        # get time
        t = datetime.now()
        year = t.year
        month = calendar.month_name[t.month]
        day = t.day

        title = ''

        if t.hour < 14:
            title = 'Morning'
        else:
            title = 'Evening'

        title = f'{title} Service - {month} {day}, {year}'
        self.widgets['episode-title-text'].setText(title)

        '''
        END OF SECTION
        '''

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
        recl.addWidget(self.widgets['record-file'], 0, 0)
        recl.addWidget(self.widgets['record-text'], 0, 1)
        recl.setColumnStretch(1, 4)

        # build upload box layout
        upl = self.layouts['upload']
        upl.addWidget(self.widgets['upload-publish'], 0, 1)
        upl.addWidget(self.widgets['upload-draft'], 0, 2)
        upl.addWidget(self.widgets['upload'], 0, 0)
        upl.addWidget(self.widgets['upload-prog'], 1, 0, 1, 3)
        upl.addWidget(self.widgets['upload-text'], 2, 0, 1, 3)
        upl.setColumnStretch(0, 4)

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

    def settings_sig(self):
        #self.pbc.exec_()
        self.settings.show()

    def file_sig(self):
        loc = self.config['last audio location']
        name, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            loc,
            filter='*.mp3')
        if name != '':
            filepath = name.rsplit('/', 1)
            # get location and store it for next time
            self.config['last audio location'] = filepath[0]
            with open('config/config.json', 'w') as f:
                json.dump(self.settings, f)
            self.widgets['record-text'].setText(filepath[1])

    def upload_sig(self):
        # dictionaries take too long to type
        butt = self.widgets['upload']
        prog = self.widgets['upload-prog']
        text = self.widgets['upload-text']
        eptype = ''

        # get episode type
        if self.widgets['upload-publish'].isChecked():
            status = 'publish'
        else:
            status = 'draft'

        # set GUI
        butt.setDisabled(True)
        prog.setDisabled(False)
        prog.setValue(0)

        # big ol' try/catch
        try:
            akey = ''
            pkey = ''

            # login
            text.setText('Logging in ...')
            text.repaint()
            self.pb.auth()
            prog.setValue(33)

            # upload file
            text.setText('Uploading audio ...')
            text.repaint()
            #akey = self.pb.upload_file('audio.madeupext')
            #pkey = self.pb.upload_file('/home/ben/church.jpg')
            prog.setValue(66)

            # get episode deets
            text.setText('Publishing episode ...')
            text.repaint()
            title = self.widgets['episode-title-text'].text()
            desc = self.widgets['episode-desc-text'].toPlainText()

            # the for-realsies publishing part
            self.pb.publish_episode(
                title=title,
                content=desc,
                status=status,
                logo_key='',
                media_key=akey)

            prog.setValue(100)
            text.setText('Episode published')
        except podbean.PodbeanError as e:
            prog.setDisabled(True)
            butt.setDisabled(False)
            text.setText(f'{text.text()} failed')
            print(f'stage: {e.stage}\nreason: {e.reason}')

    def clean(self):
        print('cleanup')

# QT IT UP
app = QApplication(sys.argv)

# initalize classes
win = SimplePodcast()

# execute, clean up, and exit
sys.exit(app.exec_())
