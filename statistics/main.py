import re
import json
import sys
from collections import defaultdict


class DataManager:

    # a pattern to grab numbers
    pa_time = re.compile(r'\s([0-9.h]+)\s')

    @staticmethod
    def get_data(path):
        """Gets statistics from file"""
        try:
            with open(path) as ff:
                restored = defaultdict(int, json.load(ff))
                return restored
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # print("That's yours first time! Welcome!")
            return defaultdict(int)

    @staticmethod
    def save_data(path, data):
        """Saves statistics to file"""
        with open(path, 'w') as ff:
            json.dump(data, ff)

    @staticmethod
    def get_time(time_format):
        """Converts 2h, .5h, 2.5h format to minutes"""
        time_format = ' %s ' % time_format
        try:
            found_time = SportData.pa_time.findall(time_format)[0]
            if found_time.endswith('h'):
                found_time = SportData.hours_to_minutes(found_time[:-1])
        except IndexError:
            # nothing found_time
            print("Whoops couldn't found any time in " + time_format)
            return 0
        return int(found_time)  # minutes

    @staticmethod
    def hours_to_minutes(hours):
        if hours.find('.') == -1:
            # time don't include minutes, minutes = 0
            minutes = 0
            pass
        else:
            if hours.startswith('.'):
                # it starts with dot, so hours = 0
                hours = '0%s' % hours
            hours, minutes = (num for num in hours.split('.'))
        # convert minutes to float
        minutes = float('0.%s' % minutes)
        return int(int(hours) * 60 + minutes * 60)


class SportTypes:
    # used for identifying sport
    sports_types = defaultdict(list, {
        'bieganie': [' bieg', ' sprint'],
        'brzuszki': [' brzusz', ' brzuch', ' brzó'],
        'pompki': [' pomp', ' odpychałem własne ciało od równi pochyłej']})

    def __init__(self, sports_types=None):
        if sports_types:
            print('podmiana')
            self.sports_types = sports_types
        print('elo')


    def replace(self, sports):
        self.sports_types = defaultdict(list, sports)


    def add_sport_type(self, new_patterns, new_pattern):
        """Adds Patterns or Pattern to system"""
        # TODO it needs to be grabed from file,
        # TODO add option to send sequence as new_pattern
        for exercise, patterns in SportData.sports_types.items():
            for pattern in patterns:
                if new_pattern.find(pattern) != -1 or pattern.find(new_pattern) != -1:
                    print('Sorry but %s patters collide!' % new_pattern)
                    print('%s => %s' % (exercise, pattern))
                    raise Exception('Patterns collide')

        self.sports_types[new_patterns].append(' ' + new_pattern)

    @classmethod
    def from_file(cls, path):
        return cls(DataManager.get_data(path))


class SportData(DataManager):

    def __init__(self, path, sports_types=None):
        self.path = path
        self.current_data = self.get_data(path)
        self.new_data = dict()
        self.SportTypes = SportTypes(sports_types)

    def new_sport_data(self, user_input):
        """Adds new sports statistic with loaded one"""
        # replace separated 'i' with ','
        user_input =  user_input.replace(' i ', ' , ')
        # make user input lowercase
        user_input = user_input.lower()

        flat_input = [item for item in user_input.split(',')]
        found_sports = defaultdict(int)

        for one_sport in flat_input:
            # adds white space to match with patters that are at beggining
            one_sport = ' %s ' % one_sport
            # grab spent time
            time_spend = self.get_time(one_sport)
            for exercise, patterns in self.SportTypes.sports_types.items():
                for pattern in patterns:
                    if one_sport.find(pattern) != -1:
                        found_sports[exercise] = time_spend
        # show it
        for sport, val in found_sports.items():
            print('%s + %s' % (sport, val), end='')
            if val >= 60:
                print('. TY KOZAKU!!!')
            elif val >= 30:
                print('. Brawo!')
            else:
                print()
        # combine this with present date
        self.mix_data(found_sports)

    def mix_data(self, new_dict):
        """Adds new data with existing one"""
        for new, val in new_dict.items():
            self.current_data[new] += val

    def save_data(self):
        super(SportData, self).save_data(self.path, self.current_data)



    @classmethod
    def from_file(cls, database_path, patterns_path):
        return cls(database_path, cls.get_data(database_path, patterns_path))

if __name__ == "__main__":
    using_args = False
    if len(sys.argv) > 1:
        using_args = True
        # untested
        for index, word in enumerate(sys.argv[1:]):
            s += word
            if index < len(sys.argv) - 1:
                s += ','
            s += ''
        print(s)
    else:
        # s = '10 pompek, 15 brzuszków, 10 min biegania, 1.7h pompki, 1h brzuszki, .2h bieg'
        # Manager = SportData('baza.txt')
        # Manager.new_sport_data(s)
        # Manager.save_data()
        # Manager.add_pattern('spacer', 'spa')
        # Manager.add_pattern('spacer', 'sp')
        # print(Manager.sports)

        while True:
            # biegałem 20 minut i przez 1.5h robiłem brzuszki
            # if not using_args:
            #     s = input("Co dzisiaj robiłeś?: ")
            # if s in 'exit q ex'.split():
            #     quit()
            s = 'Biegałem 10'
            Manager = SportData('baza.txt')
            Manager.new_sport_data(s)
            Manager.save_data()
            quit()
            if using_args:
                quit()
