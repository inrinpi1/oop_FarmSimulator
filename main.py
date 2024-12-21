from game.game import Game

if __name__ == "__main__":
    game = Game()
    game.inventory.earn_money(1000)  # добавим стартовый капитал
    game.run()