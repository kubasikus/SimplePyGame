"""Game manager stores information about game state, objects and provides
needed functions"""

from Country_Class import Country_Class
import logging

# TODO: implement better logging with timestamps and complete DEBUG a INFO logs
logging.basicConfig(filename='logger.log', level=logging.INFO)
Logger = logging.getLogger()

# game state constants
SETUP = 'setup'
SETUP_ID = 0
TURN = 'turn'
TURN_ID = 1
EVAL = 'eval'
EVAL_ID = 2
RESET = 'reset'
RESET_ID = 3


class Game_Manager:
    __instance = None
    CountryObjectDict = {}
    ActivePlayer = None
    GameStateList = [SETUP, TURN, EVAL, RESET]
    GameState = 'setup'
    LastCommand = None
    # list of player accessible functions
    GameBaseDict = {'help': 'help', 'g_advance': 'game_advance_state', 'g_state': 'print_game_state',
                    'rep': 'repeat_command'}
    GameSetupDict = {**GameBaseDict,
                     **{'c_new': 'country_add', 'c_info': 'country_list_info', 'g_setup': 'default_game_setup'}}
    GameTurnDict = {**GameBaseDict,
                    **{'attack': 'attack_country', 'c_upgrade': 'upgrade_country', 'c_info': 'country_list_info'}}
    GameEvalDict = GameBaseDict
    GameResetDict = GameBaseDict
    CombinedCommandDict = {GameStateList[SETUP_ID]: GameSetupDict, GameStateList[TURN_ID]: GameTurnDict,
                           GameStateList[EVAL_ID]: GameEvalDict, GameStateList[RESET_ID]: GameResetDict}
    ActiveCommandDict = {}

    def __init__(self):
        """ Virtually private constructor. """
        if Game_Manager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Game_Manager.__instance = self
        self.game_change_state('setup')

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Game_Manager.__instance is None:
            Game_Manager()
        return Game_Manager.__instance

    # Country modifications
    def player_set_active(self, country_name=None):
        if country_name is None:
            print('Select your country from the list:', self.list_all_countries())
            country_name = input('Country name:')
        if country_name in self.CountryObjectDict:
            self.ActivePlayer = country_name
        else:
            print('Country does not exist.')

    def country_add(self, country_name=None, lives=0, score=0):
        """This function is needed to instantiate and add a new country to
        dict"""
        if country_name is None:
            country_name = input('Name of the new country:')
        if lives == 0:
            lives = int(input('number of lives:'))

        if country_name not in self.CountryObjectDict:
            self.CountryObjectDict[country_name] = Country_Class(country_name, lives, score)
            Logger.info('new country {} with {} lives added.'.format(country_name, lives))
        else:
            Exception('Country with this name already exists')

    def country_remove(self, country_name):
        """This function removes country with 'name' from the game memory"""
        if country_name in self.CountryObjectDict:
            del self.CountryObjectDict[country_name]
            Logger.info('Country {} removed.'.format(country_name))

    def country_get(self, country_name: str) -> Country_Class():
        try:
            if country_name in self.CountryObjectDict:
                return self.CountryObjectDict[country_name]
        except KeyError:
            return None

    def country_list_info(self, country_name=None):
        if country_name is None:
            country_name = input('Country to get info about:')
        if country_name in self.CountryObjectDict:
            print(self.CountryObjectDict[country_name].__str__())

    # Game state
    def game_change_state(self, state):
        """Change game state and make new commands available"""
        if state in self.GameStateList:
            self.GameState = state
            self.ActiveCommandDict = self.CombinedCommandDict[self.GameState]

    def game_advance_state(self):
        """Rotates the game states

        """
        # first change from setup to turn
        if self.GameState == SETUP:
            if self.ActivePlayer is not None:
                self.game_change_state(self.GameStateList[TURN_ID])
            else:
                print('Could not advance game state, the game has not been set up.')
        # change from turn to eval
        if self.GameState == TURN:
            rem_country_list = [country_obj for country_obj in self.CountryObjectDict.values() if
                                country_obj.get_actions() > 0]
            if len(rem_country_list) > 0:
                print('Not all actions of {} were taken, switching...'.format(rem_country_list[0].Country_name))
                self.player_set_active(rem_country_list[0].Country_name)
            elif len(rem_country_list) == 0:
                self.game_change_state(self.GameStateList[EVAL_ID])
        # change from eval to turn
        if self.GameState == EVAL:
            # Remove killed countries
            dead_countries = [country_obj for country_obj in self.CountryObjectDict.values() if
                              country_obj.get_lives() <= 0]
            if len(dead_countries) > 0:
                for country in dead_countries:
                    print('Country ', country.Country_name, ' was defeated')
                    self.country_remove(country.Country_name)

            rem_country_list = list(self.CountryObjectDict.values())
            economy_win_country_list = [Country for Country in list(self.CountryObjectDict.values()) if
                                        Country.get_score() >= Country_Class.ECONOMY_WIN]
            # check win state - others dead or economy win
            if len(rem_country_list) == 1:
                last_country = rem_country_list[0]
                print('Country {} has won!'.format(last_country))
                self.game_change_state(self.GameStateList[RESET_ID])
            elif len(rem_country_list) == 0:
                print('Everyone died, there is not winner...')
                self.game_change_state(self.GameStateList[RESET_ID])
            elif len(economy_win_country_list) > 0:
                print('A country has won economically')  # TODO: goto reset and also display which country/ies won
                self.game_change_state(self.GameStateList[RESET_ID])
            else:
                for country in rem_country_list:
                    country.set_actions(Country_Class.MAX_ACTIONS)
                self.game_change_state(self.GameStateList[TURN_ID])

        if self.GameState == RESET:
            rem_country_list = list(self.CountryObjectDict.values())
            # remove countries
            if len(rem_country_list) > 0:
                for country in rem_country_list:
                    self.country_remove(country.Country_name)
            # reset active player
            self.ActivePlayer = None
            self.game_change_state(self.GameStateList[SETUP_ID])

    def list_all_countries(self):
        print(self.CountryObjectDict.__repr__(), '\n')

    def print_game_state(self):
        print('Current game state: ', self.GameState)
        print('Countries in game: \n')
        self.list_all_countries()
        print('Active country: ', self.ActivePlayer)

    # Country Actions
    # TODO: Implement defense operations,
    # TODO: Implement spy ops
    # TODO: Move these into Country_Class
    def upgrade_country(self, name=None):
        """Add victory points and remove action point"""

        # Need a country to act upon
        if name is None:
            name = self.ActivePlayer
        country = self.country_get(name)
        action_points = country.get_actions()
        # only allow if enough action points
        if action_points > 0:
            country.set_score(country.get_score() + 1)
            country.set_actions(action_points - 1)
            Logger.info('Country level of {} was changed to: {}'.format(name, country.get_score))
        else:
            print('Not enough action points.')

    def attack_country(self, name=None):
        """Choose which country to attack"""
        if name is None:
            while True:
                name = input('Which country to attack: ')
                if self.country_get(name) is not None and name != self.ActivePlayer:
                    break
                else:
                    print('That country does not exist')
        att_country = self.country_get(self.ActivePlayer)
        def_country = self.country_get(name)
        if att_country.get_actions() > 0:
            att_country.set_actions(att_country.get_actions() - 1)
            def_country.set_lives(def_country.get_lives() - 1)
        else:
            print('Not enough action points.')

    # CLI parser
    def help(self):
        print('available commands: {}'.format(list(self.ActiveCommandDict.keys())))

    def repeat_command(self):
        # TODO: Fix repeated rep calling
        if self.LastCommand != 'rep':
            getattr(self, self.ActiveCommandDict[self.LastCommand])()
        else:
            print('cannot repeat rep command')

    def cli_parser(self, command=None):
        # TODO: create numbered input options for faster gameplay
        if command is None:
            command = input('type your command:')
        if command in self.ActiveCommandDict:
            Logger.info('executing {} function'.format(self.ActiveCommandDict[command]))
            getattr(self, self.ActiveCommandDict[command])()
        else:
            print('unknown command.')
        self.LastCommand = command

    # Game Setups
    def default_game_setup(self):
        if len(self.CountryObjectDict) != 0:
            self.CountryObjectDict = {}
            self.ActivePlayer = None
        self.country_add('USA', 1, 0)
        self.country_add('China', 1, 0)
        self.player_set_active('USA')
