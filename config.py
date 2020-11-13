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
BOAT_SPEED = 280

    #Lista de Imagens navio:

BOAT_IMG = 'Navio.png'
BOAT_WALK_LEFT = ['D0 (3).png']
BOAT_WALK_RIGHT = ['Navio.png']
BOAT_WALK_UP = ['D0 (1).png']
BOAT_WALK_DOWN = ['D0 (2).png']
BOAT_HIT_RECT = pg.Rect(0, 0, 35, 35)

    #Lista de imagem da bola de canhão
CANNONBALL_IMG = 'bullet.png'

