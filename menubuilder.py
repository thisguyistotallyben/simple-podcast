import json

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *

class MenuBuilder():
    def __init__(self):
        print('Menu Builder init')

    def generate(self, app, fname):
        with open(fname, 'r') as f:
            # grab json
            data = json.load(f)

        menu = {}

        for m in data:
            tmenu = QMenu(m)

            # build the submenu stuff
            for item in data[m]:
                # if separator
                if 'separator' in data[m][item]:
                    tmenu.addSeparator()
                    continue

                # options
                sig = None
                hotkey = ''

                if 'signal' in data[m][item]:
                    sig = getattr(app, data[m][item]['signal'])
                if 'hotkey' in data[m][item]:
                    hotkey = data[m][item]['hotkey']

                # build the action
                taction = QAction(item, tmenu, shortcut=hotkey)
                if sig is not None:
                    taction.triggered.connect(sig)

                # add to menu
                tmenu.addAction(taction)

            # add the menu
            menu[m] = tmenu

        return menu

    def set(self, menu, menub):
        # reset menubar if not empty
        menub.clear()

        # set menu
        for m in menu:
            menub.addAction(menu[m].menuAction())
