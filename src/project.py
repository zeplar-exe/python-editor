import os
from pathlib import Path
from shutil import copytree
from PyQt5.QtWidgets import QFileDialog
from json_lib import JSON
from exlib import remove_directory


class Project(JSON):
    """
    Project class, mainly for directory management
    """

    def __init__(self, directory, app_directory, temporary=False, opening=None):
        self.current_directory = app_directory
        self.project_directory = directory
        self.saved = False
        self.current_frame = 0
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
            new = self.save_as()
            return new
        else:
            self.write_json(os.path.join(self.project_directory, "images.json"), self.project_data["clips.json"])
            self.write_json(os.path.join(self.project_directory, "clips.json"), self.project_data["images.json"])

            j_data = self.get_json("user_presets.json")

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
                remove_directory(self.project_directory)
            else:
                self.save()
                os.removedirs(file)
                copytree(self.project_directory, file)
            return Project(file, self.current_directory, opening=True)

    def get_directory(self):
        """
        Sets self.project_directory to path
        """
        return self.project_directory
