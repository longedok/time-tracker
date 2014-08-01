import sqlite3
import time

import constants
from models import ProjectModel, SessionModel

def create_db(db_name):
	projects_table_sql = '''CREATE TABLE IF NOT EXISTS `projects`	 (
		`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
		`name`	TEXT NOT NULL);'''

	sessions_table_sql = '''CREATE TABLE IF NOT EXISTS `sessions` (
		`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
		`start`	INTEGER NOT NULL,
		`end`	INTEGER,
		`duration` INTEGER,
		`project_id` INTEGER NOT NULL,
		FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
	);'''

	pauses_table_sql = '''CREATE TABLE IF NOT EXISTS `pauses` (
		`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
		`start`	INTEGER NOT NULL,
		`end`	INTEGER NOT NULL,
		`session_id`	INTEGER,
		FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
	);
	'''

	conn = sqlite3.connect(db_name)

	with conn:
		for table_sql in (projects_table_sql, sessions_table_sql, pauses_table_sql):
			conn.execute(table_sql)

	conn.close()


class GenericDao(object):

	def execute(self, sql, values=tuple()):
		conn = sqlite3.connect(constants.DATABASE_FILE)
		conn.execute('pragma foreign_keys=ON')
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
		results = self.execute("""SELECT projects.*, MAX(sessions.end), SUM(sessions.duration) 
			FROM projects 
			LEFT JOIN sessions ON projects.id == sessions.project_id 
			GROUP BY projects.id""")
		projects = []
		for prj_data in results:
			projects.append(ProjectModel(prj_data[0], prj_data[1], prj_data[2], prj_data[3]))
		return projects

	def get_by_id(self, id):
		fields = self.execute("""SELECT projects.*, MAX(sessions.end), SUM(sessions.duration) 
			FROM projects 
			LEFT JOIN sessions ON projects.id == sessions.project_id 
			WHERE projects.id = ?
			GROUP BY projects.id""", (id,))
		prj_data = fields[0]
		return ProjectModel(prj_data[0], prj_data[1], prj_data[2], prj_data[3])

	def delete_multiple(self, ids):
		self.execute("DELETE FROM projects WHERE id in (%s)" % ", ".join(map(str, ids)))


class SessionDao(GenericDao):

	def save(self, session):
		if session.id == 0:
			session.id = self.execute("INSERT INTO sessions (start, end, duration, project_id) VALUES (?,?,?,?)", 
				(session.start, session.end, session.duration, session.project_id))
			return session
		else:
			self.execute("UPDATE sessions SET start=?,end=?,duration=?,project_id=? WHERE id=?", 
				(session.start, session.end, session.duration, session.project_id, session.id))

	def get_project_sessions(self, project):
		results = self.execute("""SELECT sessions.*, COUNT(pauses.id), SUM(pauses.end - pauses.start)
			FROM sessions
			LEFT JOIN pauses ON sessions.id = pauses.session_id
			WHERE project_id = ?
			GROUP BY sessions.id""", (project.id,))
		sessions = []
		for sess_data in results:
			sessions.append(SessionModel(sess_data[0], sess_data[1], sess_data[2], 
				sess_data[3], sess_data[4], sess_data[5], sess_data[6]))
		return sessions

	def get_by_id(self, id):
		fields = self.execute("SELECT * FROM sessions WHERE id = ?", (id,))
		sess_data = fields[0]
		return SessionModel(sess_data[0], sess_data[1], sess_data[2], sess_data[3], sess_data[4])


class PauseDao(GenericDao):

	def save(self, pause):
		if pause.id == 0:
			self.execute("INSERT INTO pauses (start, end, session_id) VALUES (?,?,?)", 
				(pause.start, pause.end, pause.session_id))
		else:
			self.execute("UPDATE pauses SET start=?,end=?,session_id=? WHERE id=?", 
				(pause.start, pause.end, pause.session_id, pause.id))		