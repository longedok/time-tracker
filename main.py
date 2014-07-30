import locale
import sys

from PySide.QtGui import QApplication

from time_tracker.ui import MainForm
from time_tracker.service import ProjectService, SessionService

if __name__ == '__main__':
	locale.setlocale(locale.LC_ALL, "russian_russia") #  english_us

	app = QApplication(sys.argv)

	project_service = ProjectService()
	session_service = SessionService()

	session_service.timer_updated.connect(project_service.timer_update_slot)

	main_form = MainForm(project_service, session_service)
	main_form.show()

	app.exec_()