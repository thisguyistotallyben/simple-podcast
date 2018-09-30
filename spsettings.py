from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton,\
    QLabel, QLineEdit, QGroupBox, QPlainTextEdit, QProgressBar, QGroupBox,\
    QPlainTextEdit, QRadioButton, QFileDialog, QGridLayout


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
        self.height = 200
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
        self.authlay.setColumnStretch(1, 4)

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
