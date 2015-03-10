__author__ = 'ryan'
"""
Use this is create connections with databases.
"""
from PyQt4 import QtSql, QtCore, QtGui
import threading


def default_connection():
    """
    Creates a new connection using the default connection name.
    'reader' user should only have Select permissions
    Returns false if the connection couldn't be made.
    """

    QtSql.QSqlDatabase.database('qt_sql_default_connection').close()
    QtSql.QSqlDatabase.removeDatabase('qt_sql_default_connection')
    db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
    host, database = read_settings("default")
    db.setUserName('fab')
    db.setPassword('doylefab')
    db.setHostName(host)
    db.setDatabaseName(database)
    if db.open():
        return True
    else:
        db_err(db)
        return False


def new_connection(name, user, password, host=None, database=None):
    """
    Returns a new connection named 'name'. 'user' and 'password'
    must be supplied. Use this function to create a privileged
    connection or to connect to a different server.

    If a connection named 'name' already exists it returns that
    connection instead of making a new connection. New connections
    "timeout" after 10 minutes and are removed.

    Returns an empty connection and False if the new connection
    could not be made.
    """
    if QtSql.QSqlDatabase.database(name).open():
        db = QtSql.QSqlDatabase.database(name)
        return db, True
    else:
        if host is None or database is None:
            host, database = read_settings(name)
        db = QtSql.QSqlDatabase.addDatabase("QMYSQL", name)
        db.setUserName(user)
        db.setHostName(host)
        db.setDatabaseName(database)
        db.setPassword(password)
        if db.open():
            dbt = threading.Timer(600, close_connection, args=[name])
            dbt.start()
            return db, True
        else:
            db_err(db)
            return None, False


def check_connection():
    """
    Keeps the connection from timing out and throwing a bunch
    of errors at the user.
    """
    qry = QtSql.QSqlQuery()
    try:
        if qry.exec_("Select name from user"):
            return True, None
        else:
            print("Connection Checked - Error")
            return False, qry.lastError().text()
    except Exception:
        print("Connection Checked - Failed")
        return False, qry.lastError().text()


def close_connection(name):
    """
    Close and remove the connection 'name' if it is open.
    """
    if QtSql.QSqlDatabase.database(name).open():
        QtSql.QSqlDatabase.database(name).close()
    QtSql.QSqlDatabase.removeDatabase(name)
    print("Connection closed. New connection required")


def close_all_connections():
    """
    Loops all connections, closes and removes them.
    """
    for name in QtSql.QSqlDatabase.connectionNames():
        if QtSql.QSqlDatabase.database(name).open():
            QtSql.QSqlDatabase.database(name).close()
        QtSql.QSqlDatabase.removeDatabase(name)


def db_err(qry):
    """
    This error is used extensively.
    """
    if qry is None:
        QtGui.QMessageBox.critical(None, "Database Error", "An unknown error occurred")
    else:
        QtGui.QMessageBox.critical(None, "Database Error", qry.lastError().text())
    return


'''
Settings Block
Reads and saves database settings across sessions.
'''


def write_settings(host, database, group):
    settings = QtCore.QSettings("Doyle Mfg", "Parts SOS")
    settings.setDefaultFormat(1)
    settings.beginGroup(group)
    settings.setValue('host', str(host))
    settings.setValue('database', str(database))
    settings.endGroup()


def read_settings(group):
    settings = QtCore.QSettings("Doyle Mfg", "Parts SOS")
    settings.setDefaultFormat(1)
    settings.beginGroup(group)
    host = settings.value('host', None)
    database = settings.value('database', None)
    if host is None or database is None:
        dbs = DatabaseSettings()
        while host is None or database is None:
            host, database = dbs.get_data(group)
        write_settings(host, database, group)
    else:
        host = host
        database = database
    return host, database


class DatabaseSettings(QtGui.QDialog):
    """
    Opens a dialog to enter network settings if
    there are no settings in the config error.
    """
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setObjectName("Database Settings")
        self.resize(250, 111)
        self.setWindowIcon(QtGui.QIcon(":/icons/appLogo.png"))
        layout = QtGui.QGridLayout(self)
        self.hostname_label = QtGui.QLabel("Hostname", self)
        self.database_label = QtGui.QLabel("Database", self)
        self.hostname = QtGui.QLineEdit(self)
        self.database = QtGui.QLineEdit(self)
        self.buttons = QtGui.QDialogButtonBox(self)
        self.buttons.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)

        layout.addWidget(self.hostname_label, 0, 0)
        layout.addWidget(self.hostname, 0, 1)
        layout.addWidget(self.database_label, 1, 0)
        layout.addWidget(self.database, 1, 1)
        layout.addWidget(self.buttons, 2, 0, 1, 2)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_data(self, name):
        self.setWindowTitle('%s - Database Settings' % name)
        self.exec_()
        host = self.hostname.text()
        database = self.database.text()
        if host != "":
            if database != "":
                return host, database
            else:
                self.database.setFocus()
                return host, None
        else:
            self.hostname.setFocus()
            return None, None

    def reject(self):
        self.done(0)





