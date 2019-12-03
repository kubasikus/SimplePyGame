"""Game manager stores information about game state, objects and provides
needed functions"""

from Country_Class import Country_Class
import logging

logging.basicConfig(filename='logger.log', level=logging.INFO)
Logger = logging.getLogger()


class Game_Manager:
    __instance = None
    countryObjectDict = {}
    currentPlayer = None
    # list of player accessible functions
    function_dict = {'help': 'help', 'new': 'add_country', 'upgrade': 'upgrade',
                     'player': 'set_player', 'info': 'list_country_info'}

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Game_Manager.__instance == None:
            Game_Manager()
        return Game_Manager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Game_Manager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Game_Manager.__instance = self

    # Country modifications
    def set_player(self, name=None):
        if name is None:
            print('Select your country from the list:',
                  self.list_all_countries())
            name = input('Country name:')
        if name in self.countryObjectDict:
            self.currentPlayer = name
        else:
            print('Country does not exist.')

    def add_country(self, name=None, lives=0, score=0):
        """This function is needed to instantiate and add a new country to
        dict"""
        if name is None:
            name = input('Name of the new country:')
        if lives == 0:
            lives = int(input('number of lives:'))

        if name not in self.countryObjectDict:
            self.countryObjectDict[name] = Country_Class(name, lives, score)
            Logger.info(
                'new country {} with {} lives added.'.format(name, lives))
        else:
            Exception('Country with this name already exists')

    def remove_country(self, name):
        """This function removes country with 'name' from the game memory"""
        if name in self.countryObjectDict:
            del self.countryObjectDict[name]
            Logger.info('Country {} removed.'.format(name))
        # TODO: remove country from active country as well

    def get_country(self, name: str) -> Country_Class():
        if name in self.countryObjectDict:
            return self.countryObjectDict[name]

    def list_all_countries(self):
        print(self.countryObjectDict.__repr__())

    def list_country_info(self, name=None):
        if name is None:
            name = input('Country to get info about:')
        if name in self.countryObjectDict:
            print(self.countryObjectDict.__str__())

    # CLI parser
    def help(self):
        print('available commands: {}'.format(list(self.function_dict.keys())))

    def upgrade(self, name=None):
        """Add victory points and TODO: remove action point"""
        if name is None:
            name = self.currentPlayer
        country = self.get_country(name)
        country.set_score(country.get_score() + 1)
        Logger.info('Country level of {} was changed to: {}'.format(name,
                                                                    country.get_score))

    def cli_parser(self):
        command = input('type your command:')
        if command in self.function_dict:
            Logger.info(
                'executing {} function'.format(self.function_dict[command]))
            getattr(self, self.function_dict[command])()
