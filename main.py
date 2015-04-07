__author__ = 'ryan'

import sys
import os
from PyQt4 import QtCore, QtGui

import ui
import colors
from query import query

sys.path.insert(0, os.path.split(__file__)[0])

# Minutes to hours conversion
hours = 3600


def get_status_data(request_id):
    """
    Returns a list containing the status history for the request matching 'request_id'
    The list if pre-formatted to be dumped right into the status combobox
    """
    status_qry = query("get_request_status", [request_id])
    status = []
    if status_qry:
        while status_qry.next():
            status.append(["{0} - {1}".format(status_qry.value(1), status_qry.value(2)), status_qry.value(4)])
    return status


def get_countdown(date_string):
    """
    Returns the time remaining until the need_by date.
    time_left is the actual time remaining
    countdown is the string that is displayed in the UI
    """
    qt_date = QtCore.QDateTime.fromString(date_string, "MM/dd/yyyy hh:mmAP").toLocalTime()
    countdown = "Null"
    time_left = 0
    if qt_date.isValid():
        now = QtCore.QDateTime.currentDateTime().toLocalTime()
        time_left = now.secsTo(qt_date)/hours
        countdown = "{0} Hour(s)".format(round(time_left, 2))
    return time_left, countdown


def get_popup_pos(main, popup):
    """
    Calculates and returns the position for popup windows so they show under the users mouse but still on the screen.
    """
    pos = QtGui.QCursor.pos()
    window_pos = main.pos()
    rel_pos = pos - window_pos
    window_size = main.size()
    if rel_pos.x() > window_size.width()/2:
        pos.setX(pos.x() - popup.width())
        pos.setY(pos.y() + 10)
    else:
        pos.setX(pos.x())
        pos.setY(pos.y() + 10)
    return pos


def clear_layout(layout):
    """
    Clears all widgets off the supplied layout
    """
    for i in reversed(range(layout.count())):
        item = layout.itemAt(i)

        if isinstance(item, QtGui.QWidgetItem):
            item.widget().close()
        elif isinstance(item, QtGui.QSpacerItem):
            pass
        else:
            clear_layout(item.layout())

        layout.removeItem(item)
    return True


class Main(ui.MainWindow):
    """
    This is the main UI window.
    It contains all the button functions and timers that are needed for basic function.
    """
    def __init__(self):
        ui.MainWindow.__init__(self)
        self.requests = None

        def connections():
            self.login.clicked.connect(self.login_widget)
            self.new_request.clicked.connect(self.new_request_widget)

        connections()

        self.load_request_data()
        # self.setWindowState(QtCore.Qt.WindowFullScreen)
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.startTimer(10*1000)

    def login_widget(self):
        """
        Opens login popup and sets the timer to force the use to logout.
        """
        login_form = ui.LoginForm(self)
        login_form.move(get_popup_pos(self, login_form))
        login_form.exec_()
        if login_form.user_id != 0:
            self.user_id = login_form.user_id
            self.login.setText("Logout")
            self.login.clicked.disconnect()
            self.login.clicked.connect(self.logout)
            self.username.setText("<strong>" + login_form.username)
            self.login_time.setVisible(True)
            self.login_timer.start(1000)

    def new_request_widget(self):
        """
        Opens the new request popup. If the user isn't logged in, it opens the login popup first.
        """
        if self.user_id == 0:
            self.login.click()
            if self.user_id == 0:
                return
        new_request_form = ui.NewRequest(self)
        new_request_form.move(get_popup_pos(self, new_request_form))
        new_request_form.user_id = self.user_id
        new_request_form.request.setFocus()
        new_request_form.exec_()

    def logout(self):
        """
        Logs out the current user
        """
        self.login_timer.stop()
        self.user_id = 0
        self.username.setText("")
        self.login.setText("Login")
        self.login_time.setValue(180)
        self.login_time.setVisible(False)
        self.login.clicked.disconnect()
        self.login.clicked.connect(self.login_widget)

    def load_request_data(self):
        """
        Gets the requests from the database and displays them.

        The requests are sorted by category and time

        It also beeps if a new request is added
        """
        clear_layout(self.request_layout)
        requests_qry = query("get_all_requests")
        requests = []
        if requests_qry:
            ordered = []
            in_process = []
            delivered = []
            on_hold = []
            no_stock = []
            misc = []
            received = []
            widgets = {"On Order": ordered, "In Process": in_process, "Delivered": delivered, "On Hold": on_hold,
                       "No Stock": no_stock, "Misc": misc, "Received": received}

            while requests_qry.next():
                request_id = requests_qry.value(0)
                requests.append(request_id)
                status = get_status_data(request_id)
                need_by = requests_qry.value(2)
                time_left, countdown = get_countdown(need_by)
                if 168 >= time_left > 24:
                    palette = colors.green()
                elif 24 >= time_left > 4:
                    palette = colors.yellow()
                elif 4 >= time_left > 1:
                    palette = colors.orange()
                elif time_left <= 1:
                    palette = colors.red()
                else:
                    palette = colors.blue()

                if "Canceled" in status[0][0]:
                    pass
                else:
                    request_form = ui.RequestForm(palette=palette)
                    request_form.request_id.setText(str(request_id))
                    request_form.request.setText(requests_qry.value(1))
                    request_form.need_by.setText(need_by)
                    request_form.username.setText(requests_qry.value(3))
                    request_form.ordered_time.setText(requests_qry.value(4))

                    for idx, s in enumerate(status):
                        request_form.status_box.addItem(s[0])
                        request_form.status_box.setItemData(idx, s[1], QtCore.Qt.ToolTipRole)

                    request_form.countdown.setText(countdown)
                    if "Ordered" in status[0][0]:
                        ordered.append(request_form)
                    elif "In Process" in status[0][0]:
                        in_process.append(request_form)
                    elif "Delivered" in status[0][0]:
                        delivered.append(request_form)
                    elif "On Hold" in status[0][0]:
                        request_form.setPalette(colors.gray_text(request_form.palette()))
                        on_hold.append(request_form)
                    elif "No Stock" in status[0][0]:
                        request_form.setPalette(colors.gray_text(request_form.palette()))
                        no_stock.append(request_form)
                    elif "Received" in status[0][0]:
                        request_form.setPalette(colors.gray_text(request_form.palette()))
                        received.append(request_form)
                    else:
                        misc.append(request_form)

            for cat in ("On Order", "In Process", "Delivered", "On Hold", "No Stock", "Misc", "Received"):
                if widgets[cat].__len__() > 0:
                    if cat != "Received" or self.show_history.isChecked():
                        self.request_layout.addWidget(ui.CategoryLabel(self, cat))
                        for form in widgets[cat]:
                            self.request_layout.addWidget(form)

            if self.requests != requests:
                QtGui.QApplication.beep()
            self.requests = requests

        else:
            self.close()

    def timerEvent(self, event):
        """
        Reload the request data after a specified amount of time.
        """
        self.load_request_data()
        event.ignore()