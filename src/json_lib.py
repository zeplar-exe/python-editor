import json


class JSON:
    """
    Class holding basic JSON methods
    """

    @staticmethod
    def write_json(file, data):
        """
        Writes 'data' to the given json file
        """
        with open(file, "w") as json_file:
            json.dump(data, json_file)
            return data

    @staticmethod
    def get_json(file):
        """
        Returns json data
        """

        with open(file, "r") as json_file:
            contents = json_file.read()
            data = json.loads(contents)
            return data
