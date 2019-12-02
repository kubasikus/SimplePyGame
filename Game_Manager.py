"""Game manager stores information about game state, objects and provides
needed functions"""

from Country_Class import Country_Class


class Game_Manager:
    __instance = None
    countryObjectDict = {}

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

    def create_new_country(self, name, lives, score):
        """This function is needed to instantiate and add a new country to
        dict"""
        if name not in self.countryObjectDict:
            self.countryObjectDict[name] = Country_Class(name, lives, score)
        else:
            Exception('Country with this name already exists')

    def remove_country(self, name):
        """This function removes country with 'name' from the game memory"""
        if name in self.countryObjectDict:
            del self.countryObjectDict[name]

    def list_all_countries(self):
        print(self.countryObjectDict.__repr__())
