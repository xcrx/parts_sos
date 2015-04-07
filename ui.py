__author__ = 'ryan'
from PyQt4 import QtCore, QtGui
from query import query
import colors
import graphics


class LoginForm(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        
        self.setObjectName("login_form")
        self.setWindowFlags(QtCore.Qt.Popup)
        self.setMouseTracking(True)
        self.resize(250, 75)

        palette = colors.tan()
        self.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Source Code Pro Medium")
        self.setFont(font)

        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setMargin(6)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")

        self.userLabel = QtGui.QLabel(self)
        self.userLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.userLabel.setObjectName("userLabel")
        self.userLabel.setText("User:")
        self.gridLayout.addWidget(self.userLabel, 0, 0, 1, 1)

        self.user = QtGui.QComboBox(self)
        self.user.setObjectName("user")
        self.user_id = 0
        self.username = ""
        self.gridLayout.addWidget(self.user, 0, 1, 1, 1)

        self.passwordLabel = QtGui.QLabel(self)
        self.passwordLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.passwordLabel.setObjectName("passwordLabel")
        self.passwordLabel.setText("Password:")
        self.gridLayout.addWidget(self.passwordLabel, 1, 0, 1, 1)

        self.password = QtGui.QLineEdit(self)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 1, 1, 1, 1)

        self.buttons = QtGui.QDialogButtonBox(self)
        self.buttons.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttons.setCenterButtons(False)
        self.buttons.setObjectName("buttons")
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.gridLayout.addWidget(self.buttons, 2, 0, 1, 2)

        self.bad_pass = QtGui.QLabel(self)
        self.bad_pass.setObjectName("bad_pass")
        self.bad_pass.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.bad_pass.setText("<strong>Bad Password")
        red_text = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        red_text.setStyle(QtCore.Qt.SolidPattern)
        pass_palette = self.bad_pass.palette()
        pass_palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, red_text)
        self.bad_pass.setPalette(pass_palette)
        self.bad_pass.setVisible(False)
        self.gridLayout.addWidget(self.bad_pass, 3, 0, 1, 2)

        self.get_users()
        self.user.setFocus()

    def get_users(self):
        users_qry = query("get_users")
        if users_qry:
            self.user.addItem("", 0)
            while users_qry.next():
                self.user.addItem(users_qry.value(1), users_qry.value(0))
        else:
            self.reject()

    def accept(self):
        self.user_id = self.user.itemData(self.user.currentIndex())
        auth_qry = query("auth_user", [self.user_id])
        if auth_qry:
            auth_qry.first()
            if self.password.text() == auth_qry.value(0):
                self.username = self.user.currentText()
                self.done(0)
            else:
                self.bad_pass.setVisible(True)
        else:
            self.reject()

    def resizeEvent(self, resize_event):
        path = QtGui.QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)
        region = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        QtGui.QDialog.resizeEvent(self, resize_event)
        resize_event.accept()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setObjectName("MainWindow")
        self.resize(1024, 768)
        self.setMouseTracking(True)
        self.setWindowIcon(QtGui.QIcon(":/icons/icons/sos_window_icon.png"))
        self.setWindowTitle("Parts S.O.S.")
        self.user_id = 0

        self.setPalette(colors.tan())

        font = QtGui.QFont()
        font.setFamily("Source Code Pro Medium")
        self.setFont(font)

        self.central_widget = QtGui.QWidget(self)
        self.central_widget.setAutoFillBackground(False)
        self.central_widget.setObjectName("central_widget")

        self.central_layout = QtGui.QGridLayout(self.central_widget)
        self.central_layout.setMargin(2)
        self.central_layout.setObjectName("central_layout")

        self.header_frame = QtGui.QFrame(self.central_widget)
        size_ef = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        size_ef.setHorizontalStretch(0)
        size_ef.setVerticalStretch(0)
        size_ef.setHeightForWidth(self.header_frame.sizePolicy().hasHeightForWidth())
        self.header_frame.setSizePolicy(size_ef)
        self.header_frame.setMinimumSize(QtCore.QSize(0, 75))
        self.header_frame.setMaximumSize(QtCore.QSize(16777215, 75))
        self.header_frame.setBaseSize(QtCore.QSize(0, 75))
        self.header_frame.setMouseTracking(False)
        self.header_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.header_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.header_frame.setObjectName("header_frame")

        self.header_layout = QtGui.QGridLayout(self.header_frame)
        self.header_layout.setMargin(2)
        self.header_layout.setObjectName("header_layout")

        header_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.header_layout.addItem(header_spacer, 0, 1, 2, 1)

        self.logo = QtGui.QLabel(self.header_frame)
        size_ee = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        size_ee.setHorizontalStretch(0)
        size_ee.setVerticalStretch(0)
        size_ee.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(size_ee)
        self.logo.setMinimumSize(QtCore.QSize(140, 70))
        self.logo.setSizeIncrement(QtCore.QSize(2, 1))
        self.logo.setBaseSize(QtCore.QSize(140, 70))
        self.logo.setFrameShape(QtGui.QFrame.NoFrame)
        self.logo.setTextFormat(QtCore.Qt.AutoText)
        self.logo.setObjectName("logo")
        self.logo.setPixmap(QtGui.QPixmap(":/icons/icons/sos_logo.png"))
        self.header_layout.addWidget(self.logo, 0, 0, 2, 1)

        self.new_request = QtGui.QPushButton(self.header_frame)
        size_ff = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        size_ff.setHorizontalStretch(0)
        size_ff.setVerticalStretch(0)
        size_ff.setHeightForWidth(self.new_request.sizePolicy().hasHeightForWidth())
        self.new_request.setSizePolicy(size_ff)
        self.new_request.setMinimumSize(QtCore.QSize(32, 32))
        self.new_request.setMaximumSize(QtCore.QSize(32, 32))
        self.new_request.setObjectName("new_request")
        self.new_request.setIcon(QtGui.QIcon(":/icons/icons/sos_new_request.png"))
        self.new_request.setIconSize(QtCore.QSize(24, 24))
        self.header_layout.addWidget(self.new_request, 0, 2, 2, 1)

        self.username = QtGui.QLabel(self.header_frame)
        self.username.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.username.setObjectName("username")
        self.header_layout.addWidget(self.username, 0, 3, 1, 1)

        self.login_time = QtGui.QProgressBar(self.header_frame)
        self.login_time.setMaximum(180)
        self.login_time.setValue(180)
        self.login_time.setAlignment(QtCore.Qt.AlignCenter)
        self.login_time.setTextVisible(False)
        self.login_time.setOrientation(QtCore.Qt.Horizontal)
        self.login_time.setInvertedAppearance(True)
        self.login_time.setFormat("")
        self.login_time.setObjectName("login_time")
        self.login_time.setVisible(False)
        self.header_layout.addWidget(self.login_time, 1, 3, 1, 2)

        self.login = QtGui.QPushButton(self.header_frame)
        self.login.setFlat(True)
        self.login.setObjectName("login")
        self.login.setText("Login")
        self.login.setIcon(QtGui.QIcon(":/icons/icons/sos_login.png"))
        self.header_layout.addWidget(self.login, 0, 4, 1, 1)

        self.show_history = QtGui.QCheckBox(self.header_frame)
        self.show_history.setText("Show Completed Orders")
        self.show_history.setChecked(False)
        self.show_history.setObjectName("show_history")
        self.header_layout.addWidget(self.show_history, 2, 2, 4, 4)

        self.header_layout.setColumnStretch(1, 1)
        self.central_layout.addWidget(self.header_frame, 0, 0, 1, 2)

        self.settings = QtGui.QPushButton(self.central_widget)
        self.settings.setSizePolicy(size_ff)
        self.settings.setMinimumSize(QtCore.QSize(24, 16))
        self.settings.setMaximumSize(QtCore.QSize(24, 16))
        self.settings.setBaseSize(QtCore.QSize(24, 16))
        self.settings.setObjectName("settings")
        self.settings.setText("...")
        self.settings.setVisible(False)
        self.central_layout.addWidget(self.settings, 2, 1, 1, 1)

        self.request_scroll = QtGui.QScrollArea(self.central_widget)
        self.request_scroll.setFrameShape(QtGui.QFrame.StyledPanel)
        self.request_scroll.setFrameShadow(QtGui.QFrame.Sunken)
        self.request_scroll.setMidLineWidth(0)
        self.request_scroll.setWidgetResizable(True)
        self.request_scroll.setObjectName("request_scroll")

        self.request_frame = QtGui.QWidget()
        self.request_frame.setSizePolicy(size_ee)
        self.request_frame.setObjectName("request_frame")
        self.request_layout = QtGui.QVBoxLayout(self.request_frame)
        self.request_layout.setMargin(2)
        self.request_layout.setSpacing(2)
        self.request_layout.setObjectName("request_layout")
        self.request_layout.setAlignment(QtCore.Qt.AlignTop)
        self.request_scroll.setWidget(self.request_frame)
        self.central_layout.addWidget(self.request_scroll, 1, 0, 1, 2)

        bottom_spacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.central_layout.addItem(bottom_spacer, 2, 0, 1, 1)

        self.setCentralWidget(self.central_widget)

        self.login_timer = QtCore.QTimer()
        self.login_timer.timeout.connect(self.timer_update)

        self.status = QtGui.QStatusBar(self)
        self.status.setObjectName("status")
        self.setStatusBar(self.status)

    def timer_update(self):
        i = self.login_time.value() - 1
        if i > 0:
            self.login_time.setValue(i)
        else:
            self.login_timer.stop()
            self.login.click()


