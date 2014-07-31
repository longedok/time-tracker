import locale
import sys

from PySide.QtGui import QApplication
from PySide.QtCore import QCoreApplication

from time_tracker import constants
from time_tracker.ui import MainForm
from time_tracker.db import create_db
from time_tracker.service import ProjectService, SessionService

if __name__ == '__main__':
	locale.setlocale(locale.LC_ALL, "russian_russia") #  english_us

	create_db(constants.DATABASE_FILE)

	QCoreApplication.setOrganizationName("Kartavykh Soft")
	QCoreApplication.setApplicationName("Time Tracker")

	app = QApplication(sys.argv)

	project_service = ProjectService()
	session_service = SessionService()

	session_service.timer_updated.connect(project_service.timer_update_slot)
	session_service.session_stopped.connect(project_service.session_stop_slot)

	main_form = MainForm(project_service, session_service)
	main_form.show()

	app.exec_()