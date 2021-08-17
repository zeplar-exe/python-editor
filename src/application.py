import sys
import os
from pathlib import Path
import logging as log

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent
# import moviepy

from project import Project
from project_windows import Home

from json_lib import JSON
from exlib import remove_directory, compare_dict_keys, request_save, SafeRemoveDirectory
from preferences_window import PreferencesApplication as pref_app

logger = log.getLogger()
log.basicConfig(
    filename='log_file.log',
    level=log.DEBUG,
    format='''------------------------------------
Timestamp: %(asctime)s
Message: %(message)s
------------------------------------
'''
)
# logger.disabled = True

CURRENT_DIRECTORY = Path(__file__).parent.absolute()
PREFERENCES_FILE = "user_preferences.json"
PRESETS_FILE = "user_presets.json"


class EditorApplication(QMainWindow, JSON):
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

        self.dock_widgets = {}
        self.menu_bar = {}
        self.menu_bar_size = 20

        self.screen_size = app.primaryScreen().size()

        self.load_json_preferences(PREFERENCES_FILE)
        self.init_menubar()
        self.init_project()
        self.load_json_presets(PRESETS_FILE)
        self.init_ui()

    def init_project(self):
        """
        Creates base project file for temporary use
        """
        json_data = self.get_json(PREFERENCES_FILE)
        last_session = json_data["last_session_directory"]

        if os.path.isdir(last_session):
            self.current_project = Project(self, last_session, CURRENT_DIRECTORY, False, True)
            return
        else:
            json_data["last_session_directory"] = ""
            self.write_json(PREFERENCES_FILE, json_data)
            self.current_project = Project(
                self,
                os.path.join(CURRENT_DIRECTORY, "PE_TMP_FOLDER"),
                CURRENT_DIRECTORY,
                True
            )

    def init_ui(self):
        """
        Initiates window UI specifics
        """
        self.setWindowTitle("editor.py")
        self.size_x = int((self.screen_size.width() / 5) * 4)  # 4/5 of the screen size
        self.size_y = int((self.screen_size.height() / 4) * 3)  # 3/4 of the screen size
        data = self.get_json(PREFERENCES_FILE)

        if data["WindowSize"] == 0:
            data["WindowSize"] = {}
            data["WindowSize"]["X"] = self.size_x
            data["WindowSize"]["Y"] = self.size_y
            data = self.write_json(PREFERENCES_FILE, data)

        self.setGeometry(
            data["WindowPosition"]["X"],
            data["WindowPosition"]["Y"],
            data["WindowSize"]["X"],
            data["WindowSize"]["Y"]
        )

    def init_menubar(self):
        """
        Initiates window menubar
        """
        menu_bar = self.menuBar()
        self.menu_bar["Main"] = menu_bar
        self.menu_bar["WidgetActions"] = []  # OPTIMIZE: Create a better system of getting certain actions
        menu_bar.setFixedSize(
            int(self.screen_size.width()),
            self.menu_bar_size
        )
        menu_bar.setStyleSheet("background-color: grey")

        action_file = menu_bar.addMenu("File")

        def new_file():
            response, dialog = request_save(self.current_project)
            if response == QMessageBox.Ok:
                if CURRENT_DIRECTORY in Path(self.current_project.get_directory()).parents:
                    SafeRemoveDirectory(self, self.current_project.get_directory())
                self.current_project = Project(os.path.join(CURRENT_DIRECTORY, "PE_TMP_FOLDER"), CURRENT_DIRECTORY,
                                               True)
            elif isinstance(dialog, QMessageBox):
                dialog.reject()
            else:
                if CURRENT_DIRECTORY in Path(self.current_project.get_directory()).parents:
                    SafeRemoveDirectory(self, self.current_project.get_directory())
                self.current_project = Project(
                    self,
                    os.path.join(CURRENT_DIRECTORY, "PE_TMP_FOLDER"),
                    CURRENT_DIRECTORY,
                    True
                )

        new_f = action_file.addAction("New")
        new_f.setShortcut("Ctrl+N")
        new_f.triggered.connect(new_file)

        def open_file():
            dialog = QFileDialog()
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
            dialog.setFileMode(QFileDialog.DirectoryOnly)

            if dialog.exec_():
                dir_ = dialog.selectedFiles()[0]
                if CURRENT_DIRECTORY in Path(self.current_project.get_directory()).parents:
                    response, dialog = request_save(self.current_project)
                    if response == QMessageBox.Ok:
                        SafeRemoveDirectory(self, self.current_project.get_directory())
                        self.current_project = Project(self, dir_, CURRENT_DIRECTORY, True)
                    elif isinstance(dialog, QMessageBox):
                        dialog.reject()

        open_f = action_file.addAction("Open")
        open_f.setShortcut("Ctrl+O")
        open_f.triggered.connect(open_file)

        def save_file():
            self.current_project = self.current_project.save()

        save = action_file.addAction("Save")
        save.setShortcut("Ctrl+S")
        save.triggered.connect(save_file)

        def save_file_as():
            self.current_project = self.current_project.save_as()

        save_f_as = action_file.addAction("Save As")
        save_f_as.setShortcut("Ctrl+Shift+S")
        save_f_as.triggered.connect(save_file_as)

        action_file.addSeparator()
        quit_b = action_file.addAction("Quit")
        quit_b.setShortcut("Alt+F4")
        quit_b.triggered.connect(self.close)

        action_file = menu_bar.addMenu("Edit")
        undo = action_file.addAction("Undo")
        undo.setShortcut("Ctrl+Z")
        redo = action_file.addAction("Redo")
        redo.setShortcut("Ctrl+Shift+Z")

        action_file.addSeparator()

        def preferences_():
            """
            Instantiates preferences window
            """
            if self.current_preferences is None:
                self.current_preferences = pref_app(self)
                self.current_preferences.show()

        action_file.addAction("Preferences").triggered.connect(preferences_)

        action_file = menu_bar.addMenu("Widgets")

        def HandleWidget(name):
            alert = QMessageBox()
            alert.setWindowTitle("In Development")
            alert.setInformativeText("Sorry! This feature isn't available yet.")
            alert.setStandardButtons(QMessageBox.Ok)
            alert.setIcon(QMessageBox.Information)
            return alert.exec_()

            # if name in self.dock_widgets:
            #     self.removeDockWidget(self.dock_widgets[name])
            #
            #     j_data = self.get_json(PRESETS_FILE)
            #     for d in j_data["Presets"][j_data["Selected"]]:
            #         if d["win"] == name:
            #             j_data["Presets"][j_data["Selected"]].remove(d)
            #             self.write_json(PRESETS_FILE, j_data)
            #             break
            # else:
            #     win = getattr(Home, name, None)(self)
            #     if win:
            #         j_data = self.get_json(PRESETS_FILE)
            #         if name not in j_data["Presets"][j_data["Selected"]]:
            #             j_data["Presets"][j_data["Selected"]].append(
            #                 {
            #                     "win": name,
            #                     "pos": win.DefaultPosition,
            #                     "size": win.MinimumSize
            #                 }
            #             )
            #         self.write_json(PRESETS_FILE, j_data)
            #         win.setWindowTitle(name)
            #         if win.DefaultPosition == "Central":
            #             self.setCentralWidget(win)
            #         else:
            #             for widget in self.dock_widgets:
            #                 if widget.DefaultPosition == win.DefaultPosition:
            #                     self.tabifyDockWidget(widget, win)
            #                     break
            #             else:
            #                 self.addDockWidget(getattr(Qt, win.DefaultPosition), win)
            #         win.show()
            #         self.dock_widgets[name] = win
            #     else:
            #         log.error(f"Widget {name} does not exist.")

        preview = action_file.addAction("Preview")
        self.menu_bar["WidgetActions"].append(preview)
        preview.setCheckable(True)

        preview.triggered.connect(lambda: HandleWidget("Preview"))

        imports = action_file.addAction("Imports")
        self.menu_bar["WidgetActions"].append(imports)
        imports.setCheckable(True)

        imports.triggered.connect(lambda: HandleWidget("Imports"))

        timeline = action_file.addAction("Timeline")
        self.menu_bar["WidgetActions"].append(timeline)
        timeline.setCheckable(True)

        timeline.triggered.connect(lambda: HandleWidget("Timeline"))

        filter_ = action_file.addAction("Filter")
        self.menu_bar["WidgetActions"].append(filter_)
        filter_.setCheckable(True)

        filter_.triggered.connect(lambda: HandleWidget("Filter"))

        properties = action_file.addAction("Properties")
        self.menu_bar["WidgetActions"].append(properties)
        properties.setCheckable(True)

        properties.triggered.connect(lambda: HandleWidget("Properties"))

        action_file.addSeparator()
        presets = action_file.addAction("Preset Manager")

        def presets_():
            pass

        presets.triggered.connect(presets_)

        action_file.addSeparator()

    def changeEvent(self, event):
        """
        Handles event queue
        """
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() == Qt.WindowMaximized:
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

    def resizeEvent(self, event):
        """
        Handles move event queue
        """
        if event.type() == QEvent.Resize:
            data = self.get_json(PREFERENCES_FILE)
            size = event.size()
            data["WindowSize"]["X"] = size.width()
            data["WindowSize"]["Y"] = size.height()
            self.write_json(PREFERENCES_FILE, data)

    def closeEvent(self, _):
        """
        Handles close events
        """

        c_d = self.current_project.get_directory()
        if self.current_project.temporary:
            response, dialog = request_save(self.current_project)

            if response == QMessageBox.Ok:
                SafeRemoveDirectory(self, c_d)
            elif response == QMessageBox.Cancel:
                dialog.reject()
            else:
                SafeRemoveDirectory(self, c_d)
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
                        SafeRemoveDirectory(self, c_d)
                else:
                    SafeRemoveDirectory(self, c_d)

            json_data = self.get_json(PREFERENCES_FILE)
            if Path(json_data["last_session_directory"]).parent != CURRENT_DIRECTORY:
                json_data["last_session_directory"] = c_d
                self.write_json(PREFERENCES_FILE, json_data)

    def load_json_preferences(self, file):
        """
        Reads preferences json file and loads necessary properties and functions.
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
        elif self.get_json(PREFERENCES_FILE)["debug_mode"]:
            copy = self.user_preferences_template.copy()
            copy["debug_mode"] = True
            data = self.write_json(PREFERENCES_FILE, copy)

        if data.get("maximized") is True:
            self.showMaximized()

        if data.get("fullscreen") is True:
            self.showFullScreen()
        elif self.isFullScreen():
            self.showNormal()
            self.resize(data["WindowSize"]["X"], data["WindowSize"]["Y"])

    user_preferences_template = {
        "JSONLoaded": True,
        "maximized": False,
        "fullscreen": False,
        "warn_non_save": True,
        "debug_mode": False,

        "WindowPosition": {
            "X": 0,
            "Y": 0
        },

        "WindowSize": 0,

        "last_session_directory": "",
        "last_session_preset": "default",
    }

    def load_json_presets(self, file):
        """
        Loads previously stored or the default window preset
        """
        data = self.get_json(file)
        if (not data.get("default")) or (not compare_dict_keys(self.user_presets_template, data.copy())):
            def update(key, value, addition):
                """
                Updates JSON data based on 'value'
                """
                if data.get("default"):
                    value = data.get(key, value)

                if addition is True:
                    data.update({key: value})
                else:
                    data.pop(key)

            compare_dict_keys(self.user_presets_template, data.copy(), update)
            data = self.write_json(file, data)
        elif self.get_json(PREFERENCES_FILE)["debug_mode"]:
            data = self.write_json(PRESETS_FILE, self.user_presets_template)
        preferences = self.get_json(PREFERENCES_FILE)

        if data["Selected"] not in data["Presets"]:
            data["Selected"] = "Default"
            self.write_json(PRESETS_FILE, self.user_presets_template)
            preferences["last_session_preset"] = "Default"
            preferences = self.write_json(PREFERENCES_FILE, preferences)

        if preferences["last_session_preset"] not in data:
            preferences["last_session_preset"] = "Default"
            data["Selected"] = "Default"

        try:
            location = data["Presets"][preferences["last_session_preset"]]
            for window in location:
                for a in self.menu_bar["WidgetActions"]:
                    if a.text() == window["win"]:
                        a.setChecked(True)

                win = getattr(Home, window["win"], None)
                if win is not None:
                    win = win(self)
                    if window["pos"] is None:
                        window["pos"] = win.DefaultPosition

                    if window["size"] is None:
                        window["size"] = win.MinimumSize

                    self.dock_widgets[window["win"]] = win
                    win.setWindowTitle(window["win"])
                    win.setMinimumSize(*win.MinimumSize)
                    win.resize(*window["size"])

                    if window["pos"] == "Central":
                        self.setCentralWidget(win)
                    else:
                        self.addDockWidget(Qt.__getattribute__(Qt, window["pos"]), win)
                    win.show()
        except:
            self.current_project.source_video.close()
            raise
        # FIXME: Fix dock widget positions and sizes being inconsistent upon being added
        # NOTE: Expected window display: https://gyazo.com/c319614c348a55129762149099398769

    user_presets_template = {
        "Selected": "Default",
        "Presets": {
            "Default": [
                {
                    "win": "Preview",
                    "pos": None,
                    "size": None
                },
                {
                    "win": "Imports",
                    "pos": None,
                    "size": None
                },
                {
                    "win": "Timeline",
                    "pos": None,
                    "size": None
                },
                {
                    "win": "Properties",
                    "pos": None,
                    "size": None
                },
                {
                    "win": "Filter",
                    "pos": None,
                    "size": None
                },
            ]
        }
    }


if __name__ == "__main__":
    # noinspection PyBroadException
    application = None
    try:
        if os.path.isdir("PE_TMP_FOLDER"):
            remove_directory("PE_TMP_FOLDER")

        app = QApplication(sys.argv)
        application = EditorApplication()
        application.show()
        sys.exit(app.exec_())
    except:
        if os.path.isdir("PE_TMP_FOLDER"):
            # noinspection PyBroadException
            try:
                SafeRemoveDirectory(application, "PE_TMP_FOLDER")
            except Exception:
                remove_directory("PE_TMP_FOLDER")
        raise
