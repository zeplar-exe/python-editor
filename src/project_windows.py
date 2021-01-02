from PyQt5.QtWidgets import QWidget  # , QFrame, QVBoxLayout, QCheckBox, QPushButton, QMessageBox
from json_lib import JSON


class Home:
    class Imports(QWidget, JSON):
        pass  # TODO: Design a window where video, audio, and images can be dragged and dropped along with a QFileDialog

    class Timeline(QWidget, JSON):
        pass  # TODO: Design a window with a template timeline that updates to the current project

    class Filter(QWidget, JSON):
        pass  # TODO: Design a window that allows you to add filters to the current frame

    class Properties(QWidget, JSON):
        pass  # TODO: Design a window that allows you to edit Filters (for now)

    class ProjectHistory(QWidget, JSON):
        pass  # TODO: Design a window that displays project history (for undo/redo)


class PlaylistEditor(QWidget, JSON):
    Imports = Home.Imports

    Properties = Home.Properties

    class EditorWindow(QWidget, JSON):
        pass  # TODO: Design a window that acts as a built in file editor for imported items
