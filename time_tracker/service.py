import time
from functools import partial

from PySide.QtCore import QTimer, QObject, Signal, QModelIndex, Qt, QSettings

from models import ProjectModel, SessionModel, ProjectTableModel, SessionTableModel, PauseModel
from db import ProjectDao, SessionDao, PauseDao
from constants import SessionState

class ProjectService(QObject):
	project_activated = Signal(ProjectModel, bool) # 2nd param indicates if the activated project is newly created
	project_deleted = Signal(ProjectModel)
	active_project_deleted = Signal()
	active_project_renamed = Signal(ProjectModel)

	default_project_name = "New Project (%d)"
	project_number = 0

	def __init__(self):
		super(ProjectService, self).__init__()

		self.project_dao = ProjectDao()
		self.table_model = ProjectTableModel(self, self.project_dao)
		self.table_model.dataChanged.connect(self._data_changed)

		self.current_project = None

	def start_project(self):
		"Starts a new project"
		ProjectService.project_number += 1
		default_name = ProjectService.default_project_name % ProjectService.project_number
		self.current_project = ProjectModel(name=default_name)
		self.current_project = self.project_dao.save(self.current_project)

		self.table_model.insert_project(0, self.current_project)

		self.project_activated.emit(self.current_project, True)

	def delete_projects(self, ixs):
		"Deletes projects"

		ids = map(lambda x:self.table_model.data(x, Qt.UserRole).id, ixs)
		if self.current_project and self.current_project.id in ids:
			self.active_project_deleted.emit()
			self.current_project = None
		self.project_dao.delete_multiple(ids)
		for ix in reversed(ixs):
			self.table_model.removeRows(ix.row())

	def switch_project(self, ix):
		"Makes an existent project active"

		project = self.table_model.data(ix, Qt.UserRole)

		if project.id != self.current_project:
			self.current_project = project
			self.project_activated.emit(project, False)

	def close_project(self):
		settings = QSettings()
		if self.current_project:
			settings.setValue("projects/last_project", self.current_project.id)
		else:
			settings.remove("projects/last_project")
		settings.sync()

	def get_project_by_index(self, ix):
		return self.table_model.data(ix, Qt.UserRole)

	def get_index_by_id(self, id):
		return self.table_model.get_cell_index(id, 0)

	def timer_update_slot(self, time):
		"Updates total time of the current project in the table model"

		ix = self.table_model.get_cell_index(self.current_project.id, 2)
		self.table_model.setData(ix, 1, Qt.UserRole)

	def session_stop_slot(self):
		ix = self.table_model.get_cell_index(self.current_project.id, 1)
		self.table_model.setData(ix, time.time(), Qt.UserRole)

	def _data_changed(self, left_top, bottom_right):
		if self.current_project:
			changed_prj = self.table_model.data(left_top, Qt.UserRole)
			if left_top.column() == 0 and changed_prj.id == self.current_project.id:
				self.active_project_renamed.emit(self.current_project)


class SessionService(QObject):
	session_started = Signal(SessionModel)
	session_paused = Signal(SessionModel)
	session_resumed = Signal(SessionModel)
	session_stopped = Signal()
	timer_updated = Signal(float)

	def __init__(self):
		super(SessionService, self).__init__()

		self.session_dao = SessionDao()

		self.time = 0
		self.state = SessionState.STOPPED

		self.timer = QTimer(self)
		self.timer.timeout.connect(self._timer_timeout)

		self.current_session = None

	def start_session(self, project):
		self.time = 0
		self.current_session = SessionModel(start = time.time(), project_id = project.id)
		self.current_session = self.session_dao.save(self.current_session)
		self.timer.start(1000)
		self.state = SessionState.ACTIVE
		self.session_started.emit(self.current_session)

	def pause_session(self):
		self.timer.stop()
		self.state = SessionState.PAUSED
		self.session_paused.emit(self.current_session)

	def resume_session(self):
		self.timer.start(1000)
		self.state = SessionState.ACTIVE
		self.current_pause = None
		self.session_resumed.emit(self.current_session)

	def stop_session(self):
		self.state = SessionState.STOPPED
		self.timer.stop()
		if self.current_session:
			self.current_session.end = time.time()
			self.current_session.duration = self.time
			self.session_dao.save(self.current_session)
			self.session_stopped.emit()
			self.current_session = None
		self.time = 0

	def get_state(self):
		return self.state

	def get_table_model(self, project):
		'Returns a table model with sessions for the specified project'
		return SessionTableModel(self, project, self.session_dao)

	def _timer_timeout(self):
		self.time += 1
		self.timer_updated.emit(self.time)


class PauseService(object):

	def __init__(self):
		self.current_pause = None
		self.pause_dao = PauseDao()

	def start_pause(self, session_id):
		self.current_pause = PauseModel(start=time.time(), session_id=session_id)

	def end_pause(self):
		self.current_pause.end = time.time()
		self.pause_dao.save(self.current_pause)
		self.current_pause = None

	def session_pause_slot(self, session):
		self.start_pause(session.id)

	def session_resume_slot(self, session):
		self.end_pause()

	def session_stop_slot(self):
		if self.current_pause:
			self.end_pause()