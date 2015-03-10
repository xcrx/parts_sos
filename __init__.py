__author__ = 'ryan'

import sys
from PyQt4 import QtGui

from main import Main

import database_connection

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    if not database_connection.default_connection():
        sys.exit(1)
    myapp = Main()
    myapp.show()
    sys.exit(app.exec_())