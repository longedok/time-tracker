# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainform.ui'
#
# Created: Wed Jul 30 18:55:56 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(622, 484)
        self.verticalLayout = QtGui.QVBoxLayout(MainForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.current_project_label = QtGui.QLabel(MainForm)
        self.current_project_label.setObjectName("current_project_label")
        self.verticalLayout.addWidget(self.current_project_label)
        self.timer_label = QtGui.QLabel(MainForm)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.timer_label.setFont(font)
        self.timer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.timer_label.setObjectName("timer_label")
        self.verticalLayout.addWidget(self.timer_label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start_session_button = QtGui.QPushButton(MainForm)
        self.start_session_button.setEnabled(False)
        self.start_session_button.setObjectName("start_session_button")
        self.horizontalLayout.addWidget(self.start_session_button)
        self.stop_session_button = QtGui.QPushButton(MainForm)
        self.stop_session_button.setEnabled(False)
        self.stop_session_button.setObjectName("stop_session_button")
        self.horizontalLayout.addWidget(self.stop_session_button)
        self.start_project_button = QtGui.QPushButton(MainForm)
        self.start_project_button.setObjectName("start_project_button")
        self.horizontalLayout.addWidget(self.start_project_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.projects_table = QtGui.QTableView(MainForm)
        self.projects_table.setObjectName("projects_table")
        self.projects_table.horizontalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.projects_table)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.switch_project_button = QtGui.QPushButton(MainForm)
        self.switch_project_button.setEnabled(False)
        self.switch_project_button.setObjectName("switch_project_button")
        self.horizontalLayout_2.addWidget(self.switch_project_button)
        self.watch_sessions_button = QtGui.QPushButton(MainForm)
        self.watch_sessions_button.setEnabled(False)
        self.watch_sessions_button.setObjectName("watch_sessions_button")
        self.horizontalLayout_2.addWidget(self.watch_sessions_button)
        self.delete_project_button = QtGui.QPushButton(MainForm)
        self.delete_project_button.setEnabled(False)
        self.delete_project_button.setObjectName("delete_project_button")
        self.horizontalLayout_2.addWidget(self.delete_project_button)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)
        MainForm.setTabOrder(self.start_session_button, self.start_project_button)
        MainForm.setTabOrder(self.start_project_button, self.projects_table)

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(QtGui.QApplication.translate("MainForm", "Time Tracker", None, QtGui.QApplication.UnicodeUTF8))
        self.current_project_label.setText(QtGui.QApplication.translate("MainForm", "No current project", None, QtGui.QApplication.UnicodeUTF8))
        self.timer_label.setText(QtGui.QApplication.translate("MainForm", "00:00:00", None, QtGui.QApplication.UnicodeUTF8))
        self.start_session_button.setText(QtGui.QApplication.translate("MainForm", "Start Session", None, QtGui.QApplication.UnicodeUTF8))
        self.stop_session_button.setText(QtGui.QApplication.translate("MainForm", "Stop Session", None, QtGui.QApplication.UnicodeUTF8))
        self.start_project_button.setText(QtGui.QApplication.translate("MainForm", "Start New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.switch_project_button.setText(QtGui.QApplication.translate("MainForm", "Switch to project", None, QtGui.QApplication.UnicodeUTF8))
        self.watch_sessions_button.setText(QtGui.QApplication.translate("MainForm", "Watch Sessions", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_project_button.setText(QtGui.QApplication.translate("MainForm", "Delete", None, QtGui.QApplication.UnicodeUTF8))