class RequestForm(QtGui.QDialog):
    def __init__(self, parent=None, palette=colors.green()):
        QtGui.QDialog.__init__(self, parent)
        self.setObjectName("request_form")
        self.resize(1060, 75)
        size_policy_ef = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        size_policy_ef.setHorizontalStretch(0)
        size_policy_ef.setVerticalStretch(0)
        size_policy_ef.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy_ef)
        self.setMinimumSize(QtCore.QSize(0, 75))
        self.setMaximumSize(QtCore.QSize(16777215, 75))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        font = QtGui.QFont()
        font.setFamily("Source Code Pro Medium")
        font.setPointSize(12)
        self.setFont(font)

        self.request_layout = QtGui.QGridLayout(self)
        self.request_layout.setMargin(2)
        self.request_layout.setVerticalSpacing(1)
        self.request_layout.setObjectName("request_layout")

        self.request_id = QtGui.QLabel(self)
        size_policy_mf = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        size_policy_mf.setHorizontalStretch(0)
        size_policy_mf.setVerticalStretch(0)
        size_policy_mf.setHeightForWidth(self.request_id.sizePolicy().hasHeightForWidth())
        self.request_id.setSizePolicy(size_policy_mf)
        self.request_id.setMinimumSize(QtCore.QSize(24, 24))
        self.request_id.setMaximumSize(QtCore.QSize(48, 24))
        self.request_id.setObjectName("request_id")
        self.request_layout.addWidget(self.request_id, 0, 0, 1, 1)

        self.need_by = QtGui.QLabel(self)
        self.need_by.setObjectName("need_by")
        self.request_layout.addWidget(self.need_by, 0, 2, 2, 1)

        self.update_button = QtGui.QPushButton(self)
        size_policy_ff = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        size_policy_ff.setHorizontalStretch(0)
        size_policy_ff.setVerticalStretch(0)
        size_policy_ff.setHeightForWidth(self.update_button.sizePolicy().hasHeightForWidth())
        self.update_button.setSizePolicy(size_policy_ff)
        self.update_button.setMinimumSize(QtCore.QSize(24, 24))
        self.update_button.setMaximumSize(QtCore.QSize(24, 24))
        self.update_button.setObjectName("update_button")
        self.update_button.setIcon(QtGui.QIcon(":/icons/icons/sos_update.png"))
        self.update_button.clicked.connect(self.update_status)
        self.request_layout.addWidget(self.update_button, 2, 0, 1, 1)

        self.countdown = QtGui.QLabel(self)
        self.countdown.setObjectName("countdown")
        self.request_layout.addWidget(self.countdown, 2, 2, 1, 1)

        self.request = QtGui.QLabel(self)
        self.request.setSizePolicy(size_policy_ef)
        self.request.setObjectName("request")
        self.request_layout.addWidget(self.request, 0, 1, 2, 1)

        self.ordered_time = QtGui.QLabel(self)
        self.ordered_time.setSizePolicy(size_policy_ef)
        self.ordered_time.setObjectName("ordered_time")
        self.request_layout.addWidget(self.ordered_time, 1, 1, 3, 1)

        self.username = QtGui.QLabel(self)
        self.username.setObjectName("username")
        self.request_layout.addWidget(self.username, 0, 3, 3, 1)

        self.status_box = QtGui.QComboBox(self)
        self.status_box.setObjectName("status_box")
        self.status_box.setMinimumSize(175, 24)
        self.request_layout.addWidget(self.status_box, 0, 4, 3, 1)

    def update_status(self):
        main = self.topLevelWidget()
        if main.user_id == 0:
            main.login.click()
            if main.user_id == 0:
                return
        status_form = StatusForm(self)
        pos = QtGui.QCursor.pos()
        pos.setX(pos.x())
        status_form.request_id = self.request_id.text()
        pos.setY(pos.y() + 10)
        status_form.move(pos)
        status_form.get_status()
        status_form.user_id = main.user_id
        status_form.status.setFocus()
        status_form.exec_()


