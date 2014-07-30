import sqlite3
import time

import constants
from models import ProjectModel, SessionModel


class GenericDao(object):

	def execute(self, sql, values=tuple()):
		conn = sqlite3.connect(constants.DATABASE_FILE)
		with conn:
			curr = conn.cursor()
			results = list(curr.execute(sql, values))
			if (not results) and curr.lastrowid:
				results = curr.lastrowid
		conn.close()
		return results


class ProjectDao(GenericDao):

	def save(self, project):
		if project.id == 0:
			project.id = self.execute("INSERT INTO projects (name) VALUES (?)", (project.name,))
			return project
		else:
			self.execute("UPDATE projects SET name=? WHERE id=?", (project.name, project.id))

	def get_all(self):
		results = self.execute("""SELECT projects.*, MAX(sessions.end), SUM(sessions.end - sessions.start) 
			FROM projects 
			LEFT JOIN sessions ON projects.id == sessions.project_id 
			GROUP BY projects.id""")
		projects = []
		for prj_data in results:
			projects.append(ProjectModel(prj_data[0], prj_data[1], prj_data[2], prj_data[3]))
		return projects

	def get_by_id(self, id):
		fields = self.execute("SELECT * FROM projects WHERE id = ?", (id,))
		prj_data = fields[0]
		return ProjectModel(prj_data[0], prj_data[1])

	def get_last_session(self, project):
		result = self.execute("SELECT MAX(end) FROM sessions WHERE project_id = ?", (project_id,))
		return result[0]

	def get_total_duration(self, project):
		result = self.execute("""SELECT SUM(dlt) 
			FROM (SELECT s.end - s.start as dlt 
				  FROM sessions as s where project_id = ?)""", (project.id,))
		return result[0][0]

	def delete(self, project):
		self.execute("DELETE FROM projects WHERE id = ?", (project.id,))

	def delete_multiple(self, ids):
		self.execute("DELETE FROM projects WHERE id in (%s)" % ", ".join(map(str, ids)))


class SessionDao(GenericDao):

	def save(self, session):
		if session.id == 0:
			self.execute("INSERT INTO sessions (start, end, project_id) VALUES (?,?,?)", 
				(session.start, session.end, session.project_id))
		else:
			self.execute("UPDATE sessions SET start=?,end=?,project_id=? WHERE id=?", 
				(session.start, session.end, session.project_id, session.id))

	def get_project_sessions(self, project):
		results = self.execute("SELECT * FROM sessions WHERE project_id = ?", (project.id,))
		sessions = []
		for sess_data in results:
			sessions.append(SessionModel(sess_data[0], sess_data[1], sess_data[2], sess_data[3]))
		return sessions

	def get_by_id(self, id):
		fields = self.execute("SELECT * FROM sessions WHERE id = ?", (id,))
		sess_data = fields[0]
		return SessionModel(sess_data[0], sess_data[1], sess_data[2], sess_data[3])