# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_sessionsform.ui'
#
# Created: Tue Jul 22 00:16:20 2014
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
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edit_button = QtGui.QPushButton(SessionsForm)
        self.edit_button.setEnabled(False)
        self.edit_button.setObjectName("edit_button")
        self.horizontalLayout.addWidget(self.edit_button)
        self.delete_button = QtGui.QPushButton(SessionsForm)
        self.delete_button.setEnabled(False)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout.addWidget(self.delete_button)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SessionsForm)
        QtCore.QMetaObject.connectSlotsByName(SessionsForm)

    def retranslateUi(self, SessionsForm):
        SessionsForm.setWindowTitle(QtGui.QApplication.translate("SessionsForm", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_button.setText(QtGui.QApplication.translate("SessionsForm", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_button.setText(QtGui.QApplication.translate("SessionsForm", "Delete", None, QtGui.QApplication.UnicodeUTF8))

