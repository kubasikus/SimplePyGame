from Game_Manager import Game_Manager

if __name__ == '__main__':
    manager = Game_Manager()
    manager.create_new_country('USA', 5, 0)
    manager.create_new_country('China', 6, 0)
    manager.remove_country('USA')
    manager.list_all_countries()
