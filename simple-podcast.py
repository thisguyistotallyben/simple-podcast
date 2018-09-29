import time
import sys
import json
import calendar
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton,\
    QLabel, QLineEdit, QGroupBox, QPlainTextEdit, QProgressBar, QGroupBox,\
    QPlainTextEdit, QRadioButton, QFileDialog, QGridLayout

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

        self.defbox = QGroupBox('Default Podcast Logo')
        self.defbutt = QPushButton('Choose File')
        self.deftext = QLabel()

        self.defbutt.clicked.connect(self.deflogo_sig)

        logo = self.parent.config['default logo']
        if logo == '':
            self.deftext.setText('No default logo chosen')
        else:
            self.deftext.setText(logo)

        # layouts
        self.authlay = QGridLayout()
        self.deflay = QGridLayout()
        self.lay = QGridLayout()
        self.authbox.setLayout(self.authlay)
        self.defbox.setLayout(self.deflay)
        self.main.setLayout(self.lay)

        # put things in the stuff
        self.authlay.addWidget(self.authidl, 0, 0)
        self.authlay.addWidget(self.authid, 0, 1, 1, 2)
        self.authlay.addWidget(self.authsecretl, 1, 0)
        self.authlay.addWidget(self.authsecret, 1, 1, 1, 2)
        self.authlay.addWidget(self.authbutt, 2, 0)

        self.deflay.addWidget(self.defbutt, 0, 0)
        self.deflay.addWidget(self.deftext, 0, 1)
        self.deflay.setColumnStretch(1, 4)

        self.lay.addWidget(self.authbox)
        self.lay.addWidget(self.defbox)
        self.lay.setRowStretch(2, 4)

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
            # set GUI
            self.authid.setDisabled(True)
            self.authsecret.setDisabled(True)
            self.authbutt.setText('Setting...')
            self.authbutt.repaint()

            # update everything
            id = self.authid.text()
            secret = self.authsecret.text()

            self.parent.config['podbean']['id'] = id
            self.parent.config['podbean']['secret'] = secret
            self.parent.update_config()
            self.parent.pb.update_credentials(id, secret)
            self.authbutt.setText('Update')

        '''
        id = self.authid.text()
        secret = self.authsecret.text()
        self.parent.pb.update_credentials(id, secret)
        '''

    def deflogo_sig(self):
        loc = self.parent.config['last image location']
        name, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            loc,
            filter='Images (*.jpg *.JPG *.jpeg *.JPEG *.png *.PNG);;*')
        if name != '':
            filepath = name.rsplit('/', 1)
            # get location and store it for next time
            self.parent.config['last image location'] = filepath[0]
            self.parent.config['default logo'] = name
            self.parent.update_config()

            # update GUI
            self.deftext.setText(filepath[1])
            self.parent.widgets['logo-text'].setText(filepath[1])
            self.parent.logo_file = name


