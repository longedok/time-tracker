import time

from PySide.QtGui import QWidget, QHeaderView, QDialog, QAbstractItemView
from PySide.QtCore import QTimer, Qt, Slot

from ui_mainform import Ui_MainForm
from ui_sessionsform import Ui_SessionsForm

from constants import SessionState
from models import ProjectModel, SessionModel
from utils import convert_seconds_to_time


class MainForm(QWidget, Ui_MainForm):

	def __init__(self, project_service, session_service, parent=None):
		super(MainForm, self).__init__(parent)
		self.setupUi(self)

		self.project_service = project_service
		self.session_service = session_service

		self.start_session_button.clicked.connect(self.start_session_clicked)
		self.stop_session_button.clicked.connect(self.stop_session_clicked)
		self.start_project_button.clicked.connect(self.start_project_clicked)
		self.switch_project_button.clicked.connect(self.switch_project_clicked)
		self.watch_sessions_button.clicked.connect(self.watch_sessions_clicked)
		self.delete_project_button.clicked.connect(self.delete_project_clciked)

		self.session_service.session_started.connect(self.session_start_slot)
		self.session_service.session_paused.connect(self.session_pause_slot)
		self.session_service.session_resumed.connect(self.session_resume_slot)
		self.session_service.session_stopped.connect(self.session_finish_slot)
		self.session_service.timer_updated.connect(self.timer_update_slot)

		self.project_service.project_activated.connect(self.project_activation_slot)

		self.projects_table.setModel(self.project_service.table_model)
		self.projects_table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		self.projects_table.setSelectionBehavior(QAbstractItemView.SelectRows)

		selection_model = self.projects_table.selectionModel()
		selection_model.selectionChanged.connect(self._selection_changed)

		self.current_project = None

	def start_session_clicked(self):
		session_state = self.session_service.get_state()
		if session_state == SessionState.STOPPED:
			self.session_service.start_session(self.current_project)
		elif session_state == SessionState.ACTIVE:
			self.session_service.pause_session()
		elif session_state == SessionState.PAUSED:
			self.session_service.resume_session()

	def stop_session_clicked(self):
		self.session_service.stop_session()

	def start_project_clicked(self):
		self.project_service.start_project()

	def switch_project_clicked(self):
		ix = self.projects_table.selectionModel().selectedRows()[0]
		self.project_service.switch_project(ix)

	def watch_sessions_clicked(self):
		pass

	def delete_project_clciked(self):
		start = time.time()
		ixs = self.projects_table.selectionModel().selectedRows()
		self.project_service.delete_projects(ixs)
		print "Total:", time.time() - start

	@Slot(SessionModel)
	def session_start_slot(self, session):
		self.start_session_button.setText("Pause")
		self.stop_session_button.setEnabled(True)
		self.start_project_button.setEnabled(False)

	@Slot()
	def session_pause_slot(self):
		self.start_session_button.setText("Resume")

	@Slot()
	def session_resume_slot(self):
		self.start_session_button.setText("Pause")

	@Slot()
	def session_finish_slot(self):
		self.start_project_button.setEnabled(True)
		self.start_session_button.setText("Start Session")
		self.stop_session_button.setEnabled(False)
		self._clear_timer()

	@Slot(ProjectModel)
	def project_activation_slot(self, project):
		self.current_project = project
		self._clear_timer()
		self.current_project_label.setText("Current project is <strong>%s</strong>" % project.name)
		self.start_session_button.setEnabled(True)

	@Slot(float)
	def timer_update_slot(self, time):
		self.timer_label.setText(convert_seconds_to_time(time))

	def _selection_changed(self, selected, deselected):
		rows = self.projects_table.selectionModel().selectedRows()
		if len(rows) == 1: # a single project was selected, enable all bottom buttons
			self.switch_project_button.setEnabled(True)
			self.watch_sessions_button.setEnabled(True)
			self.delete_project_button.setEnabled(True)
		elif len(rows) > 1: # multiple projects were selected, enable only 'delete' button
			self.switch_project_button.setEnabled(False)
			self.watch_sessions_button.setEnabled(False)
			self.delete_project_button.setEnabled(True)
		else: # no projects were selected, disable all bottom buttons
			self.switch_project_button.setEnabled(False)
			self.watch_sessions_button.setEnabled(False)
			self.delete_project_button.setEnabled(False)

	def _clear_timer(self):
		self.timer_label.setText("00:00:00")


class SessionForm(QDialog, Ui_SessionsForm):

	def __init__(self, parent, project, session_dao):
		super(SessionForm, self).__init__(parent)
		self.setupUi(self)

		self.project = project
		self.session_dao = session_dao
		self.setWindowTitle("Project: %s" % self.project.name)

		self.sessions_model = SessionTableModel(self, project, self.session_dao)
		self.table_sessions.setModel(self.sessions_model)
		self.table_sessions.horizontalHeader().setResizeMode(QHeaderView.Stretch)