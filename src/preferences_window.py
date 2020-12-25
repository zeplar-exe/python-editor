from PyQt5.QtWidgets import QWidget, QGridLayout
from json_lib import JSON
import graphics as gp

PREFERENCES_FILE = "user_preferences.json"

class PreferencesApplication(QWidget, JSON):
    """
    Main class for pyqt application
    """
    def __init__(self, main):
        """
        Class Initiator
        """
        super().__init__()

        self.setMinimumSize(300, 225)
        self.size_x = 0
        self.size_y = 0

        self.init_ui()

    def init_ui(self):
        """
        Initiates window UI specifics
        """
        self.setWindowTitle("Preferences")
        self.size_x = 500
        self.size_y = 500

        self.setGeometry(
            0,
            0,
            int(self.size_x),
            int(self.size_y)
        )
