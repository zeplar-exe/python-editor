import os

def remove_directory(dir_):
    """
    Recursively removes a directory and files/directories inside of it
    """
    for file in os.listdir(dir_):
        full_name = os.path.join(dir_, file)
        if os.path.isdir(full_name):
            remove_directory(full_name)
            os.removedirs(full_name)
        else:
            os.remove(full_name)

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

def request_save(project):
    if project.project_data["clips"] != project.clips:
        return True
        
    if project.project_data["images"] != project.images:
        return True

    return False
