import json


class DataManager:

    class InvalidMap(Exception):
        pass

    @staticmethod
    def get(path):
        """Gets statistics from file"""

        with open(path) as ff:
            restored = json.load(ff)
            return restored

    @staticmethod
    def save(data, path):
        """Saves statistics to file"""
        with open(path, 'w') as ff:
            json.dump(data, ff)