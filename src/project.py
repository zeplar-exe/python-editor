import os
import moviepy.editor as editor
from pathlib import Path
from shutil import copytree
from PyQt5.QtWidgets import QFileDialog
from json_lib import JSON
from exlib import remove_directory, SafeRemoveDirectory
import logging as log

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


class Project(JSON):
    """
    Project class, mainly for directory management
    """

    def __init__(self, main_class, directory, app_directory, temporary=False, opening=None):
        self.current_directory = app_directory
        self.project_directory = directory
        self.main_class = main_class
        self.saved = False
        self.source_video = None
        self.source_video_path = ""

        self.FPS = 30
        self.current_frame = 0
        self.frame_number = 0

        self.temporary = temporary
        self.project_data = {
            "imports.csv": {},
            "source.mp4": {}
        }

        if opening is None:
            os.mkdir(directory)
            for direc in self.project_data:
                direc = os.path.join(directory, direc)
                open(direc, "x").close()
                self.write_json(direc, {})

        if not self.project_data["source.mp4"]:
            editor.ColorClip((500, 500), (50, 50, 50), duration=5).write_videofile(
                os.path.join(directory, "source.mp4"), fps=self.FPS, logger=None
            )

        i_dir = os.path.join(directory, "imports.csv")
        self.source_video = editor.VideoFileClip(os.path.join(directory, "source.mp4"))
        self.source_video_path = os.path.join(self.project_directory, "source.mp4")
        self.project_data["source.mp4"] = self.source_video

        self.SetFrame(0)

        self.imports = self.get_json(i_dir)
        self.project_data["imports.csv"] = self.imports

    def save(self):
        """
        Handles save command
        """
        if self.current_directory in Path(self.project_directory).parents:
            new = self.save_as()
            return new
        else:
            for direc in self.project_data:
                self.write_json(os.path.join(self.project_directory, direc), self.project_data[direc])

            self.source_video.write_videofile(os.path.join(self.project_directory, "source.mp4"), fps=self.FPS, logger=None)

        return self

    def save_as(self):
        """
        Handles save as command
        """
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        if dialog.exec_():
            file = dialog.selectedFiles()[0]
            if Path(self.project_directory).parent == self.current_directory:
                remove_directory(file)
                copytree(self.project_directory, file)
                SafeRemoveDirectory(self.main_class, self.project_directory)
            else:
                self.save()
                os.removedirs(file)
                copytree(self.project_directory, file)
            return Project(self.main_class, file, self.current_directory, opening=True)

    def get_directory(self):
        """
        Sets self.project_directory to path
        """
        return self.project_directory

    def SetFrame(self, num):
        self.frame_number = num
        self.current_frame = self.source_video.get_frame(self.frame_number)
        if "Preview" in self.main_class.dock_widgets:
            preview = self.main_class.dock_widgets["Preview"]
            preview.UpdatePreview(preview.main_label)
