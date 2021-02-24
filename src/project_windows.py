from PyQt5.QtWidgets import QDockWidget  # , QFrame, QVBoxLayout, QCheckBox, QPushButton, QMessageBox
from json_lib import JSON


class Home:
    class Preview(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

            # self.init_ui()

        def closeEvent(self, _):
            for w in self.parent.menu_bar["WidgetActions"]:
                if w.text() == self.__class__.__name__:
                    w.setChecked(False)

        DefaultPosition = "Central"
        MinimumSize = (400, 400)
        pass  # TODO: Design a window that displays the current frame and acts as a preview

    class Imports(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            for w in self.parent.menu_bar["WidgetActions"]:
                if w.text() == self.__class__.__name__:
                    w.setChecked(False)

        DefaultPosition = "LeftDockWidgetArea"
        MinimumSize = (100, 600)
        pass  # TODO: Design a window where video, audio, and images can be dragged and dropped along with a QFileDialog

    class Timeline(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            for w in self.parent.menu_bar["WidgetActions"]:
                if w.text() == self.__class__.__name__:
                    w.setChecked(False)

        DefaultPosition = "BottomDockWidgetArea"
        MinimumSize = (400, 150)
        pass  # TODO: Design a window with a template timeline that updates to the current project

    class Filter(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            for w in self.parent.menu_bar["WidgetActions"]:
                if w.text() == self.__class__.__name__:
                    w.setChecked(False)

        DefaultPosition = "RightDockWidgetArea"
        MinimumSize = (150, 600)
        pass  # TODO: Design a window that allows you to add filters to the current frame

    class Properties(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            for w in self.parent.menu_bar["WidgetActions"]:
                if w.text() == self.__class__.__name__:
                    w.setChecked(False)

        DefaultPosition = "RightDockWidgetArea"
        MinimumSize = (150, 600)
        pass  # TODO: Design a window that allows you to edit Filters (for now)

    class History(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            for w in self.parent.menu_bar["WidgetActions"]:
                if w.text() == self.__class__.__name__:
                    w.setChecked(False)

        DefaultPosition = "LeftDockWidgetArea"
        MinimumSize = (150, 600)
        pass  # TODO: Design a window that displays project history (for undo/redo)

    class EditorWindow(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            for w in self.parent.menu_bar["WidgetActions"]:
                if w.text() == self.__class__.__name__:
                    w.setChecked(False)

        DefaultPosition = "TopDockWidgetArea"
        MinimumSize = (450, 600)
        pass  # TODO: Design a window that acts as a built in file editor for imported items and specific frames

    class PresetManager(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            for w in self.parent.menu_bar["WidgetActions"]:
                if w.text() == self.__class__.__name__:
                    w.setChecked(False)

        DefaultPosition = "TopDockWidgetArea"
        MinimumSize = (450, 600)
        pass  # TODO: Design a window that holds saved presets and also allows new presets to be made with a name
