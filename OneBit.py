""" 
ONEBIT THE GAME!

Jogo criado por: Leticia Coêlho Barbosa e Matheus Silva Melo de Oliveira
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
from tilemap_codigo import *
from os import path
from config import *
from sprites import *


#----- Criando classe Jogo responsável por atualizações e tratamento de eventos

class Jogo (pygame.sprite.Sprite):
    
    def __init__(self):

        #Inicializando biblioteca

        pygame.init() 

        #Inicializando a trilha sonora
        pygame.mixer.init()
        
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
        map_folder = path.join(game_folder,'map2')
        
        #Importando mapa:
        self.map = TiledMap(path.join(map_folder, 'mapa_matheus.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        
        #Imagens inicias
        self.init_img = pygame.image.load(path.join(IMG_DIR, 'deixando.gif')).convert()

        #Imagens sprites
        #self.cannonball_img=pygame.image.load(img_folder,'cannonball.png').convert_alpha()

        #Fontes utilizadas
        self.romulus = path.join(FONT_DIR, 'romulus.TTF')
        self.romulus_20 = pygame.font.Font(self.romulus, 20)
        self.romulus_30 = pygame.font.Font(self.romulus, 30)
        self.romulus_40 = pygame.font.Font(self.romulus, 40)
        self.romulus_80 = pygame.font.Font(self.romulus, 80)
        
        #Inicializando músicas de fundo-da abertura
        self.abertura = pygame.mixer.Channel(5)
        self.abertura.set_volume(0.3)
        abertura = pygame.mixer.music.load(path.join(MUSIC_DIR, 'pirates.ogg'))

        #Dicionário com os efeitos sonoros utilziados
        self.sound_effects = {}
        self.sound_effects['abertura'] = pygame.mixer.Sound(path.join(MUSIC_DIR, 'ONE_PIECE.ogg'))
        self.sound_effects['winner'] = pygame.mixer.Sound(path.join(MUSIC_DIR, 'pirates.ogg'))

        #Importando Imagens utilizadas

        self.boat_img = pygame.image.load(path.join(img_folder, BOAT_WALK_RIGHT)).convert_alpha()
        self.cannonball_img = pygame.image.load(path.join(img_folder, CANNONBALL_IMG)).convert_alpha()
 
        #Importando movimentação dos personagens

            #Esquerda
        self.boat_left = {}
        self.boat_left[BOAT_WALK_LEFT] =  pygame.image.load(path.join(IMG_DIR, BOAT_WALK_LEFT)).convert_alpha()
        self.boat_left[BOAT_WALK_LEFT] =  pygame.transform.scale(self.boat_left[BOAT_WALK_LEFT], (BOAT_WIDTH, BOAT_HEIGHT))
            # Direita
        self.boat_right = {}
        self.boat_right[BOAT_WALK_RIGHT] =  pygame.image.load(path.join(IMG_DIR, BOAT_WALK_RIGHT)).convert_alpha()
        self.boat_right[BOAT_WALK_RIGHT] =  pygame.transform.scale(self.boat_right[BOAT_WALK_RIGHT], (BOAT_WIDTH, BOAT_HEIGHT))
            # Cima
        self.boat_up = {}
        self.boat_up[BOAT_WALK_UP] =  pygame.image.load(path.join(IMG_DIR, BOAT_WALK_UP)).convert_alpha()
        self.boat_up[BOAT_WALK_UP] =  pygame.transform.scale(self.boat_up[BOAT_WALK_UP], (BOAT_WIDTH, BOAT_HEIGHT))
            # Baixo
        self.boat_down = {}
        self.boat_down[BOAT_WALK_DOWN] =  pygame.image.load(path.join(IMG_DIR, BOAT_WALK_DOWN)).convert_alpha()
        self.boat_down[BOAT_WALK_DOWN] =  pygame.transform.scale(self.boat_down[BOAT_WALK_DOWN], (BOAT_WIDTH, BOAT_HEIGHT))


    def new(self):
        #Começando as variáveis do código
        
        self.todos_elementos = pygame.sprite.Group()
        self.cannonballs = pygame.sprite.Group()
        self.ilhas = pygame.sprite.Group() #Obstaculo

        #Criando objetos no mapa
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Boat(self,tile_object.x, tile_object.y)

            #FALTA ACRESCENTAR MOBS E OBSTACULO        

        #Camera
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False        

    def run(self):
        #Iniciando o mixer de música
        pygame.mixer.music.play (loops=-1)

    # Loop do jogo 

        self.playing = True
        
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()
    

    #Criando Tela inicial:
    def init_screen(self): # Exibe a tela inicial do jogo
        
        self.abertura.play(self.sound_effects['abertura'])
        running = True # Configura o looping
        
        while running:
            
            self.clock.tick(30)
            self.information = False # Alterna exibição
            self.screen.fill(BLACK)
            
            # Fundo de tela
            self.image = self.init_img  
            self.image_rect = self.image.get_rect()
            self.image_rect.center = (WIDTH/2, self.image_rect.height/2)
            self.screen.blit(self.image, self.image_rect)
            
            # Desenha o texto 
            self.draw_text("ONE BIT", self.romulus_40, RED, WIDTH/2, HEIGHT/2 -10)
            self.draw_text("THE GAME", self.romulus_30, RED, WIDTH/2, HEIGHT/2 + 40)
            self.draw_text("PRESS 'ENTER' TO START", self.romulus_30, LIGHTRED, WIDTH/2, HEIGHT/2 + 80)
            self.draw_text("LETICIA & MATHEUS PRESENTS", self.romulus_30, BLACK, WIDTH/2, HEIGHT/2 - 80)
            self.draw_text("A DESIGN SOFTWARE's PROJECT", self.romulus_30, BLACK, WIDTH/2, HEIGHT/2 - 320)
            self.draw_text("Pressione 'ESC' para pausar o jogo", self.romulus_20, WHITE, WIDTH/5 +5, HEIGHT - 15)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN: # Se apertar Enter, entra no Jogo
                        running = False
                        self.Fase1 = True

        self.abertura.stop()

    def update(self):
        #Atualiza os elementos gráficos do jogo
        self.todos_elementos.update()
        self.camera.update(self.player)

        ##COLOCAR CONDIÇÕES DE COLISÃO

    def draw_grid(self):
        #Desenhando linhas (grid) na tela

        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    def draw(self):
        #Desenhando mapa na tela

        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        pygame.display.flip()

        ##FALTA COMPLEMENTO

    #Gerando textos na tela
    def draw_text(self, text, font, color, x, y): 
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surface, text_rect)

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

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def quit(self):

        #Fechar o jogo

        pygame.quit()
        sys.exit()

#Inicialização
jogo= Jogo()
#Loop Principal
while True:
        jogo.new()
        jogo.run()
        jogo.show_go_screen()

