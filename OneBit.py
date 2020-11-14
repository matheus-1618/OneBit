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

#----- Criando classe Jogo responsável por atualizações e tratamento de eventos

class Jogo (pygame.sprite.Sprite):
    
    def __init__(self):

        #Inicializando biblioteca

        pygame.init() 
        
        #Inicializando Tela:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    #Carregando imagens importantes
    def load_data(self):
        
        #Especificando os caminhos de busca dos arquivos
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,'img')
        map_folder = path.join(game_folder,'map1')
        
        #Criando mapa:
        self.map = TiledMap(path.join(map_folder, 'map1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        
        #Imagens sprites
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
        self.cannonballs = pygame.sprite.Group()
    
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

    def draw_grid(self):
        #Desenhando linhas (grid) na tela

        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    def draw(self):
        #Desenhando mapa na tela

        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img)
        pg.display.flip()

    def events(self):

        #Guardando eventos principais ocorridos durante o jogo:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:       
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_h:
                    self.draw_debug = not self.draw_debug

    def quit(self):

        #Fechar o jogo

        pygame.quit()
        sys.exit()

