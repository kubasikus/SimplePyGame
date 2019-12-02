class Country_Class():

    def __init__(self, country_name='No_Name', lives_num=3, score=0):
        self.Country_name = country_name
        self.Lives_num = lives_num
        self.Score = score

    def __repr__(self):
        return 'Country is called: {} \n' \
               'It has {} lives and score of {} \n'.format(self.Country_name,
                                                        self.Lives_num,
                                                        self.Score)
