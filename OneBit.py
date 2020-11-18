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

class Jogo:
    
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

        #Fontes utilizadas
        self.ken_pixel = path.join(FONT_DIR, 'kenpixel_blocks.TTF')
        self.romulus = path.join(FONT_DIR, 'romulus.TTF')
        self.trioDX = path.join(FONT_DIR, 'TrioDX.fon')
        self.romulus_20 = pygame.font.Font(self.romulus, 20)
        self.romulus_30 = pygame.font.Font(self.romulus, 30)
        self.kenpixel_40 = pygame.font.Font(self.ken_pixel, 40)
        self.kenpixel_80 = pygame.font.Font(self.ken_pixel, 80)
        self.trioDX_10 = pygame.font.Font(self.trioDX, 10)
        self.trioDX_200 = pygame.font.Font(self.trioDX, 200)
        
        #Inicializando músicas de fundo-da abertura
        self.abertura = pygame.mixer.Channel(5)
        self.abertura.set_volume(0.3)
        abertura = pygame.mixer.music.load(path.join(MUSIC_DIR, 'ONE_PIECE.ogg'))
        pygame.mixer.music.load(path.join(MUSIC_DIR, 'pirates.ogg'))
        pygame.mixer.music.set_volume(0.5)
        #Dicionário com os efeitos sonoros utilziados
        self.sound_effects = {}
        self.sound_effects['abertura'] = pygame.mixer.Sound(path.join(MUSIC_DIR, 'ONE_PIECE.ogg'))
        self.sound_effects['cannonball'] = pygame.mixer.Sound(path.join(EFFECTS_DIR, 'tiro_canhão.mp3'))

        #Importando Imagens utilizadas

        self.boat_img = pygame.image.load(path.join(img_folder, BOAT_IMG)).convert_alpha()
        self.cannonball_img = pygame.image.load(path.join(img_folder, CANNONBALL_IMG)).convert_alpha()
        self.cracken_img = pygame.image.load(path.join(img_folder, CRACKEN_IMG)).convert_alpha()

        #Importando movimentação dos personagens

        #Navio
            #Esquerda
        self.boat_left = {}
        self.boat_left[BOAT_WALK_LEFT] =  pygame.image.load(path.join(IMG_DIR,'Barco', BOAT_WALK_LEFT)).convert_alpha()
        self.boat_left[BOAT_WALK_LEFT] =  pygame.transform.scale(self.boat_left[BOAT_WALK_LEFT], (BOAT_WIDTH, BOAT_HEIGHT))
            # Direita
        self.boat_right = {}
        self.boat_right[BOAT_WALK_RIGHT] =  pygame.image.load(path.join(IMG_DIR,'Barco', BOAT_WALK_RIGHT)).convert_alpha()
        self.boat_right[BOAT_WALK_RIGHT] =  pygame.transform.scale(self.boat_right[BOAT_WALK_RIGHT], (BOAT_WIDTH, BOAT_HEIGHT))
            # Cima
        self.boat_up = {}
        self.boat_up[BOAT_WALK_UP] =  pygame.image.load(path.join(IMG_DIR,'Barco', BOAT_WALK_UP)).convert_alpha()
        self.boat_up[BOAT_WALK_UP] =  pygame.transform.scale(self.boat_up[BOAT_WALK_UP], (BOAT_WIDTH, BOAT_HEIGHT))
            # Baixo
        self.boat_down = {}
        self.boat_down[BOAT_WALK_DOWN] =  pygame.image.load(path.join(IMG_DIR,'Barco', BOAT_WALK_DOWN)).convert_alpha()
        self.boat_down[BOAT_WALK_DOWN] =  pygame.transform.scale(self.boat_down[BOAT_WALK_DOWN], (BOAT_WIDTH, BOAT_HEIGHT))

        #Piratas
            #Esquerda
        self.pirate_esquerda = {}
        self.pirate_esquerda[PIRATA_ESQUERDA]=pygame.image.load(path.join(IMG_DIR,PIRATA_ESQUERDA))
        self.pirate_esquerda[PIRATA_ESQUERDA]=pygame.transform.scale(self.pirate_esquerda[PIRATA_ESQUERDA],(PIRATA_WIDTH,PIRATA_HEIGHT))

            #Direita
        self.pirate_direita = {}
        self.pirate_direita[PIRATA_DIREITA]=pygame.image.load(path.join(IMG_DIR,PIRATA_DIREITA))
        self.pirate_direita[PIRATA_DIREITA]=pygame.transform.scale(self.pirate_direita[PIRATA_DIREITA],(PIRATA_WIDTH,PIRATA_HEIGHT))
            #Cima
        self.pirate_cima = {}
        self.pirate_cima[PIRATA_CIMA]=pygame.image.load(path.join(IMG_DIR,PIRATA_CIMA))
        self.pirate_cima[PIRATA_CIMA]=pygame.transform.scale(self.pirate_cima[PIRATA_CIMA],(PIRATA_WIDTH,PIRATA_HEIGHT))
            #Baixo
        self.pirate_baixo = {}
        self.pirate_baixo[PIRATA_BAIXO]=pygame.image.load(path.join(IMG_DIR,PIRATA_BAIXO))
        self.pirate_baixo[PIRATA_BAIXO]=pygame.transform.scale(self.pirate_baixo[PIRATA_BAIXO],(PIRATA_WIDTH,PIRATA_HEIGHT))
    
    def new(self):
        #Começando as variáveis do código
        
        self.all_sprites = pygame.sprite.Group()#Grupo geral
        self.ilhas = pygame.sprite.Group() #Obstaculo
        self.crackens = pygame.sprite.Group()#crackens
        self.cannonball = pygame.sprite.Group()#Bala de canhão
        self.pirates=pygame.sprite.Group()#Piratas inimigos

        #Criando objetos no mapa
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'boat':#Spawna o Navio no mapa
                self.boat=Boat(self,tile_object.x, tile_object.y)
            if tile_object.name == 'cracken':#Spawna o Cracken no mapa
                Cracken(self, tile_object.x, tile_object.y)
            if tile_object.name == 'island':#Gera os limites da ilha
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            #Spawna os piratas no mapa
            if tile_object.name == 'pirate_l':
                Pirata_esquerda(self,self.pirate_esquerda[PIRATA_ESQUERDA], tile_object.x, tile_object.y)
            if tile_object.name == 'pirate_r':
                Pirata_direita(self,self.pirate_direita[PIRATA_DIREITA], tile_object.x, tile_object.y)
            if tile_object.name == 'pirate_t':
                Pirata_baixo(self,self.pirate_baixo[PIRATA_BAIXO], tile_object.x, tile_object.y)
            if tile_object.name == 'pirate_b':
                Pirata_cima(self,self.pirate_cima[PIRATA_CIMA], tile_object.x, tile_object.y)
       

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
            self.draw_text("ONE BIT", self.kenpixel_80, RED, WIDTH/2, HEIGHT/2 -20)
            self.draw_text("THE GAME", self.kenpixel_40, RED, WIDTH/2, HEIGHT/2 + 40)
            self.draw_text("PRESS 'ENTER' TO START", self.romulus_30, BLACK, WIDTH/2, HEIGHT/2 + 120)
            self.draw_text("LETICIA & MATHEUS PRESENTS", self.romulus_30, BLACK, WIDTH/2, HEIGHT/2 - 100)
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
        self.all_sprites.update()
        self.camera.update(self.boat)
        # Cracken atinge jogador
        hits = pygame.sprite.spritecollide(self.boat, self.crackens, False, collide_hit_rect)
        for hit in hits:
            self.boat.health -= CRACKEN_DAMAGE
            hit.vel = vec(0, 0)
            if self.boat.health <= 0:
                self.playing = False
        if hits:
            self.boat.pos += vec(CRACKEN_KNOCKBACK, 0).rotate(-hits[0].rot)
        # balas atingem crackens
        hits = pygame.sprite.groupcollide(self.crackens, self.cannonball, False, True)
        for hit in hits:
            hit.health -= CANNONBALL_DAMAGE
            hit.vel = vec(0, 0)
        #balas atingem barcos
        hits = pygame.sprite.groupcollide(self.pirates, self.cannonball, False, True)
        for hit in hits:
            hit.health -= CANNONBALL_DAMAGE
            hit.vel = vec(0, 0)

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
        #desenhando a barra de vida dos personagens
        for sprite in self.all_sprites:
            if isinstance(sprite, Cracken):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if isinstance(sprite,Pirata_esquerda):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if isinstance(sprite, Pirata_direita):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if isinstance(sprite, Pirata_baixo):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if isinstance(sprite, Pirata_cima):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pygame.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        #RETIRAR DEPOIS,APENAS PARA AUXILIO DE OBJETOS
        if self.draw_debug:
            for wall in self.ilhas:
                pygame.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        draw_boat_health(self.screen, 10, 10, self.boat.health / BOAT_HEALTH)
        pygame.display.flip()


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
    jogo.init_screen()
    while True:
        jogo.new()
        jogo.run()
        