class StatusForm(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setObjectName("status_form")
        self.setWindowFlags(QtCore.Qt.Popup)
        self.setMouseTracking(True)
        self.resize(250, 75)
        self.request_id = False
        self.user_id = False

        palette = colors.tan()
        self.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Source Code Pro Medium")
        self.setFont(font)

        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setMargin(6)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")

        self.statusLabel = QtGui.QLabel(self)
        self.statusLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.statusLabel.setObjectName("statusLabel")
        self.statusLabel.setText("Status:")
        self.gridLayout.addWidget(self.statusLabel, 0, 0, 1, 1)

        self.status = QtGui.QComboBox(self)
        self.status.setObjectName("status")
        self.gridLayout.addWidget(self.status, 0, 1, 1, 1)

        self.notesLabel = QtGui.QLabel(self)
        self.notesLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.notesLabel.setObjectName("notesLabel")
        self.notesLabel.setText("Notes:")
        self.gridLayout.addWidget(self.notesLabel, 1, 0, 1, 1)

        self.notes = QtGui.QLineEdit(self)
        self.notes.setObjectName("notes")
        self.gridLayout.addWidget(self.notes, 1, 1, 1, 1)

        self.buttons = QtGui.QDialogButtonBox(self)
        self.buttons.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttons.setCenterButtons(False)
        self.buttons.setObjectName("buttons")
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.gridLayout.addWidget(self.buttons, 2, 0, 1, 2)

    def get_status(self):
        status_qry = query("get_status")
        if status_qry:
            self.status.addItem("", 0)
            while status_qry.next():
                self.status.addItem(status_qry.value(1), [status_qry.value(0), status_qry.value(2)])
        else:
            self.reject()

    def accept(self):
        status_id, status_protected = self.status.itemData(self.status.currentIndex())
        if status_protected != 0:
            protected_qry = query("auth_status", [self.request_id])
            if protected_qry:
                protected_qry.first()
                if self.user_id == int(protected_qry.value(0)):
                    print("Good")
                    auth = True
                else:
                    print("Bad")
                    auth = False
            else:
                print("Failed")
                auth = False
        else:
            print("Not Protected")
            auth = True

        if auth:
            update_qry = query("update_request", [self.request_id, status_id, self.user_id, self.notes.text()])
            if update_qry:
                self.done(1)
            else:
                self.done(0)
        else:
            QtGui.QMessageBox.critical(None, "Not Authorized", "Only the original user can use this status")

    def resizeEvent(self, resize_event):
        path = QtGui.QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)
        region = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        QtGui.QDialog.resizeEvent(self, resize_event)
        resize_event.accept()
        
        
