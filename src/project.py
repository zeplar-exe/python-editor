import os
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog
from json_lib import JSON
from exlib import remove_directory
from shutil import copyfile

class Project(JSON):
    """
    Project class, mainly for directory management
    """

    def __init__(self, directory, app_directory, temporary, opening = None):
        self.current_directory = app_directory
        self.project_directory = directory
        self.saved = False
        self.temporary = temporary
        self.project_data = {
            "clips.json": [],
            "images.json": []
        }

        if opening is None:
            os.mkdir(directory)
            c_dir = os.path.join(directory, "clips.json")
            i_dir = os.path.join(directory, "images.json")
            open(c_dir, "x").close()
            self.write_json(c_dir, {})
            open(i_dir, "x").close()
            self.write_json(i_dir, {})

        self.clips = self.get_json(os.path.join(directory, "images.json"))
        self.project_data["clips.json"] = self.clips

        self.images = self.get_json(os.path.join(directory, "clips.json"))
        self.project_data["images.json"] = self.images

    def save(self):
        """
        Handles save command
        """
        if self.current_directory in Path(self.project_directory).parents:
            remove_directory(self.project_directory)
            self.save_as()
        else:
            self.write_json(self.clips, self.project_data["clips.json"])
            self.write_json(self.images, self.project_data["images.json"])

        return self

    def save_as(self):
        """
        Handles save as command
        """
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setFileMode(QFileDialog.DirectoryOnly)

        if dialog.exec_() == QFileDialog.AcceptSave:
            file = dialog.selectedFiles()[0]
            if Path(self.project_directory).parent == self.current_directory:
                copyfile(self.project_directory, file)
                remove_directory(self.project_directory)
            else:
                self.save()
                copyfile(self.project_directory, file)
            return Project(file, self.current_directory, True)

    def set_directory(self, path):
        """
        Sets self.project_directory to path
        """
        self.project_directory = path
        return path

    def get_directory(self):
        """
        Sets self.project_directory to path
        """
        return self.project_directory
