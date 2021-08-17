import json
import csv


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


class CSV:
    """
        Class holding basic CSV methods
    """

    @staticmethod
    def write_csv(file, data):
        """
        Writes 'data' to the given csv file
        """
        with open(file, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(data)
            return data

    @staticmethod
    def get_csv(file):
        """
        Returns csv data
        """

        data = []
        with open(file, "r") as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in reader:  # each row is a list
                data.append(row)

            return data
