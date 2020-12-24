import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget

user_preferences_template = {
    "JSONLoaded": True,
    "maximized": False,
    "fullscreen": False
}

def compare_dict_keys(dict_a, dict_b):
    """
    Compares the keys of two dictionaries, checking if they both have the same keys.
    """
    for key in dict_a:
        if not key in dict_b:
            return False

    return True

class EditorApplication:
    """
    Main class for pyqt
    """
    def __init__(self):
        """
        Class Initiator
        """
        app = QApplication(sys.argv)
        self.screen = app.primaryScreen()
        self.screen_size = self.screen.size()

        self.size_x = (self.screen_size.width()/4)*3
        self.size_y = (self.screen_size.height()/4)*3

        window = QWidget()
        window.setGeometry(
            int(self.position_x),
            int(self.position_y),
            int(self.size_x),
            int(self.size_y)
        )
        window.setWindowTitle("PyQt")
        self.load_json_preferences("user_preferences.json", window)

        window.show()
        sys.exit(app.exec_())

    def write_json(self, file, data):
        """
        Writes 'data' to the given json 'file'
        """
        with open(file, "w") as json_file:
            json.dump(data, json_file)

    def load_json_preferences(self, file, window):
        """
        Reads preferences json file and loads neccessary properties and functions.
        If json data does not exist, it is created.
        """
        with open(file, "r") as json_file:
            contents = json_file.read()
            data = json.loads(contents)

            if data.get("JSONLoaded",True) or not compare_dict_keys(data,user_preferences_template):
                return self.write_json(file, user_preferences_template)

            if data["maximized"]:
                window.showMaximized()

            if data["fullscreen"]:
                window.showFullScreen()

    position_x = 0
    position_y = 0

EditorApplication()
