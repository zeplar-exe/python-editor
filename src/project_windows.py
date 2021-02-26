from PyQt5.QtWidgets import QDockWidget  # , QFrame, QVBoxLayout, QCheckBox, QPushButton, QMessageBox
from json_lib import JSON


def Close(obj):
    obj.parent.removeDockWidget(obj.parent.dock_widgets[object.__class__.__name__])

    j_data = obj.get_json("user_presets.json")
    for d in j_data["Presets"][j_data["Selected"]]:
        if d["win"] == obj.__class__.__name__:
            j_data["Presets"][j_data["Selected"]].remove(d)
            obj.write_json("user_presets.json", j_data)
            break

    for w in obj.parent.menu_bar["WidgetActions"]:
        if w.text() == obj.__class__.__name__:
            w.setChecked(False)


class Home:
    class Preview(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            Close(self)

        DefaultPosition = "Central"
        MinimumSize = (400, 400)
        pass  # TODO: Design a window that displays the current frame and acts as a preview

    class Imports(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            Close(self)

        DefaultPosition = "LeftDockWidgetArea"
        MinimumSize = (100, 600)
        pass  # TODO: Design a window where video, audio, and images can be dragged and dropped along with a QFileDialog

    class Timeline(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            Close(self)

        DefaultPosition = "BottomDockWidgetArea"
        MinimumSize = (400, 150)
        pass  # TODO: Design a window with a template timeline that updates to the current project

    class Filter(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            Close(self)

        DefaultPosition = "RightDockWidgetArea"
        MinimumSize = (150, 600)
        pass  # TODO: Design a window that allows you to add filters to the current frame

    class Properties(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            Close(self)

        DefaultPosition = "RightDockWidgetArea"
        MinimumSize = (150, 600)
        pass  # TODO: Design a window that allows you to edit Filters (for now)

    class History(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            Close(self)

        DefaultPosition = "LeftDockWidgetArea"
        MinimumSize = (150, 600)
        pass  # TODO: Design a window that displays project history (for undo/redo)

    class EditorWindow(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            Close(self)

        DefaultPosition = "TopDockWidgetArea"
        MinimumSize = (450, 600)
        pass  # TODO: Design a window that acts as a built in file editor for imported items and specific frames

    class PresetManager(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            Close(self)

        DefaultPosition = "TopDockWidgetArea"
        MinimumSize = (450, 600)
        pass  # TODO: Design a window that holds saved presets and also allows new presets to be made with a name
