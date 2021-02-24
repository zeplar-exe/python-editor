import logging
from PyQt5.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QCheckBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from json_lib import JSON

PREFERENCES_FILE = "user_preferences.json"


class PreferencesApplication(QMainWindow, JSON):
    """
    Main class for pyqt application
    """

    def __init__(self, main):
        """
        Class Initiator
        """
        super().__init__()

        self.main = main
        self.setMinimumSize(300, 225)
        self.size_x = 0
        self.size_y = 0

        self.init_ui()

    def init_ui(self):
        """
        Initiates window UI specifics
        """
        main = self.main
        self.setWindowTitle("Preferences")
        self.size_x = (main.screen_size.width() / 10) * 3.3
        self.size_y = (main.screen_size.height() / 10) * 7
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignLeft)
        frame_layout.setSpacing(2)

        self.setFixedSize(
            int(self.size_x),
            int(self.size_y)
        )

        frame = QFrame()
        self.setCentralWidget(frame)
        frame.setGeometry(
            0,
            0,
            self.size().width(),
            (self.size().height() / 10) * 7.5
        )
        frame.setFrameShape(QFrame.StyledPanel)

        pref_data = self.get_json(PREFERENCES_FILE)

        checkbox_d = QCheckBox("Enable DEBUG mode")
        if pref_data.get("debug_mode"):
            checkbox_d.setChecked(True)
        frame_layout.addWidget(checkbox_d)

        checkbox_f = QCheckBox("Open editor in fullscreen mode")
        if pref_data.get("fullscreen") is True:
            checkbox_f.setChecked(True)
        frame_layout.addWidget(checkbox_f)

        checkbox_w = QCheckBox("Warn when exiting without saving")
        if pref_data.get("warn_non_save") is True:
            checkbox_w.setChecked(True)
        frame_layout.addWidget(checkbox_w)

        close_button = QPushButton("Exit without Saving", parent=self)
        close_button.move(
            self.size_x - (close_button.size().width() * 2) - 10,
            self.size_y - close_button.size().height() - 5
        )

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
        close_save_button.move(
            self.size_x - close_save_button.size().width() - 5,
            self.size_y - close_save_button.size().height() - 5
        )

        def save_close():
            data = {
                "debug_mode": checkbox_d.isChecked(),
                "fullscreen": checkbox_f.isChecked(),
                "warn_non_save": checkbox_w.isChecked()}
            new = self.get_json(PREFERENCES_FILE)
            for key in data:
                new[key] = data[key]

            self.write_json(PREFERENCES_FILE, new)
            main.load_json_preferences(PREFERENCES_FILE)

            self.close()

        close_save_button.clicked.connect(save_close)

        frame_layout.addStretch()
        frame.setLayout(frame_layout)

    def closeEvent(self, _):
        self.main.current_preferences = None
