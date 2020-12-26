import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QMenuBar
from PyQt5.QtCore import Qt, QEvent
from json_lib import JSON
from preferences_window import PreferencesApplication as pref_app
#import graphics as gp

PREFERENCES_FILE = "user_preferences.json"

def compare_dict_keys(dict_a, dict_b, yielder = None):
    """
    Compares the keys of two dictionaries, checking if they both have the same keys.
    """
    for key in dict_a:
        if dict_b.get(key) is None:
            if (yielder is not None) and callable(yielder):
                yielder(key, dict_a[key], True)
            else:
                return False

    for key in dict_b:
        if dict_a.get(key) is None:
            if (yielder is not None) and callable(yielder):
                yielder(key, dict_a.get(key, None), False)
            else:
                return False

    return True

class EditorApplication(QWidget, JSON):
    """
    Main class for pyqt application
    """

    def __init__(self):
        """
        Class Initiator
        """
        super().__init__()

        self.setMinimumSize(300, 225)
        self.size_x = 0
        self.size_y = 0

        self.screen = app.primaryScreen()
        self.screen_size = self.screen.size()

        self.load_json_preferences(PREFERENCES_FILE)
        self.init_ui()
        self.init_menubar()

        self.pref_dialog = pref_app(self)

    def init_ui(self):
        """
        Initiates window UI specifics
        """
        self.setWindowTitle("editor.py")
        self.size_x = (self.screen_size.width()/5)*4
        self.size_y = (self.screen_size.height()/4)*3

        data = self.get_json(PREFERENCES_FILE)
        self.setGeometry(
            data["WindowPosition"]["X"],
            data["WindowPosition"]["Y"],
            int(self.size_x),
            int(self.size_y)
        )

    def init_menubar(self):
        """
        Initiates window toolbar
        """
        layout = QGridLayout()
        self.setLayout(layout)

        menu_bar = QMenuBar()
        layout.addWidget(menu_bar, 0, 0)

        action_file = menu_bar.addMenu("File")
        action_file.addAction("New")
        action_file.addAction("Open")
        action_file.addAction("Save")
        action_file.addSeparator()
        action_file.addAction("Quit").triggered.connect(self.close)

        action_file = menu_bar.addMenu("Edit")
        action_file.addAction("Undo")
        action_file.addAction("Redo")
        action_file.addSeparator()
        def preferences_():
            """
            Instiantates preferences window
            """
            self.pref_dialog.show()
        action_file.addAction("Preferences").triggered.connect(preferences_)

        layout.addWidget(menu_bar)

    def changeEvent(self, event):
        """
        Handles event queue
        """
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMaximized:
                existing_data = self.get_json(PREFERENCES_FILE)
                existing_data["maximized"] = True
                self.write_json(PREFERENCES_FILE, existing_data)
            else:
                existing_data = self.get_json(PREFERENCES_FILE)
                existing_data["maximized"] = False
                self.write_json(PREFERENCES_FILE, existing_data)

    def moveEvent(self, event):
        """
        Handles event queue
        """
        if event.type() == QEvent.Move:
            data = self.get_json(PREFERENCES_FILE)
            pos = event.pos()
            data["WindowPosition"]["X"] = pos.x()
            data["WindowPosition"]["Y"] = pos.y()
            self.write_json(PREFERENCES_FILE, data)

    def load_json_preferences(self, file):
        """
        Reads preferences json file and loads neccessary properties and functions.
        If json data does not exist, it is created.
        """

        data = self.get_json(file)
        if (not data.get("JSONLoaded", False)) or (not compare_dict_keys(self.user_preferences_template, data)):
            def update(key, value, addition):
                """
                Updates JSON data based on 'value'
                """
                if data.get("JSONLoaded", False):
                    value = data.get(key, value)

                if addition is True:
                    data.update({key: value})
                else:
                    data.pop(key)

            compare_dict_keys(self.user_preferences_template, data.copy(), update)
            data = self.write_json(file, data)

        if data.get("maximized") is True:
            self.showMaximized()

        if data.get("fullscreen") is True:
            self.showFullScreen()
        elif self.isFullScreen():
            self.showNormal()
            self.resize(int(self.size_x), int(self.size_y))

    user_preferences_template = {
        "JSONLoaded": True,
        "maximized": False,
        "fullscreen": False,

        "WindowPosition": {
            "X": 0,
            "Y": 0
        }
    }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    EditorApplication().show()
    sys.exit(app.exec_())
