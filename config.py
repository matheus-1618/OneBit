import pygame
from os import path
vec = pygame.math.Vector2

#Definindo Gerais:

#Diretórios acessados
GAME_DIR = path.dirname(__file__)
IMG_DIR = path.join(GAME_DIR, 'img')
FONT_DIR = path.join(GAME_DIR, 'assets', 'fontes')
MUSIC_DIR = path.join(GAME_DIR, 'assets', 'sounds', 'musica')
EFFECTS_DIR = path.join(GAME_DIR,'assets','sounds','effects')

TITLE= 'ONE BIT GAME'

#Configurando tamanho da tela:

WIDTH = 1024
HEIGHT = 768

TILESIZE = 64 

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
BOAT_HEALTH = 100

#Lista de Imagens navio:
BOAT_IMG = 'Navio.png'
BOAT_WALK_LEFT = 'D0 (3).png'
BOAT_WALK_RIGHT = 'Navio.png'
BOAT_WALK_UP = 'D0 (1).png'
BOAT_WALK_DOWN = 'D0 (2).png'
BOAT_HIT_RECT = pygame.Rect(0, 0, 35, 35)
BOAT_HIT_RECT = pygame.Rect(0, 0, 35, 35)

#Configurações balas de canhão
CANNONBALL_IMG = 'bullet.png'
CANNONBALL_SPEED = 500
CANNONBALL_LIFETIME = 1000
CANNONBALL_RATE = 700
KICKBACK = 50
CANNONBALL_PROPG = 5
CANNONBALL_DAMAGE = 10

#Intervalo entre um tiro e outro:

dt_shot= 300
#Configurações inimigas
CRACKEN_IMG = 'enemie.png'
CRACKEN_SPEEDS = [150, 100, 75, 125]
CRACKEN_HIT_RECT = pygame.Rect(0, 0, 30, 30)
CRACKEN_HEALTH = 100
CRACKEN_DAMAGE = 10
CRACKEN_KNOCKBACK = 20
AVOID_RADIUS = 50

#Configurações inimigas pirata
PIRATA_DIREITA= 'pirata_direita.png'
PIRATA_ESQUERDA= 'pirata_esquerda.png'
PIRATA_CIMA= 'pirata_cima.png'
PIRATA_BAIXO = 'pirata_baixo.png'
PIRATA_HEALTH = 30
PIRATA_DAMAGE=10
PIRATA_WIDTH= 130
PIRATA_HEIGHT = 130
PIRATA_HIT_RECT = pygame.Rect(0,0,0.8*PIRATA_WIDTH,0.8*PIRATA_HEIGHT)
PIRATA_SPEED = 80