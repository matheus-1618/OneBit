""" 
ONEBIT GAME!

Jogo criado por: Leticia Coêlho Barbosa e Matheus Silva
na disciplina de Design de Software

Professor orientador: Luciano Soares,
1A- ENG
INSPER 2020.2

Créditos no arquivo README.md
"""

# ===== Inicialização =====
# ----- Importa e inicia pacotes

import pygame
import sys
from os import path
from config import *
from sprites import *

pygame.init()

#----- Criando classe Jogo responsável por atualizações e tratamento de eventos

class Jogo (pygame.sprite.Sprite):
    
    def __init__(self):

        #Inicializando biblioteca

        pyagame.init() 
        
        #Inicializando Tela:
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def run(self):

    # Loop do jogo 

        self.playing = True
        
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def events(self):

        #Guardando eventos principais ocorridos durante o jogo:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:       
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

    def quit(self):

        #Fechar o jogo

        pygame.quit()
        sys.exit()

#Criando dicionario assets:

assets={}

#Carregando imagens:
map_init = pygame.image.load('./assets/Fundoinicial.jpg').convert()  
boat_img = pygame.image.load('./assets/navio_inicial.png').convert_alpha()
cannonball_img = pygame.image.load('./assets/balacanhao_1.png').convert_alpha()

#Redimensionando:

assets['map_init'] = pygame.transform.scale(map_init,(WIDTH,HEIGHT))
assets['boat_img'] = pygame.transform.scale(boat_img, (BOAT_WIDTH, BOAT_HEIGHT))
assets['cannonball_img'] = pygame.transform.scale(cannonball_img, (CANNONBALL_WIDTH,CANNONBALL_HEIGHT))

# ----- Inicia estruturas de dados (Classes)

class Boat(pygame.sprite.Sprite):
    def __init__(self, assets,groups):
        
        self.jogo = jogo
        self.groups = jogo.all_sprites  
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.image = assets['boat_img']
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT/2
        self.speedx=0
        self.speedy=0
        self.assets=assets

    def shoot (self):
        pass

    def update(self):
        pass

class Cannonball(pygame.sprite.Sprite):
    def __init__(self, assets, groups):
        
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)   

        self.image = assets['cannonball_img']
        self.rect = self.image.get_rect()

    def update(self):
        pass

game = True
#Ajuste de velocidade e tempo
clock=pygame.time.Clock()
FPS=30
#Criando as balas de canhões:

all_sprites = pygame.sprite.Group()
all_cannonballs = pygame.sprite.Group()

groups = {}
groups['all_sprites']=all_sprites
groups['all_cannonballs']=all_cannonballs

#Criando o navio controlado
boat= Boat(assets,groups)
all_sprites.add(boat)

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    #Eventos cruciais
    for event in pygame.event.get():
        #Ações tomadas pelo jogador:
        if event.type == pygame.QUIT:
            game = False
        #Teclas sendo apertadas
        if event.type == pygame.KEYDOWN:
            #Cada tecla tem seu direcionamento
            if event.key == pygame.K_LEFT:
                boat.speedx -=10
            if event.key == pygame.K_RIGHT:
                boat.speedx +=10
            if event.key == pygame.K_UP:
                boat.speedy +=10
            if event.key == pygame.K_DOWN:
                boat.speedy -=10
            if event.key == pygame.K_SPACE:
                boat.shoot()
        #Teclas sendo soltas
        if event.type == pygame.KEYUP:
            #Cada tecla tem seu direcionamento:
            if event.key == pygame.K_LEFT:
                boat.speedx +=10
            if event.key == pygame.K_RIGHT:
                boat.speedx -=10
            if event.key == pygame.K_UP:
                boat.speedy -=10
            if event.key == pygame.K_DOWN:
                boat.speedy +=10

    #Atualizando os estados do game
    all_sprites.update()

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados