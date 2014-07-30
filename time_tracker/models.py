import time

from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex

from utils import convert_seconds_to_time, convert_timestamp_to_time


class ProjectModel(object):
	default_project_name = "New Project (%d)"
	project_number = 1

	def __init__(self, id=0, name='', last_session=None, total_duration=0):
		if len(name) == 0:
			self.name = ProjectModel.default_project_name % ProjectModel.project_number
			ProjectModel.project_number += 1
		else:
			self.name = name
		self.id = id
		self.last_session = last_session or time.time()
		self.total_duration = total_duration or 0

	def __str__(self):
		return "%d - %s" % (self.id, self.name)


class ProjectTableModel(QAbstractTableModel):

	def __init__(self, parent, project_dao, *args):
		QAbstractTableModel.__init__(self, parent, *args)

		self.projects = project_dao.get_all()
		self.project_dao = project_dao

	def insert_project(self, position, project):
		self.beginInsertRows(QModelIndex(), position, position)

		self.projects.insert(position, project)

		self.endInsertRows()

	def rowCount(self, parent):
		return len(self.projects)

	def columnCount(self, parent):
		return 3

	def data(self, index, role):
		if not index.isValid():
			return None

		if not 0 <= index.row() < len(self.projects):
			return None

		if role == Qt.UserRole:
			return self.projects[index.row()]

		if role == Qt.DisplayRole or role == Qt.EditRole:
			prj = self.projects[index.row()]

			if index.column() == 0:
				return prj.name
			elif index.column() == 1:
				return convert_timestamp_to_time(prj.last_session)
			elif index.column() == 2:
				return convert_seconds_to_time(prj.total_duration)

		return None

	def headerData(self, col, orientation, role):
		if role != Qt.DisplayRole:
			return None

		if orientation == Qt.Horizontal:
			if col == 0:
				return "Name"
			elif col == 1:
				return "Last Session"
			elif col == 2:
				return "Total Duration"
		
		return None

	def removeRows(self, position, rows=1, index=QModelIndex()):
		self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
		
		del self.projects[position:position+rows]

		self.endRemoveRows()

		return True

	def setData(self, index, value, role):
		if index.isValid() and 0 <= index.row() < len(self.projects):
			if role == Qt.EditRole:
				prj = self.projects[index.row()]
				if index.column() == 0:
					prj.name = value
					self.project_dao.save(prj)
				else:
					return False
			elif role == Qt.UserRole:
				prj = self.projects[index.row()]
				if index.column() == 2:
					prj.total_duration += value
				else:
					return False

			self.dataChanged.emit(index, index)
			return True

		return False

	def flags(self, index):
		if index.column() == 0:
			return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
		return super(ProjectTableModel, self).flags(index)

	def get_project_duration_index(self, project):
		"Returns index of the 'Duration' cell for the given project"

		for row, prj in enumerate(self.projects):
			if prj.id == project.id:
				return self.index(row, 2, QModelIndex())


class SessionModel(object):
	def __init__(self, id=0, start=0, end=0, project_id=0):
		self.id = id
		self.start = start
		self.end = end
		self.project_id = project_id

	def __str__(self):
		format_str = "%H:%M:%S"
		return "%d - %s %s %d" % (self.id, strftime(format_str, self.start), 
			strftime(format_str, self.end), self.project_id)

class SessionTableModel(QAbstractTableModel):

	def __init__(self, parent, project, session_dao, *args):
		QAbstractTableModel.__init__(self, parent, *args)

		self.sessions = session_dao.get_project_sessions(project)
		self.session_dao = session_dao

	def rowCount(self, parent):
		return len(self.sessions)

	def columnCount(self, parent):
		return 3

	def data(self, index, role):
		if role == Qt.UserRole:
			return self.sessions[index.row()]
		if role != Qt.DisplayRole:
			return None
		session = self.sessions[index.row()]
		if index.column() == 0:
			return convert_timestamp_to_time(session.start)
		elif index.column() == 1:
			return convert_timestamp_to_time(session.end)
		elif index.column() == 2:
			return convert_seconds_to_time(session.end - session.start)

	# def flags(self, index):
	# 	if index.column() == 0:
	# 		return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
	# 	return super(ProjectTableModel, self).flags(index)

	# def setData(self, index, value, role):
	# 	if index.column() == 0:
	# 		prj = self.projects[index.row()]
	# 		prj.name = value
	# 		self.dataChanged.emit(index, index)
	# 		self.project_dao.save(prj)
	# 		return True
	# 	else:
	# 		return False

	def headerData(self, col, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			if col == 0:
				return "Start"
			elif col == 1:
				return "End"
			elif col == 2:
				return "Duration"
		else:
			return QAbstractTableModel.headerData(self, col, orientation, role)