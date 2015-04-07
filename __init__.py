__author__ = 'ryan'

'''
Parts Simple Order System or S.O.S. as it's called here was written for Doyle Manufacturing but I hope others will
find it useful. It is a very simple program for requesting items from our parts department. Managers can make requests
is plain text and specify when they need what they are requesting. From that point it is added to the schedule and
ordered by due date and status. Requests come off the schedule after being marked as canceled or received. Below is the
text from the Parts S.O.S. manual.

This manual will go over the basic operating instructions for the Doyle Parts Simple Order System or S.O.S. for short.
Any questions about operation or suggestions for improvement should be directed to Ryan Hanson, (rhanson@doylemfg.com).

Basic Workflow
    Making a New Request
In order to make a new request you must have a valid login, know what you are requesting and know when you need it.
When you have this info you can click the “New Request” button . If you are not logged in a popup will prompt
you to do so. After logging in a second popup will allow you to enter your request and your needed date.
Use the “tab” key to navigate the cells and enter your information. When you are done click “Ok” and your order will
be submitted with your username and the current date.

    Updating a Request
When a request moves from one status to the next it must be updated. To update an order, click the “Update Request”
button . If you are not logged in a popup will prompt you to do so.  After logging in a second popup will prompt you
to pick a new status and you will also have an opportunity to enter any notes for the status if you need to.
When you are done click “Ok” and the status will be updated. Only the request’s creator can make the request as
“Received” or “Canceled”. Making either of these status will remove the request from the display.

Colors and Sorting
You will notice that all the requests are coded in different colors based on due date. The color code is as follows.
        RED – Less than one hour
        ORANGE – Less than four hours
        YELLOW – Less than 24 hours
        GREEN – Less than a week
        BLUE – More than a week

    The requests are also sorted by status. The order is as follows.
        Ordered
        In Process
        Delivered
        On Hold
        No Stock

Misc Notes
Logout timer is set to 3 minutes. After 3 minutes the current user is logged out.
Status notes can be seen by pulling down the current status drop down and mousing over the status that you want.
'''


import sys
from PyQt4 import QtGui, QtCore

from main import Main

import database_connection

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    if not database_connection.default_connection():
        sys.exit(1)
    sos = Main()
    sos.setWindowModality(QtCore.Qt.ApplicationModal)
    sos.show()
    sys.exit(app.exec_())