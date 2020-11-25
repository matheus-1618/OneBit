import pygame
from os import path
vec = pygame.math.Vector2

#------Definindo Gerais-----#

#Diretórios acessados
GAME_DIR = path.dirname(__file__)
IMG_DIR = path.join(GAME_DIR, 'img')
FONT_DIR = path.join(GAME_DIR, 'assets', 'fontes')
MUSIC_DIR = path.join(GAME_DIR, 'assets', 'sounds', 'musica')
EFFECTS_DIR = path.join(GAME_DIR,'assets','sounds','effects')

TITLE= "ONE BIT GAME"

#Configurando tamanho da tela:

WIDTH = 1024
HEIGHT = 768

TILESIZE = 64 

#Clock e controle de FPS

clock = pygame.time.Clock()
FPS = 60
dt = clock.tick(FPS)/1000

#Cores utilizadas

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

#Configuração itens
RUM_SPREAD=15
CARNE_LIFE=10
CARNE_XP=10
TESOURO_XP=50

RUM_IMG='bottle.png'
MEAT_IMG='Carne.png'
TESOURO_IMG= 'chest_SE (1).png'


#Imagem inicial
INIT_IMG=['frame-1.gif','frame-2.gif','frame-3.gif','frame-4.gif','frame-5.gif','frame-6.gif']

#Imagem instruções
INST_IMG=['inst-1.png','inst-2.png']

#Imagem game over
OVER_IMG=['fram-1.gif','fram-2.gif','fram-3.gif','fram-4.gif','fram-5.gif','fram-6.gif','fram-7.gif','fram-8.gif','fram-9.gif','fram-10.gif','fram-11.gif','fram-12.gif','fram-13.gif','fram-14.gif']

#Imagem de transição
TRAN_IMG=['frae-1.gif','frae-2.gif','frae-3.gif','frae-4.gif','frae-5.gif','frae-6.gif','frae-7.gif','frae-8.gif','frae-9.gif','frae-10.gif','frae-11.gif','frae-12.gif','frae-13.gif','frae-14.gif','frae-15.gif','frae-15.gif','frae-16.gif','frae-17.gif','frae-18.gif','frae-19.gif','frae-20.gif','frae-21.gif','frae-22.gif','frae-23.gif','frae-24.gif','frae-25.gif','frae-26.gif','frae-27.gif','frae-28.gif','frae-29.gif','frae-30.gif','frae-31.gif','frae-32.gif','frae-33.gif','frae-34.gif','frae-35.gif','frae-36.gif','frae-37.gif','frae-38.gif','frae-39.gif','frae-40.gif']

#Imagem de vitória
WIN_IMG=['mar-1.gif','mar-2.gif','mar-3.gif','mar-4.gif','mar-5.gif','mar-6.gif','mar-7.gif','mar-8.gif','mar-9.gif','mar-10.gif','mar-11.gif','mar-12.gif','mar-13.gif','mar-14.gif','mar-15.gif']

#Configurações gerais navio :

BOAT_WIDTH = 120
BOAT_HEIGHT = 120
BOAT_SPEED = 280
BOAT_KICKBACK=-50
BOAT_HEALTH = 250
BOAT_XP=0.1
BOAT_XP_MAX=350

#Lista de Imagens navio:
BOAT_IMG = 'Navio.png'
BOAT_WALK_LEFT = 'D0 (3).png'
BOAT_WALK_RIGHT = 'Navio.png'
BOAT_WALK_UP = 'D0 (1).png'
BOAT_WALK_DOWN = 'D0 (2).png'
BOAT_HIT_RECT = pygame.Rect(0, 0, 35, 35)

#Configurações balas de canhão
CANNONBALL_IMG = 'bullet.png'
CANNONBALL_SPEED = 500
CANNONBALL_LIFETIME = 1000
CANNONBALL_RATE = 700
KICKBACK = 50
CANNONBALL_PROPG = 5
CANNONBALL_DAMAGE = 10
CANNONBALL_DAMAGE2=10
CANNONBALL_LESS_SPEED=10

#Intervalo entre um tiro e outro:

dt_shot= 700

#Configurações inimigas
CRACKEN_IMG = 'enemie.png'
CRACKEN_SPEEDS = [150, 100, 75, 125]
CRACKEN_HIT_RECT = pygame.Rect(0, 0, 30, 30)
CRACKEN_HEALTH = 200
CRACKEN_DAMAGE = 15
CRACKEN_KNOCKBACK = 20
CRACKEN_XP=200
AVOID_RADIUS = 50

MOB_KNOCKBACK= 20   #Recuo

#Configurações inimigas pirata
PIRATA_DIREITA= 'pirata_direita.png'
PIRATA_ESQUERDA= 'pirata_esquerda.png'
PIRATA_CIMA= 'pirata_cima.png'
PIRATA_BAIXO = 'pirata_baixo.png'
PIRATA_HEALTH = 20
PIRATA_DAMAGE=5
PIRATA_WIDTH= 130
PIRATA_HEIGHT = 130
PIRATA_HIT_RECT = pygame.Rect(0,0,0.8*PIRATA_WIDTH,0.8*PIRATA_HEIGHT)
PIRATA_SPEED =[175, 150, 130, 200]
PIRATA_XP=30