


class Country_Class():
    MAX_ACTIONS = 1
    ECONOMY_WIN = 2

    def __init__(self, country_name='No_Name', lives_num=3, score=0):
        self.Country_name = country_name
        self.Lives_num = lives_num
        self.Score = score
        self.Actions = self.MAX_ACTIONS

    def __repr__(self):
        return '{} has {} lives, {} action points and score of {} \n'.format(self.Country_name, self.Lives_num,
                                                                             self.Actions, self.Score)

    def set_lives(self, value):
        self.Lives_num = value

    def get_lives(self):
        return self.Lives_num

    def set_score(self, value):
        self.Score = value

    def get_score(self):
        return self.Score

    def set_actions(self, value):
        if value > self.MAX_ACTIONS:
            value = self.MAX_ACTIONS
        self.Actions = value

    def get_actions(self):
        return self.Actions