class NewRequest(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setObjectName("NewRequest")
        self.setWindowFlags(QtCore.Qt.Popup)
        self.setMouseTracking(True)
        self.setPalette(colors.tan())
        self.resize(300, 75)
        self.user_id = 0

        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setMargin(6)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")

        self.request_label = QtGui.QLabel(self)
        self.request_label.setObjectName("request_label")
        self.request_label.setText("Request:")
        self.gridLayout.addWidget(self.request_label, 0, 0, 1, 1)

        self.request = QtGui.QLineEdit(self)
        self.request.setObjectName("request")
        self.gridLayout.addWidget(self.request, 0, 1, 1, 1)

        self.need_by_label = QtGui.QLabel(self)
        self.need_by_label.setObjectName("need_by_label")
        self.need_by_label.setText("Needed By:")
        self.gridLayout.addWidget(self.need_by_label, 1, 0, 1, 1)

        self.need_by = QtGui.QDateTimeEdit(self)
        self.need_by.setObjectName("need_by")
        self.need_by.setCalendarPopup(True)
        self.need_by.setDateTime(QtCore.QDateTime.addDays(QtCore.QDateTime.currentDateTime(), 7))
        self.gridLayout.addWidget(self.need_by, 1, 1, 1, 1)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

    def accept(self):
        need_by = self.need_by.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        request_qry = query("new_request", [self.request.text(), need_by, self.user_id])
        if request_qry:
            self.done(1)
        else:
            self.reject()

    def resizeEvent(self, resize_event):
        path = QtGui.QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)
        region = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        QtGui.QDialog.resizeEvent(self, resize_event)
        resize_event.accept()


class CategoryLabel(QtGui.QLabel):
    def __init__(self, parent=None, label=""):
        QtGui.QLabel.__init__(self, parent)
        self.setText(label)
        font = QtGui.QFont()
        font.setFamily("Source Code Pro Bold")
        font.setPointSize(14)
        self.setFont(font)