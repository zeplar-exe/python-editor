import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QEvent

def compare_dict_keys(dict_a, dict_b, yielder = None):
    """
    Compares the keys of two dictionaries, checking if they both have the same keys.
    """
    for key in dict_a:
        if dict_b.get(key) is None:
            if (yielder is not None) and callable(yielder):
                yielder(key, dict_a[key], True)
            else:
                return False

    for key in dict_b:
        if dict_a.get(key) is None:
            if (yielder is not None) and callable(yielder):
                yielder(key, dict_a.get(key, None), False)
            else:
                return False

    return True

class EditorApplication(QWidget):
    """
    Main class for pyqt application
    """
    def __init__(self):
        """
        Class Initiator
        """
        app = QApplication(sys.argv)
        super().__init__()

        self.size_x = 0
        self.size_y = 0

        self.screen = app.primaryScreen()
        self.screen_size = self.screen.size()

        self.setWindowTitle("PyQt Editor")
        self.init_ui()
        self.load_json_preferences("user_preferences.json")

        self.user_preferences_template["X"] = self.size_x
        self.user_preferences_template["Y"] = self.size_y

        self.show()
        sys.exit(app.exec_())

    def init_ui(self):
        """
        Initiates window UI specifics
        """
        self.size_x = (self.screen_size.width()/5)*4
        self.size_y = (self.screen_size.height()/4)*3

        self.setGeometry(
            int(self.position_x),
            int(self.position_y),
            int(self.size_x),
            int(self.size_y)
        )

    def changeEvent(self, event):
        """
        Handles event queue
        """
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMaximized:
                existing_data, _ = self.get_json("user_preferences.json")
                existing_data["maximized"] = True
                self.write_json("user_preferences.json", existing_data)
            else:
                existing_data, _ = self.get_json("user_preferences.json")
                existing_data["maximized"] = False
                self.write_json("user_preferences.json", existing_data)

    position_x = 0
    position_y = 0

    def get_json(self, file):
        """
        Returns json data
        """

        with open(file, "r") as json_file:
            contents = json_file.read()
            data = json.loads(contents)
            return data, contents

    def write_json(self, file, data):
        """
        Writes 'data' to the given json 'file'
        """
        with open(file, "w") as json_file:
            json.dump(data, json_file)

    def load_json_preferences(self, file):
        """
        Reads preferences json file and loads neccessary properties and functions.
        If json data does not exist, it is created.
        """

        data, _ = self.get_json(file)
        if (not data.get("JSONLoaded", False)) or (not compare_dict_keys(self.user_preferences_template, data)):
            def update(key, value, addition):
                """
                Updates JSON data based on 'value'
                """
                if data.get("JSONLoaded", False):
                    value = data.get(key, value)

                if addition is True:
                    data.update({key: value})
                else:
                    data.pop(key)

            compare_dict_keys(self.user_preferences_template, data.copy(), update)

            self.write_json(file, data)

        if data.get("maximized"):
            self.showMaximized()

        if data.get("fullscreen"):
            self.showFullScreen()

    user_preferences_template = {
        "JSONLoaded": True,
        "maximized": False,
        "fullscreen": False,

        "WindowSize": {
            "X": 0,
            "Y": 0
        }
    }

if __name__ == "__main__":
    EditorApplication()
