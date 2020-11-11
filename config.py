import pygame
from os import path

#Definindo Gerais:

GAME_DIR = path.dirname(__file__)
IMG_DIR = path.join(GAME_DIR, 'img')

TITLE= 'ONE BIT GAME'

#Configurando tamanho da tela:

WIDTH = 700
HEIGHT = 700

# Clock e controle de FPS

clock = pygame.time.Clock()
FPS = 60
dt = clock.tick(FPS)/1000

# Cores utilizadas

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BROWN = (106, 55, 5)
ORANGE = (255, 140, 0)
BLUE = (0, 0, 255)
GRAY = (192, 192, 192)

#Configurações gerais navio :

BOAT_WIDTH = 120
BOAT_HEIGHT = 120
PLAYER_SPEED = 280

    #Lista de Imagens navio:

PLAYER_IMG = 'Navio.png'
PLAYER_WALK_LEFT = ['D0 (3).png']
PLAYER_WALK_RIGHT = ['Navio.png']
PLAYER_WALK_UP = ['D0 (1).png']
PLAYER_WALK_DOWN = ['D0 (2).png']

PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

