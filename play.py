from game import Game
from config import SCREEN_WIDTH, SCREEN_HEIGHT

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)

try:
  game.start()
except KeyboardInterrupt: 
  game.exit()