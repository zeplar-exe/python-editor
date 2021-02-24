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
            json.dump(data, json_file, indent=4, sort_keys=True)
            return data

    @staticmethod
    def get_json(file):
        """
        Returns json data
        """

        with open(file, "r") as json_file:
            try:
                contents = json_file.read()
                data = json.loads(contents)
            except json.decoder.JSONDecodeError:
                return JSON.write_json(file, {})
            else:
                return data
