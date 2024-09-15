import math
from tools import get_screen_dimensions


screen_width, screen_height = get_screen_dimensions() # width and height are in pixels so they depend on screen resolution not actual 

# YOU CAN EDIT THESE:
SCREEN_WIDTH = screen_width*9//10
SCREEN_HEIGHT = screen_height*9//10

BG_COLOR=(0, 0, 0)
TEXT_COLOR=(255, 255, 255)
BALL_COLOR=(0, 255, 0)
PLAYER_PADDLE_COLOR=(255, 0, 0)
OP_PADDLE_COLOR=(0, 0, 255)

PORT = 7893


# DO NOT TOUCH THESE!!!
HOST_IP = "192.168.43.1" # it works for most devices never touch it if the game is working for you

BALL_RADIUS = 1/70                # will be multiplied by SCREEN_HEIGHT
BALL_SPEED = 1/100, 1/100         # will be multiplied by SCREEN_WIDTH, SCREEN_HEIGHT
MAX_BOUNCE_ANGLE = math.radians(80)

PLAYER_WIDTH = 1/6                # will be multiplied bySCREEN_WIDTH
PLAYER_HEIGHT = 1/30              # will be multiplied by SCREEN_HEIGHT
INITIAL_POS_LEFT_DOWN_CORNER = 1/2 - PLAYER_WIDTH/2 # effectively center the player paddle
PLAYER_SPEED = 1/100              # will be multiplied by SCREEN_WIDTH
PADDING = 1/80                   # will be multiplied by SCREEN_HEIGHT