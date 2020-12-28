import os
from pathlib import Path
from json_lib import JSON
from exlib import remove_directory

class Project(JSON):
    """
    Project class, mainly for directory management
    """

    def __init__(self, directory, app_directory, opening = None):
        self.current_directory = app_directory
        self.__project_directory = directory
        self.project_data = {
            "clips": [],
            "images": []
        }

        if opening is None:
            os.mkdir(directory)
            open(os.path.join(directory, "clips.json"), "x").close()

        with open(os.path.join(directory, "clips.json")) as f_data:
            self.project_data["clips"] = f_data

        with open(os.path.join(directory, "images.json")) as f_data:
            self.project_data["images"] = f_data

        os.mkdir(os.path.join(self.__project_directory, "clips"))
        os.mkdir(os.path.join(self.__project_directory, "images"))

    def save(self):
        """
        Handles save command
        """
        if Path(self.__project_directory).parent == self.current_directory:
            remove_directory(self.__project_directory)
        else:
            pass

    def save_as(self, directory):
        """
        Handles save as command
        """
        if Path(self.__project_directory).parent == self.current_directory:
            remove_directory(self.__project_directory)
        else:
            pass

    def remove(self):
        """
        Removes project directory
        """
        remove_directory(self.__project_directory)

    def set_directory(self, path):
        """
        Sets self.project_directory to path
        """
        self.__project_directory = path
        return path

    def get_directory(self):
        """
        Sets self.project_directory to path
        """
        return self.__project_directory
