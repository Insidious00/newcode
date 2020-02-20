import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 800   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 700  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Game"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
NPC_IMAGE1 = "npc1.png"
NPC_IMAGE2 = "npc2.png"
PLAYER_IMG4 = ['Front.png', 'Front1.png','Front2.png']
PLAYER_IMG1 = ['Left.png', 'Left1.png','Left2.png']
PLAYER_IMG2 = ['Right.png', 'Right1.png','Right2.png']
PLAYER_IMG3 = ['Back.png', 'Back1.png','Back2.png']
LOGO_IMG = "logo_image.png"
dialogueBack = "background.jpg"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)

DIALOGUE1 = [("Wonderful Day isnt it!"),("Hello, have I seen you before"),("Let me guess... someone stole your sweetroll.")]
Mission_Init_1 = [("Hey, you look like an outsider. If you're looking for work, I've heard the blacksmith needs someone!")]
Mission_Dial_1 = ["How can I help you?"]
Mission_Ans_1 = [("Who are you?"), ("Nothing"), ("Where am I?")]


invPos = [[85,576],[193,576],[301,576],[409,576]]
