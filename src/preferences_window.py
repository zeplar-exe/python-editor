from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QCheckBox, QPushButton, QDialog
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

        textbox = QCheckBox("Open editor in fullscreen mode")
        if pref_data.get("fullscreen") is True:
            textbox.setChecked(True)
        grid.addWidget(textbox)

        close_button = QPushButton("Exit without Saving")
        grid.addWidget(close_button)
        def close_():
            dialog = QDialog()
            layout = QVBoxLayout()
            dialog.setLayout(layout)
            dialog.resize(125, 75)
            dialog.setMaximumSize(125, 75)
            dialog.setMinimumSize(125, 75)

            dialog.setWindowTitle("Are you sure?")
            conf = QPushButton("Confirm", dialog)
            layout.addWidget(conf, alignment=Qt.AlignLeft | Qt.AlignBottom)
            ret = QPushButton("Take me back", dialog)
            layout.addWidget(ret, alignment=Qt.AlignRight | Qt.AlignBottom)

            def accept_():
                self.close()
                dialog.accept()

            def cancel_():
                dialog.reject()

            conf.clicked.connect(accept_)
            ret.clicked.connect(cancel_)

            dialog.exec_()

        close_button.clicked.connect(close_)

        close_save_button = QPushButton("Save and Exit")
        grid.addWidget(close_save_button)
        def save_close():
            close_save_button.setCheckable(False)

            data = {"fullscreen": textbox.isChecked()}
            new = self.get_json(PREFERENCES_FILE)
            for key in data:
                new[key] = data[key]

            self.write_json(PREFERENCES_FILE, new)
            main.load_json_preferences(PREFERENCES_FILE)

            self.close()

        close_save_button.clicked.connect(save_close)
