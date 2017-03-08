import json
from time import strftime, localtime

class DataManager:

    @staticmethod
    def get_data(path):
        """Gets statistics from file"""
        try:
            with open(path) as ff:
                restored = json.load(ff)
                return restored
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # print("That's yours first time! Welcome!")
            return {}

    @staticmethod
    def save_data(data, path):
        """Saves statistics to file"""
        with open(path, 'w') as ff:
            json.dump(data, ff)

    @staticmethod
    def get_time():
        return strftime('%H:%M', localtime())
