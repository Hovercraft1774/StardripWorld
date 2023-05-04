from scripts.game import *

def main():
    game = Game()
    game.start_Screen()
    game.new()
    game.gameLoop()
    game.end_Screen()
    exit()



if __name__ == '__main__':
    main()