class SimplePodcast(QMainWindow):
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
        print('Config file loaded')

        # start podbean service
        pbid = self.config['podbean']['id']
        pbsecret = self.config['podbean']['secret']
        self.pb = podbean.Podbean(pbid, pbsecret)

        # audio file
        self.audio_file = ''
        self.logo_file = self.config['default logo']

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

        # audio box
        self.widgets['audio-box'] = QGroupBox('Step 2: Select Audio')
        self.widgets['audio-file'] = QPushButton('Choose file')
        self.widgets['audio-text'] = QLabel('No audio selected')

        # logo box
        self.widgets['logo-box'] = QGroupBox('Step 3: Select Logo')
        self.widgets['logo-file'] = QPushButton('Choose File')
        self.widgets['logo-text'] = QLabel('No image selected')

        # upload box
        self.widgets['upload-box'] = QGroupBox('Step 4: Upload')
        self.widgets['upload-publish'] = QRadioButton('Publish')
        self.widgets['upload-draft'] = QRadioButton('Draft')
        self.widgets['upload'] = QPushButton('Upload podcast')
        self.widgets['upload-prog'] = QProgressBar()
        self.widgets['upload-text'] = QLabel()

        # connect
        self.widgets['upload'].clicked.connect(self.upload_sig)
        self.widgets['audio-file'].clicked.connect(self.audio_sig)
        self.widgets['logo-file'].clicked.connect(self.logo_sig)

        # setup
        self.widgets['upload-publish'].setChecked(True)

        logo = self.config['default logo']
        if logo != '':
            self.widgets['logo-text'].setText(logo.rsplit('/', 1)[1])

        '''
        THIS PART IS SPECIFIC TO A CHURCH PODCAST AUTO NAMING SCHEME
        IF YOU DO NOT WANT THIS, REMOVE THIS SECTION
        '''

        # get time
        t = datetime.now()
        year = t.year
        month = calendar.month_name[t.month]
        day = t.day

        # set title
        title = ''
        if t.hour < 14:
            title = 'Morning'
        else:
            title = 'Evening'
        title = f'{title} Service - {month} {day}, {year}'

        # set title box
        self.widgets['episode-title-text'].setText(title)

        '''
        END OF SECTION
        '''

    def setupLayouts(self):
        self.layouts = {}

        # define
        self.layouts['main'] = QGridLayout()
        self.layouts['audio'] = QGridLayout()
        self.layouts['logo'] = QGridLayout()
        self.layouts['upload'] = QGridLayout()
        self.layouts['episode'] = QGridLayout()

    def build(self):
        # build main layout
        mainl = self.layouts['main']
        mainl.addWidget(self.widgets['episode-box'], 0, 0)
        mainl.addWidget(self.widgets['audio-box'], 1, 0)
        mainl.addWidget(self.widgets['logo-box'], 2, 0)
        mainl.addWidget(self.widgets['upload-box'], 3, 0)

        # build audio box layout
        recl = self.layouts['audio']
        recl.addWidget(self.widgets['audio-file'], 0, 0)
        recl.addWidget(self.widgets['audio-text'], 0, 1)
        recl.setColumnStretch(1, 4)

        # build logo box layout
        logl = self.layouts['logo']
        logl.addWidget(self.widgets['logo-file'], 0, 0)
        logl.addWidget(self.widgets['logo-text'], 0, 1)
        logl.setColumnStretch(1, 4)

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
        self.widgets['audio-box'].setLayout(recl)
        self.widgets['logo-box'].setLayout(logl)
        self.widgets['upload-box'].setLayout(upl)
        self.widgets['episode-box'].setLayout(epl)

        self.setCentralWidget(self.widgets['main'])

    # ## ACTIONS AND SIGNALS ## #

    def settings_sig(self):
        self.settings.show()

    def audio_sig(self):
        loc = self.config['last audio location']
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', loc,
                                              filter='*.mp3')
        if name != '':
            self.audio_file
            filepath = name.rsplit('/', 1)
            # get location and store it for next time
            self.config['last audio location'] = filepath[0]
            self.update_config()
            self.widgets['audio-text'].setText(filepath[1])

    def logo_sig(self):
        loc = self.config['last image location']
        name, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            loc,
            filter='Images (*.jpg *.JPG *.jpeg *.JPEG *.png *.PNG)')
        if name != '':
            filepath = name.rsplit('/', 1)
            # get location and store it for next time
            self.config['last image location'] = filepath[0]
            self.update_config()
            self.widgets['logo-text'].setText(filepath[1])

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
            # akey = self.pb.upload_file('audio.madeupext')
            # pkey = self.pb.upload_file('/home/ben/church.jpg')
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
            print('HEERE HERE HERE HERE')
            prog.setDisabled(True)
            butt.setDisabled(False)
            text.setText(f'{text.text()} failed ({e.reason})')
            print(f'stage: {e.stage}\nreason: {e.reason}')
            return

    def update_config(self):
        with open('config/config.json', 'w') as f:
            json.dump(self.config, f)


# QT IT UP
app = QApplication(sys.argv)

# initalize classes
win = SimplePodcast()

# execute, clean up, and exit
sys.exit(app.exec_())
