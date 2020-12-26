from PyQt5.QtWidgets import QWidget, QGridLayout, QCheckBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
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
        grid = QGridLayout()
        grid.setAlignment(Qt.AlignLeft)
        grid.setSpacing(2)
        self.setLayout(grid)

        self.setWindowTitle("Preferences")
        self.size_x = 500
        self.size_y = 500

        self.setGeometry(
            0,
            0,
            int(self.size_x),
            int(self.size_y)
        )

        pref_data = self.get_json(PREFERENCES_FILE)

        textbox_f = QCheckBox("Open editor in fullscreen mode")
        if pref_data.get("fullscreen") is True:
            textbox_f.setChecked(True)

        textbox_w = QCheckBox("Warn when exiting without saving")
        if pref_data.get("warn_non_save") is True:
            textbox_w.setChecked(True)

        grid.addWidget(textbox_f, 0, 0)
        grid.addWidget(textbox_w, 0, 0)

        close_button = QPushButton("Exit without Saving")
        grid.addWidget(close_button)
        def close_():
            if textbox_w.isChecked():
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

        close_save_button = QPushButton("Save and Exit")
        grid.addWidget(close_save_button)
        def save_close():
            close_save_button.setCheckable(False)

            data = {"fullscreen": textbox_f.isChecked(), "warn_non_save": textbox_w.isChecked()}
            new = self.get_json(PREFERENCES_FILE)
            for key in data:
                new[key] = data[key]

            self.write_json(PREFERENCES_FILE, new)
            main.load_json_preferences(PREFERENCES_FILE)

            self.close()
        close_save_button.clicked.connect(save_close)
