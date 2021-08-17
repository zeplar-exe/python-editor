import os
from PyQt5.QtWidgets import QMessageBox
from json_lib import JSON


def remove_directory(dir_):
    """
    Recursively removes a directory and files/directories inside of it
    """
    for file in os.listdir(dir_):
        full_name = os.path.join(dir_, file)
        if os.path.isdir(full_name):
            remove_directory(full_name)
        else:
            os.remove(full_name)

    if os.path.isdir(dir_):
        os.removedirs(dir_)
    else:
        os.remove(dir_)


def compare_dict_keys(dict_a, dict_b, yielder=None):
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


def get_keys(dictionary: dict):
    """
    Return a list of keys from a dictionary
    """
    ret = []
    for key in dictionary:
        ret.append(key)
    return ret


def request_save(project):
    """
    Checks if project has been modified
    """
    modified = False

    if project.project_data["imports.json"] != project.imports:
        modified = True

    if project.project_data["source.mp4"] != project.source_video:
        modified = True

    if get_keys(project.project_data) != os.listdir(project.get_directory()):
        modified = True

    if modified:
        if JSON.get_json("user_preferences.json")["warn_non_save"]:
            dialog = QMessageBox()
            dialog.setText("Project modifications have been found")
            dialog.setInformativeText("Are you sure you would like to discard unsaved changes?")
            dialog.setIcon(QMessageBox.Information)
            dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            return dialog.exec_(), dialog

    return 0, 0

def SafeRemoveDirectory(app_, dir_):
    app_.current_project.source_video.close()
    if "Preview" in app_.dock_widgets:
        app_.dock_widgets["Preview"].CloseMedia()
    remove_directory(dir_)
