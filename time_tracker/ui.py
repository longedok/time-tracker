import time

from PySide.QtGui import QWidget, QHeaderView, QDialog, QAbstractItemView, QMessageBox, QItemSelectionModel
from PySide.QtCore import QTimer, Qt, Slot, QSettings

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
		self.project_service.active_project_deleted.connect(self.active_project_deletion_slot)
		self.project_service.active_project_renamed.connect(self.active_project_rename_slot)

		self.projects_table.setModel(self.project_service.table_model)
		self.projects_table.setSortingEnabled(True)
		self.projects_table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		self.projects_table.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.projects_table.doubleClicked.connect(self._table_view_double_click)

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
		self._switch_project(ix)

	def watch_sessions_clicked(self):
		ix = self.projects_table.selectionModel().selectedRows()[0]
		prj = self.project_service.get_project_by_index(ix)
		sess_form = SessionForm(self, prj, self.session_service)
		sess_form.show()

	def delete_project_clciked(self):
		ixs = self.projects_table.selectionModel().selectedRows()
		ix_num = len(ixs)
		title = "Delete project%s" % ("s" if ix_num > 1 else "",)
		message = "Are you sure? (%d project%s)" % (ix_num, "s" if ix_num > 1 else "")
		ret = QMessageBox.question(self, title, message, 
							QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
		if ret == QMessageBox.Yes:
			self.project_service.delete_projects(ixs)

	@Slot(SessionModel)
	def session_start_slot(self, session):
		self.start_session_button.setText("Pause")
		self.stop_session_button.setEnabled(True)
		self.start_project_button.setEnabled(False)

	@Slot()
	def session_pause_slot(self, session):
		self.start_session_button.setText("Resume")

	@Slot()
	def session_resume_slot(self, session):
		self.start_session_button.setText("Pause")

	@Slot()
	def session_finish_slot(self):
		self.start_project_button.setEnabled(True)
		self.start_session_button.setText("Start Session")
		self.stop_session_button.setEnabled(False)
		self._clear_timer()

	@Slot(ProjectModel, bool)
	def project_activation_slot(self, project, new_project):
		self.current_project = project
		self._clear_timer()
		self.current_project_label.setText("Current project is <strong>%s</strong>" % project.name)
		if new_project:
			ix = self.project_service.get_index_by_id(project.id)
			self.projects_table.edit(ix)
			self.projects_table.selectionModel().setCurrentIndex(ix, 
				QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
		self.start_session_button.setEnabled(True)

	@Slot(float)
	def timer_update_slot(self, time):
		self.timer_label.setText(convert_seconds_to_time(time))

	@Slot(ProjectModel)
	def active_project_deletion_slot(self):
		if self.session_service.get_state() == SessionState.ACTIVE:
			self.session_service.stop_session()
			self.current_project_label.setText("No current project")
			self.start_session_button.setEnabled(False)
		self.current_project = None

	@Slot(ProjectModel)
	def active_project_rename_slot(self, project):
		self.current_project_label.setText("Current project is <strong>%s</strong>" % project.name)

	def showEvent(self, event):
		settings = QSettings()
		last_project_id = settings.value("projects/last_project")
		if last_project_id:
			ix = self.project_service.get_index_by_id(last_project_id)
			self.project_service.switch_project(ix)

	def closeEvent(self, event):
		self.session_service.stop_session()
		self.project_service.close_project()

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

	def _table_view_double_click(self, index):
		self._switch_project(index)

	def _clear_timer(self):
		self.timer_label.setText("00:00:00")

	def _switch_project(self, ix):
		if self.session_service.get_state() == SessionState.ACTIVE:
			self.session_service.stop_session()
		self.project_service.switch_project(ix)


class SessionForm(QDialog, Ui_SessionsForm):

	def __init__(self, parent, project, session_service):
		super(SessionForm, self).__init__(parent)
		self.setupUi(self)

		self.project = project
		self.setWindowTitle("Project: %s" % project.name)

		self.sessions_table.setModel(session_service.get_table_model(project))
		self.sessions_table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
		self.sessions_table.setSelectionBehavior(QAbstractItemView.SelectRows)