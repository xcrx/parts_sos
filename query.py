__author__ = 'ryan'

from PyQt4 import QtSql, QtGui
import sys
from database_connection import db_err

new_request = ("INSERT INTO `sos_request` (`id`, `request`, `need_by`, `user`) "
               "VALUES (NULL, '{0}', '{1}', {2});")

update_request = ("INSERT INTO `sos_request_status` (`request_id`, `status_id`, `user`, `created`, `notes`) "
                  "VALUES ({0}, {1}, {2}, CURRENT_TIMESTAMP, '{3}')")

get_users = "SELECT `User_ID`, `Name` FROM `Users_tbl` ORDER BY `Users_tbl`.`Name` ASC"

get_status = "SELECT `id`, `status`, `protected` FROM `sos_status` ORDER BY `id` ASC"

auth_status = "SELECT `user` FROM `sos_request` WHERE `id` = {0} LIMIT 1"

auth_user = "SELECT `Password` FROM `Users_tbl` WHERE `User_ID` = {0} LIMIT 1"

get_all_requests = ("SELECT `id`, `request`, DATE_FORMAT(`need_by`, '%m/%d/%Y %h:%i%p') as 'need_by_f', "
                    "`Users_tbl`.`Name` as 'User', DATE_FORMAT(`ordered_time`, '%m/%d/%Y %h:%i%p') FROM `sos_request` "
                    "LEFT JOIN `Users_tbl` ON `sos_request`.`user` = `Users_tbl`.`User_ID` ORDER BY `need_by` ASC")

get_filtered_requests = ("SELECT `id`, `request`, DATE_FORMAT(`need_by`, '%m/%d/%Y %h:%i%p') as 'need_by_f', "
                         "`Users_tbl`.`Name` as 'User' FROM `sos_request` LEFT JOIN `Users_tbl` ON "
                         "`sos_request`.`user` = `Users_tbl`.`User_ID` WHERE {0} ORDER BY `need_by` ASC")

get_request_status = ("SELECT `sos_request_status`.`id`, `sos_status`.`status`, `Users_tbl`.`Init` as 'User', "
                      "DATE_FORMAT(`created`, '%Y-%m-%d %r') as 'created_f', `notes` from (sos_request_status "
                      "LEFT JOIN sos_status ON sos_request_status.`status_id` = sos_status.`id`) LEFT JOIN "
                      "Users_tbl ON `sos_request_status`.`user` = `Users_tbl`.`User_ID` "
                      "WHERE `request_id` = {0} ORDER BY `sos_request_status`.`id` DESC")


def query(data, args=None, db='qt_sql_default_connection'):
    """
    Runs and returns a query.

    It takes the name of the query as an argument and finds it as a variable from up above
    """
    qry = QtSql.QSqlQuery(db)
    try:
        data = getattr(sys.modules[__name__], data)
    except AttributeError:
        QtGui.QMessageBox.critical(None, "INTERNAL ERROR", "A query matching %s was not found. Contact Admin." % data)
        return False
    if args:
        data = data.format(*args)
    if qry.exec_(data):
        return qry
    else:
        db_err(qry)
        return False