import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QMenuBar, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent
from project import Project
from json_lib import JSON
from exlib import remove_directory, compare_dict_keys, request_save
from preferences_window import PreferencesApplication as pref_app

CURRENT_DIRECTORY = Path(__file__).parent.absolute()
PREFERENCES_FILE = "user_preferences.json"
REQUIRED_PROJECT_FILES = {
    "directory": [],

    "file": [
        "clips.json",
        "images.json"
    ],
}

class EditorApplication(QWidget, JSON):
    """
    Main class for pyqt application
    """

    def __init__(self):
        super().__init__()

        self.setMinimumSize(300, 225)
        self.current_project = None
        self.current_preferences = None
        self.size_x = 0
        self.size_y = 0

        self.screen_size = app.primaryScreen().size()

        self.load_json_preferences(PREFERENCES_FILE)
        self.init_ui()
        self.init_menubar()
        self.init_project()

        #self.pref_dialog = pref_app(self)

    def init_project(self):
        """
        Creates base project file for temporary use
        """
        json_data = self.get_json(PREFERENCES_FILE)
        last_session = json_data["last_session_directory"]

        if os.path.isdir(last_session):
            self.current_project = Project(last_session, CURRENT_DIRECTORY, False, True)
            return
        else:
            json_data["last_session_directory"] = ""
            self.write_json(PREFERENCES_FILE, json_data)
            self.current_project = Project(
                os.path.join(CURRENT_DIRECTORY, "PE_TMP_FOLDER"), 
                CURRENT_DIRECTORY, 
                True
            )

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
            response, dialog = request_save(self.current_project)
            if response == QMessageBox.Ok:
                if CURRENT_DIRECTORY in Path(self.current_project.get_directory()).parents:
                    remove_directory(self.current_project.get_directory())
                self.current_project = Project(os.path.join(CURRENT_DIRECTORY, "PE_TMP_FOLDER"), CURRENT_DIRECTORY, True)
            elif isinstance(dialog, QMessageBox):
                dialog.reject()
            else:
                if CURRENT_DIRECTORY in Path(self.current_project.get_directory()).parents:
                    remove_directory(self.current_project.get_directory())
                self.current_project = Project(os.path.join(CURRENT_DIRECTORY, "PE_TMP_FOLDER"), CURRENT_DIRECTORY, True)
        new_f = action_file.addAction("New")
        new_f.setShortcut("Ctrl+N")
        new_f.setToolTip("New Project")
        new_f.triggered.connect(new_file)

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
                    if CURRENT_DIRECTORY in Path(self.current_project.get_directory()).parents:
                        response, dialog = request_save(self.current_project)
                        if response == QMessageBox.Ok:
                            remove_directory(self.current_project.get_directory())
                            self.current_project = Project(dir_, CURRENT_DIRECTORY, True)
                        elif isinstance(dialog, QMessageBox):
                            dialog.reject()
        open_f = action_file.addAction("Open")
        open_f.setShortcut("Ctrl+O")
        open_f.setToolTip("Open Project")
        open_f.triggered.connect(open_file)

        def save_file():
            self.current_project = self.current_project.save()
        save = action_file.addAction("Save")
        save.setShortcut("Ctrl+S")
        save.setToolTip('Save File')
        save.triggered.connect(save_file)

        def save_file_as():
            self.current_project = self.current_project.save_as()
        save_f_as = action_file.addAction("Save As")
        save_f_as.setShortcut("Ctrl+Shift+S")
        save_f_as.setToolTip("Save Project As")
        save_f_as.triggered.connect(save_file_as)

        action_file.addSeparator()
        quit_b = action_file.addAction("Quit")
        quit_b.setShortcut("Alt+F4")
        quit_b.setToolTip("Quit Application")
        quit_b.triggered.connect(self.close)

        action_file = menu_bar.addMenu("Edit")
        undo = action_file.addAction("Undo")
        undo.setShortcut("Ctrl+Z")
        undo.setToolTip("Undo Action")
        redo = action_file.addAction("Redo")
        redo.setShortcut("Ctrl+Shift+Z")
        redo.setToolTip("Redo Action")

        action_file.addSeparator()
        def preferences_():
            """
            Instiantates preferences window
            """
            self.current_preferences = pref_app(self)
            self.current_preferences.show()
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
        c_d = self.current_project.get_directory()
        if self.current_project.temporary:
            response, dialog = request_save(self.current_project)

            if response == QMessageBox.Ok:
                remove_directory(c_d)
            elif response == QMessageBox.Cancel:
                dialog.reject()
            else:
                remove_directory(c_d)
            return

        if os.path.isdir(c_d):
            if request_save(self.current_project):
                dialog = QMessageBox()
                dialog.setText("Project has been modified and is not saved.")
                dialog.setInformativeText("Would you like to save your data?")
                dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.No)

                ret = dialog.exec_()
                if ret:
                    if ret == QMessageBox.Ok:
                        self.current_project.save()
                    elif ret == QMessageBox.No:
                        remove_directory(c_d)
                else:
                    remove_directory(c_d)

            json_data = self.get_json(PREFERENCES_FILE)
            if Path(json_data["last_session_directory"]).parent != CURRENT_DIRECTORY:
                json_data["last_session_directory"] = c_d
                self.write_json(PREFERENCES_FILE, json_data)

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
        "last_session_directory": "",

        "WindowPosition": {
            "X": 0,
            "Y": 0
        }
    }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    EditorApplication().show()
    sys.exit(app.exec_())
