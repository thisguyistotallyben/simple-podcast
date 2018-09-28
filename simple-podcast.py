import time
import sys
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

from modules import podbean, menubuilder


class PodbeanCreds(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PodbeanCreds, self).__init__(parent)
        self.idlabel = QLabel('Client ID')
        self.secretlabel = QLabel('Client Secret')
        self.id = QtWidgets.QLineEdit(self)
        self.secret = QtWidgets.QLineEdit(self)
        self.set = QtWidgets.QPushButton('Set', self)
        self.set.clicked.connect(self.handleLogin)
        layout = QGridLayout(self)
        layout.addWidget(self.idlabel, 0, 0)
        layout.addWidget(self.id, 0, 1)
        layout.addWidget(self.secretlabel, 1, 0)
        layout.addWidget(self.secret, 1, 1)
        layout.addWidget(self.set, 2, 0, 1, 2)

    def handleLogin(self):
        if (self.id.text() == 'foo' and
            self.secret.text() == 'bar'):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')

    def enter_creds(self):
        self.exec_()



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

        # setup menu
        self.mb = menubuilder.MenuBuilder()
        self.menub = self.menuBar()
        self.menu = self.mb.generate(self, 'config/menu.json')
        self.mb.set(self.menu, self.menub)

        # load config file
        with open('config/config.json') as f:
            self.settings = json.load(f)
        print(self.settings)

        self.pbc = PodbeanCreds(self)

        # start podbean service
        pbid = self.settings['podbean']['id']
        pbsecret = self.settings['podbean']['secret']
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
        self.widgets['record-file'] = QPushButton('Choose file')
        self.widgets['record-text'] = QLineEdit()

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

        #self.widgets['upload-publish'].toggled.connect\
        #    (lambda:self.btnstate(self.b1))

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

        # build upload box layout
        upl = self.layouts['upload']
        upl.addWidget(self.widgets['upload-publish'], 0, 1)
        upl.addWidget(self.widgets['upload-draft'], 0, 2)
        upl.addWidget(self.widgets['upload'], 1, 0, 1, 3)
        upl.addWidget(self.widgets['upload-prog'], 2, 0, 1, 3)
        upl.addWidget(self.widgets['upload-text'], 3, 0, 1, 3)
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

    def creds_sig(self):
        self.pbc.exec_()

    def file_sig(self):
        loc = self.settings['last file location']
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', loc)
        if name != '':
            # get location and store it for next time
            print(name.rsplit('/', 1))

    def upload_sig(self):
        # dictionaries are long to type
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
            # login
            text.setText('Logging in ...')
            text.repaint()
            self.pb.auth()
            prog.setValue(33)

            # upload file
            text.setText('Uploading audio ...')
            text.repaint()
            #akey = self.pb.upload_file('audio.madeupext')
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
                status=status)#,
                #media_key=akey)

            prog.setValue(100)
            text.setText('Episode published')
        except podbean.PodbeanError as e:
            prog.setDisabled(True)
            butt.setDisabled(False)
            text.setText(f'{text.text()} failed')
            print(f'stage: {e.stage}\nreason: {e.reason}')


        '''
        if self.pb.auth():
            prog.setValue(33)
        else:
            text.setText('Login ... Failed')

        # upload audio file
        text.setText('Uploading audio ...')
        text.repaint()
        try:
            akey = self.pb.upload_file('audio.madeupext')
        except podbean.PodbeanError as e:
            print(f'UH OH REASON: {e.reason}')
            return
        prog.setValue(66)

        # publish
        title = self.widgets['episode-title-text'].text()
        desc = self.widgets['episode-desc-text'].toPlainText()
        text.setText('Publishing episode ...')
        text.repaint()
        self.pb.publish_episode(title=title, content=desc, media_key=akey)
        # prog.setDisabled(True) # not really for anything
        # self.pb.publish_episode(title, desc, None, None)
        prog.setValue(100)
        text.setText('Episode published')
        butt.setDisabled(False)
        '''
    def clean(self):
        print('cleanup')

# QT IT UP
app = QApplication(sys.argv)

# initalize classes
win = SimplePodcast()

# execute, clean up, and exit
sys.exit(app.exec_())
