# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_sessionsform.ui'
#
# Created: Wed Jul 30 18:55:57 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SessionsForm(object):
    def setupUi(self, SessionsForm):
        SessionsForm.setObjectName("SessionsForm")
        SessionsForm.resize(587, 484)
        self.verticalLayout = QtGui.QVBoxLayout(SessionsForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sessions_table = QtGui.QTableView(SessionsForm)
        self.sessions_table.setObjectName("sessions_table")
        self.verticalLayout.addWidget(self.sessions_table)

        self.retranslateUi(SessionsForm)
        QtCore.QMetaObject.connectSlotsByName(SessionsForm)

    def retranslateUi(self, SessionsForm):
        SessionsForm.setWindowTitle(QtGui.QApplication.translate("SessionsForm", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

