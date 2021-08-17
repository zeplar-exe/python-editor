from PyQt5.QtWidgets import (
    QWidget, QStyle, QPushButton,
    QDockWidget, QLabel, QVBoxLayout,
    QSizePolicy, QScrollArea, QFileDialog
)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import Qt, QUrl, QSize
from json_lib import JSON, CSV
from time import sleep
import logging as log
import os

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


expanding_size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


def Close(obj):
    obj.updating = False
    obj.update_var.terminate()

    obj.parent.removeDockWidget(obj.parent.dock_widgets[object.__class__.__name__])

    j_data = JSON.get_json("user_presets.json")
    for d in j_data["Presets"][j_data["Selected"]]:
        if d["win"] == obj.__class__.__name__:
            j_data["Presets"][j_data["Selected"]].remove(d)
            JSON.write_json("user_presets.json", j_data)
            break

    for w in obj.parent.menu_bar["WidgetActions"]:
        if w.text() == obj.__class__.__name__:
            w.setChecked(False)


def CreateTitleBar(name, parent):
    # parent.setDisabled(True)

    parent.setContextMenuPolicy(Qt.PreventContextMenu)
    title_label = QLabel(text=name, parent=parent)
    title_label.setFont(QFont("Arial", 10))
    return title_label


class Home:
    class Preview(QDockWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)
            self.setTitleBarWidget(CreateTitleBar("Preview", self))

            self.main_label = None
            self.play_button = None
            self.media_player = None
            self.last_frame_recall = None
            self.updating = True
            self.update_var = None

            self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
            self.media_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(self.parent.current_project.source_video_path))
            )

            widget = QWidget()
            layout = QVBoxLayout()
            widget.setLayout(layout)
            self.setWidget(widget)

            label = QVideoWidget()
            # FIXME: Causes the entire screen to flicker and forces the main window to the side
            self.main_label = label

            play_button = QPushButton()
            play_button.setEnabled(False)
            play_button.setFixedHeight(24)
            play_button.setIconSize(QSize(16, 16))
            play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            play_button.clicked.connect(self.play)
            self.play_button = play_button

            self.media_player.setVideoOutput(label)
            self.media_player.stateChanged.connect(self.mediaStateChanged)
            # layout.addWidget(label)

            self.UpdatePreview(label)

        def UpdatePreview(self, label):
            return
            # frame = self.parent.current_project.frame_number
            # if frame != self.last_frame_recall:
            #     self.last_frame_recall = frame
            #     frame = self.parent.current_project.current_frame
            #
            #     height, width, channel = frame.shape
            #     bytesPerLine = 3 * width
            #     frame_image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            #
            #     pixmap = QPixmap.fromImage(frame_image)
            #
            #     label.setPixmap(pixmap.scaled(label.size(), Qt.IgnoreAspectRatio))

        def play(self):
            if self.media_player.state() == QMediaPlayer.PlayingState:
                self.media_player.pause()
            else:
                self.media_player.play()

        def mediaStateChanged(self, _):
            if self.media_player.state() == QMediaPlayer.PlayingState:
                self.play_button.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
            else:
                self.play_button.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

        def CloseMedia(self):
            self.media_player.setMedia(QMediaContent())

        def closeEvent(self, _):
            Close(self)

        DefaultPosition = "Central"
        MinimumSize = (400, 400)
        pass  # TODO: Create basic buttons for manipulating the preview

    class Imports(QDockWidget):  # TODO: Add import button to replace dropEvent for now
        def __init__(self, parent):
            super().__init__()
            imports_ref = self

            self.parent = parent
            self.setParent(parent)
            self.setTitleBarWidget(CreateTitleBar("Imports", self))
            self.setAcceptDrops(True)

            scroll = QScrollArea()
            self.setWidget(scroll)
            scroll.setWidgetResizable(True)

            import_button = QPushButton(text="Import...", parent=scroll)

            def GetFileViaDialog():
                dialog = QFileDialog()
                dialog.setFileMode(QFileDialog.ExistingFile)

                if dialog.exec_():
                    file = dialog.selectedFiles()[0]
                    dat = CSV.get_csv(self.imports_file)
                    dat.append(file)
                    CSV.write_csv(self.imports_file, dat)
                    imports_ref.Update()

            import_button.pressed.connect(GetFileViaDialog)

            class ScrollContent(QWidget):
                def __init__(self, parent_widget):
                    super().__init__(parent_widget)
                    self.parent = parent_widget

                def dragEnterEvent(self, event):
                    log.debug("dragEnterEvent Called")
                    event.accept()

                def dropEvent(self, event):  # FIXME: Does not fire
                    for url in event.mimeData().urls():
                        path = url.toLocalFile()
                        CSV.write_csv(self.imports_file, CSV.get_csv(self.imports_file).append(path))

                    imports_ref.Update()

            scroll_content = ScrollContent(scroll)

            scroll_layout = QVBoxLayout(scroll_content)
            scroll_content.setLayout(scroll_layout)
            scroll.setWidget(scroll_content)
            self.scroll_layout = scroll_layout
            self.imports_file = os.path.join(parent.current_project.get_directory(), "imports.csv")

            self.Update()

        def Update(self):
            for file in JSON.get_json(
                    self.imports_file
            ):
                self.scroll_layout.addWidget(self.File(file))

        def closeEvent(self, _):
            Close(self)

        class File(QWidget):
            def __init__(self, absolute_path, file_type="nil"):
                super().__init__()
                layout = QVBoxLayout()
                self.setLayout(layout)

                truncated_path = absolute_path[0:15]

                if truncated_path != absolute_path:
                    truncated_path += "..."

                FilePathLabel = QLabel(truncated_path)
                FileTypeLabel = QLabel(file_type)

                layout.addWidget(FilePathLabel)
                layout.addWidget(FileTypeLabel)

        DefaultPosition = "LeftDockWidgetArea"
        MinimumSize = (100, 100)
        pass  # TODO: Design a window where video, audio, and images can be dragged and dropped along with a QFileDialog

    class Timeline(QDockWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)
            self.setTitleBarWidget(CreateTitleBar("Timeline", self))

        def closeEvent(self, _):
            Close(self)

        DefaultPosition = "BottomDockWidgetArea"
        MinimumSize = (400, 100)
        pass  # TODO: Design a window with a template timeline that updates to the current project

    class Filter(QDockWidget, JSON):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)
            self.setTitleBarWidget(CreateTitleBar("Filters", self))

        def closeEvent(self, _):
            Close(self)

        DefaultPosition = "RightDockWidgetArea"
        MinimumSize = (150, 100)
        pass  # TODO: Design a window that allows you to add filters to the current frame

    class Properties(QDockWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)
            self.setTitleBarWidget(CreateTitleBar("Properties", self))

        def closeEvent(self, _):
            Close(self)

        DefaultPosition = "RightDockWidgetArea"
        MinimumSize = (150, 100)
        pass  # TODO: Design a window that allows you to edit Filters (for now)

    class PresetManager(QDockWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setParent(parent)

        def closeEvent(self, _):
            pass

        MinimumSize = (450, 100)
        pass  # TODO: Design a window that holds saved presets and also allows new presets to be made with a name
