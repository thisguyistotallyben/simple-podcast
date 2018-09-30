'''
Author:  Benjamin Johnson
Version: 1.0
Purpose: A simple dialog for quickly uploading podcast episodes to the Podbean
         service.  Parts of this program are tailored for church podcasting and
         are labelled so they can be removed for more general purposes.
'''

import time
import sys
import json
import calendar
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton,\
    QLabel, QLineEdit, QGroupBox, QPlainTextEdit, QProgressBar, QGroupBox,\
    QPlainTextEdit, QRadioButton, QFileDialog, QGridLayout, QMessageBox

from spsettings import Settings
from modules import podbean, menubuilder


class SimplePodcast(QMainWindow):
    def __init__(self):
        # formalities
        super().__init__()

        # load config file
        with open('config/config.json') as f:
            self.config = json.load(f)
        print('Config file loaded')

        # start podbean service
        pbid = self.config['podbean']['id']
        pbsecret = self.config['podbean']['secret']
        self.pb = podbean.Podbean(pbid, pbsecret)

        # setup
        self.setupWindow()
        self.setupWidgets()
        self.setupLayouts()
        self.build()

        # set state
        self.set_default_state()

        # settings dialog
        self.settings = Settings(self)

        # show
        self.show()

    def setupWindow(self):
        # variables
        self.title = 'Simple Podcast'
        self.left = 50
        self.top = 50
        self.width = 400
        self.height = 100

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # menu
        self.mb = menubuilder.MenuBuilder()
        self.menub = self.menuBar()
        self.menu = self.mb.generate(self, 'config/menu.json')
        self.mb.set(self.menu, self.menub)

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
        self.widgets['audio-text'] = QLabel()

        # logo box
        self.widgets['logo-box'] = QGroupBox('Step 3: Select Logo')
        self.widgets['logo-file'] = QPushButton('Choose File')
        self.widgets['logo-text'] = QLabel()

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

        # build episode box layout
        epl = self.layouts['episode']
        epl.addWidget(self.widgets['episode-title'], 0, 0)
        epl.addWidget(self.widgets['episode-title-text'], 0, 1)
        epl.addWidget(self.widgets['episode-desc'], 1, 0)
        epl.addWidget(self.widgets['episode-desc-text'], 1, 1)

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

        # set layouts
        self.widgets['main'].setLayout(mainl)
        self.widgets['audio-box'].setLayout(recl)
        self.widgets['logo-box'].setLayout(logl)
        self.widgets['upload-box'].setLayout(upl)
        self.widgets['episode-box'].setLayout(epl)

        self.setCentralWidget(self.widgets['main'])

    '''
    SIGNALS
    '''

    def settings_sig(self):
        self.settings.show()

    def about_sig(self):
        QMessageBox.about(self, 'About',
                          ('Simple Podcast\n\n'
                           'Author - Benjamin Johnson\n'
                           'Version - 1.0'))

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

        # set GUI
        butt.setDisabled(True)
        prog.setDisabled(False)
        prog.setValue(0)

        # big ol' try/catch
        try:
            akey = ''
            lkey = ''

            '''AUTHORIZE'''
            text.setText('Authorizing ...')
            text.repaint()
            self.pb.auth()
            prog.setValue(25)

            '''UPLOAD AUDIO'''
            if self.audio_file != '':
                text.setText('Uploading audio ...')
                text.repaint()
                akey = self.pb.upload_file(self.audio_file)
                prog.setValue(50)

            '''UPLOAD LOGO'''
            if self.logo_file != '':
                text.setText('Uploading logo ...')
                text.repaint()
                lkey = self.pb.upload_file(self.logo_file)
                prog.setValue(75)

            '''UPLOAD PODCAST'''
            text.setText('Uploading episode ...')
            text.repaint()

            # get podcast parameters
            if self.widgets['upload-publish'].isChecked():
                status = 'publish'
            else:
                status = 'draft'
            title = self.widgets['episode-title-text'].text()
            desc = self.widgets['episode-desc-text'].toPlainText()

            # upload to podbean
            self.pb.publish_episode(
                title=title,
                content=desc,
                status=status,
                logo_key=lkey,
                media_key=akey)

            prog.setValue(100)
            text.setText('Episode published')
        except podbean.PodbeanError as e:
            prog.setDisabled(True)
            butt.setDisabled(False)
            text.setText(f'{text.text()} failed ({e.reason})')
            print(f'stage: {e.stage}\nreason: {e.reason}')
            return

    '''
    HELPER FUNCTIONS
    '''

    def set_default_state(self):
        # set variables
        self.audio_file = ''
        self.logo_file = self.config['default logo']

        # set GUI
        self.widgets['episode-title-text'].setText('')
        self.widgets['episode-desc-text'].clear()

        self.widgets['audio-text'].setText('No audio selected')

        logo = self.config['default logo']
        if logo != '':
            self.widgets['logo-text'].setText(logo.rsplit('/', 1)[1])
        else:
            self.widgets['logo-text'].setText('No image selected')

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

    def update_config(self):
        with open('config/config.json', 'w') as f:
            json.dump(self.config, f)


# QT IT UP
app = QApplication(sys.argv)

# initalize classes
win = SimplePodcast()

# execute, clean up, and exit
sys.exit(app.exec_())
