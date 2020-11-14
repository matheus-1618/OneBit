import pygame
from os import path

#Definindo Gerais:

#Diretórios acessados
GAME_DIR = path.dirname(__file__)
IMG_DIR = path.join(GAME_DIR, 'img')
FONT_DIR = path.join(GAME_DIR, 'assets', 'fontes')
MUSIC_DIR = path.join(GAME_DIR, 'assets', 'sounds', 'musica')

TITLE= 'ONE BIT GAME'

#Configurando tamanho da tela:

WIDTH = 700
HEIGHT = 700

TILESIZE = 32  

# Clock e controle de FPS

clock = pygame.time.Clock()
FPS = 60
dt = clock.tick(FPS)/1000

# Cores utilizadas

WHITE = (255, 255, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTRED = (155, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
BLUE = (0, 0, 255)
GRAY = (192, 192, 192)


#Configurações gerais navio :

BOAT_WIDTH = 120
BOAT_HEIGHT = 120
BOAT_SPEED = 280
BOAT_KICKBACK=-50

#Intervalo entre um tiro e outro:

dt_shot= 300

#Lista de Imagens navio:

BOAT_IMG = 'Navio.png'
BOAT_WALK_LEFT = ['D0 (3).png']
BOAT_WALK_RIGHT = ['Navio.png']
BOAT_WALK_UP = ['D0 (1).png']
BOAT_WALK_DOWN = ['D0 (2).png']
BOAT_HIT_RECT = pygame.Rect(0, 0, 35, 35)

#Configurações balas de canhão
CANNONBALL_IMG = 'bullet.png'
CANNONBALL_SPEED= 300
CANNONBALL_PROPG=3
