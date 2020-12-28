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
        self.project_directory = directory
        self.saved = False
        self.project_data = {
            "clips": [],
            "images": []
        }

        if opening is None:
            os.mkdir(directory)
            open(os.path.join(directory, "clips.json"), "x").close()
            open(os.path.join(directory, "images.json"), "x").close()

        self.clips = os.path.join(directory, "clips.json")
        with open(self.clips) as f_data:
            self.project_data["clips"] = f_data

        self.images = open(os.path.join(directory, "images.json"))
        with open(self.images) as f_data:
            self.project_data["images"] = f_data

        os.mkdir(os.path.join(self.project_directory, "clips"))
        os.mkdir(os.path.join(self.project_directory, "images"))

    def save(self):
        """
        Handles save command
        """
        if Path(self.project_directory).parent == self.current_directory:
            remove_directory(self.project_directory)
            self.save_as()
        else:
            self.write_json(self.clips, self.project_data["clips"])
            self.write_json(self.images, self.project_data["images"])

    def save_as(self, directory = ""):
        """
        Handles save as command
        """
        if not directory:
            pass

        if Path(self.project_directory).parent == self.current_directory:
            remove_directory(self.project_directory)
        else:
            pass

    def release(self):
        """
        Removes project directory
        """
        remove_directory(self.project_directory)

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

    def __del__(self):
        self.clips.close()
        self.images.close()
