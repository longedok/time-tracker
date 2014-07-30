# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_sessionsform.ui'
#
# Created: Mon Jul 21 19:26:35 2014
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
        self.table_sessions = QtGui.QTableView(SessionsForm)
        self.table_sessions.setObjectName("table_sessions")
        self.verticalLayout.addWidget(self.table_sessions)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_edit = QtGui.QPushButton(SessionsForm)
        self.button_edit.setObjectName("button_edit")
        self.horizontalLayout.addWidget(self.button_edit)
        self.button_delete = QtGui.QPushButton(SessionsForm)
        self.button_delete.setObjectName("button_delete")
        self.horizontalLayout.addWidget(self.button_delete)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SessionsForm)
        QtCore.QMetaObject.connectSlotsByName(SessionsForm)

    def retranslateUi(self, SessionsForm):
        SessionsForm.setWindowTitle(QtGui.QApplication.translate("SessionsForm", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.button_edit.setText(QtGui.QApplication.translate("SessionsForm", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.button_delete.setText(QtGui.QApplication.translate("SessionsForm", "Delete", None, QtGui.QApplication.UnicodeUTF8))

