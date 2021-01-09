from PyQt5.QtWidgets import QDockWidget  # , QFrame, QVBoxLayout, QCheckBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from json_lib import JSON


class Home:
    class Preview(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent

        DefaultPosition = Qt.TopDockWidgetArea
        pass  # TODO: Design a window that displays the current frame and acts as a preview

    class Imports(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.setParent(parent)

        DefaultPosition = Qt.LeftDockWidgetArea
        pass  # TODO: Design a window where video, audio, and images can be dragged and dropped along with a QFileDialog

    class Timeline(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.setParent(parent)

        DefaultPosition = Qt.BottomDockWidgetArea
        pass  # TODO: Design a window with a template timeline that updates to the current project

    class Filter(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.setParent(parent)

        DefaultPosition = Qt.RightDockWidgetArea
        pass  # TODO: Design a window that allows you to add filters to the current frame

    class Properties(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.setParent(parent)

        DefaultPosition = Qt.RightDockWidgetArea
        pass  # TODO: Design a window that allows you to edit Filters (for now)

    class ProjectHistory(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.setParent(parent)

        DefaultPosition = Qt.LeftDockWidgetArea
        pass  # TODO: Design a window that displays project history (for undo/redo)

    class EditorWindow(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.setParent(parent)

        DefaultPosition = Qt.TopDockWidgetArea
        pass  # TODO: Design a window that acts as a built in file editor for imported items and specific frames

    class PresetManager(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.setParent(parent)

        DefaultPosition = Qt.TopDockWidgetArea
        pass  # TODO: Design a window that holds saved presets and also allows new presets to be made with a name
