from PyQt5.QtWidgets import QWidget, QCheckBox, QPushButton, QMessageBox
from json_lib import JSON
#import graphics as gp

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

        self.init_ui(main)

    def init_ui(self, main):
        """
        Initiates window UI specifics
        """
        self.setWindowTitle("Preferences")
        self.size_x = 400
        self.size_y = 500

        self.setGeometry(
            0,
            0,
            int(self.size_x),
            int(self.size_y)
        )

        pref_data = self.get_json(PREFERENCES_FILE)

        checkbox_f = QCheckBox("Open editor in fullscreen mode", parent=self)
        if pref_data.get("fullscreen") is True:
            checkbox_f.setChecked(True)

        checkbox_w = QCheckBox("Warn when exiting without saving", parent=self)
        if pref_data.get("warn_non_save") is True:
            checkbox_w.setChecked(True)

        close_button = QPushButton("Exit without Saving", parent=self)
        def close_():
            if checkbox_w.isChecked():
                dialog = QMessageBox()
                dialog.setIcon(QMessageBox.Question)
                dialog.setText("Preferences may have been modified")
                dialog.setInformativeText("Are you sure that you would like to exit without saving?")
                dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                dialog.resize(125, 75)
                dialog.setMaximumSize(125, 75)
                dialog.setMinimumSize(125, 75)

                ret = dialog.exec_()

                if ret == QMessageBox.Ok:
                    dialog.accept()
                    self.close()
                elif ret == QMessageBox.Cancel:
                    dialog.reject()
            else:
                self.close()
        close_button.clicked.connect(close_)

        close_save_button = QPushButton("Save and Exit", parent=self)
        def save_close():
            close_save_button.setCheckable(False)

            data = {"fullscreen": checkbox_f.isChecked(), "warn_non_save": checkbox_w.isChecked()}
            new = self.get_json(PREFERENCES_FILE)
            for key in data:
                new[key] = data[key]

            self.write_json(PREFERENCES_FILE, new)
            main.load_json_preferences(PREFERENCES_FILE)

            self.close()
        close_save_button.clicked.connect(save_close)
