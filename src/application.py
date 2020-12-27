import sys
import os
from shutil import copyfile
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QMenuBar, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent
from json_lib import JSON
from preferences_window import PreferencesApplication as pref_app

PREFERENCES_FILE = "user_preferences.json"
REQUIRED_PROJECT_FILES = {
    "directory": [
        "clips",
        "images"
    ],

    "file": [],
}

def remove_directory(dir_):
    """
    Recursively removes a directory and files/directories inside of it
    """
    for file in os.listdir(dir_):
        full_name = os.path.join(dir_, file)
        if os.path.isdir(full_name):
            remove_directory(full_name)
            os.removedirs(full_name)
        else:
            os.remove(full_name)

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
        self.project_directory = None
        self.size_x = 0
        self.size_y = 0

        self.screen = app.primaryScreen()
        self.screen_size = self.screen.size()

        self.load_json_preferences(PREFERENCES_FILE)
        self.init_ui()
        self.init_menubar()
        self.init_project()

        self.pref_dialog = pref_app(self)

    def init_project(self):
        """
        Creates base project file for temporary use
        """
        if self.project_directory is None:
            self.project_directory = os.path.join("C:\\tmp", "PE_TMP_FOLDER")

        if os.path.isdir(self.project_directory):
            remove_directory(self.project_directory)

        os.mkdir(self.project_directory)
        os.mkdir(os.path.join(self.project_directory, "clips"))
        os.mkdir(os.path.join(self.project_directory, "images"))

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

        def new_file():
            self.init_project()
        action_file.addAction("New").triggered.connect(new_file)

        def open_file():
            dialog = QFileDialog()
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
            dialog.setFileMode(QFileDialog.DirectoryOnly)

            def fail_dialog(reject, missing):
                """
                Dialog to display when an invalid directory is chosen
                """
                fail = QMessageBox()
                fail.setText("File to open should be a valid project directory.")
                fail.setInformativeText("Missing {0}".format(", ".join(missing)))
                fail.setIcon(QMessageBox.Information)
                fail.setStandardButtons(QMessageBox.Ok)
                fail.exec_()
                reject.reject()
                open_file()

            if dialog.exec_():
                dir_ = dialog.selectedFiles()[0]
                missing = []

                for req_d in REQUIRED_PROJECT_FILES["directory"]:
                    if not os.path.isdir(os.path.join(dir_, req_d)):
                        missing.append(req_d)

                for req_f in REQUIRED_PROJECT_FILES["file"]:
                    if not os.path.isfile(os.path.join(dir_, req_f)):
                        missing.append(req_f)

                if missing:
                    fail_dialog(dialog, missing)
                    return
                else:
                    remove_directory(self.project_directory)
                    self.project_directory = dir_
                    self.init_project()
        action_file.addAction("Open").triggered.connect(open_file)

        def save_file():
            dialog = QFileDialog()
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
            dialog.setFileMode(QFileDialog.DirectoryOnly)

            def fail_dialog(reject):
                """
                Dialog to display when an invalid directory is chosen
                """
                fail = QMessageBox()
                fail.setText("Directory should be empty")
                fail.setInformativeText("Please choose a different directory.")
                fail.setIcon(QMessageBox.Information)
                fail.setStandardButtons(QMessageBox.Ok)
                fail.exec_()
                reject.reject()
                open_file()

            if dialog.exec_():
                dir_ = dialog.selectedFiles()[0]

                if len(os.listdir(dir_)) == 0:
                    original = self.project_directory
                    copyfile(self.project_directory, dir_)
                    self.project_directory = dir_
                    remove_directory(original)
                else:
                    fail_dialog(dialog)
        action_file.addAction("Save").triggered.connect(save_file)
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
        Handles move event queue
        """
        if event.type() == QEvent.Move:
            data = self.get_json(PREFERENCES_FILE)
            pos = event.pos()
            data["WindowPosition"]["X"] = pos.x()
            data["WindowPosition"]["Y"] = pos.y()
            self.write_json(PREFERENCES_FILE, data)

    def closeEvent(self, _):
        """
        Handles close events
        """
        if os.path.isdir(self.project_directory):
            child = Path(self.project_directory)
            test_root = Path("C:\\tmp")

            if test_root in child.parents:
                remove_directory(self.project_directory)

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
        "warn_non_save": True,

        "WindowPosition": {
            "X": 0,
            "Y": 0
        }
    }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    EditorApplication().show()
    sys.exit(app.exec_())
