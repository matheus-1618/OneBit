""" 
ONEBIT THE GAME!

Jogo criado por: Leticia Coêlho Barbosa e Matheus Silva
na disciplina de Design de Software

Professor orientador: Luciano Soares
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

    #Carregando imagens importantes
    def load_data(self):
        
        #especificando os caminhos de busca dos arquivos
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,'img')
        self.boat_img = pygame.image.load(img_folder,BOAT_IMG).convert_alpha()
        self.cannonball_img=pygame.image.load(img_folder,CANNONBALL_IMG).convert_alpha()
        
        #Criando dicionários para guardar os movimentos do navio
        
        #Busca arquivos para o movimento para direita
        self.boat_right = {}
        for pict in BOAT_WALK_RIGHT:
            self.boat_right[pict] = pygame.image.load(path.join(IMG_DIR,img)).convert_alpha()
            self.boat_right[pict] = pygame.transform.scale(self.boat_right[pict],(BOAT_WIDTH,BOAT_HEIGHT))

        #Busca arquivos para o movimento para esquerda
        self.boat_left = {}
        for pict in BOAT_WALK_LEFT:
            self.boat_left[pict] = pygame.image.load(path.join(IMG_DIR,img)).convert_alpha()
            self.boat_left[pict] = pygame.transform.scale(self.boat_left[pict],(BOAT_WIDTH,BOAT_HEIGHT))  

        #Busca arquivos para o movimento para cima
        self.boat_up = {}
        for pict in BOAT_WALK_UP:
            self.boat_up[pict] = pygame.image.load(path.join(IMG_DIR,img)).convert_alpha()
            self.boat_up[pict] = pygame.transform.scale(self.boat_up[pict],(BOAT_WIDTH,BOAT_HEIGHT)) 

        #Busca arquivos para o movimento para baixo
        self.boat_down = {}
        for pict in BOAT_WALK_DOWN:
            self.boat_right[pict] = pygame.image.load(path.join(IMG_DIR,img)).convert_alpha()
            self.boat_right[pict] = pygame.transform.scale(self.boat_down[pict],(BOAT_WIDTH,BOAT_HEIGHT)) 


    def new(self):
        #Começando as variáveis fo código
        
        self.todos_elementos = pygame.sprite.Group()
        self.cannonballs = pg.sprite.Group()
    
    def run(self):

    # Loop do jogo 

        self.playing = True
        
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def update(self):
        #atualiza os elementos gráficos do jogo
        self.todos_elementos.update()
    
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

game = True
#Ajuste de velocidade e tempo
clock=pygame.time.Clock()
FPS=30


#Criando o navio controlado
boat= Boat(assets,groups)
todos_elementos.add(boat)

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
    todos_elementos.update()

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados