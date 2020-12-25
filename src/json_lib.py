import json

class JSON:
    """
    Class holding basic JSON methods
    """
    def write_json(self, file, data):
        """
        Writes 'data' to the given json file
        """
        with open(file, "w") as json_file:
            json.dump(data, json_file)
            return data

    def get_json(self, file):
        """
        Returns json data
        """

        with open(file, "r") as json_file:
            contents = json_file.read()
            data = json.loads(contents)
            return data, contents
