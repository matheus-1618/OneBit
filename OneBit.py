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


#----- Criando classe Jogo -----#

class Jogo:
    
    def __init__(self):

        #Inicializando biblioteca

        pygame.init() 

        #Inicializando a trilha sonora
        pygame.mixer.init()
        
        #------Inicializando Tela------#
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        #------Inicializando Fases e transições------#
        self.playing = True                               
        self.paused = False 
        self.GAMEOVER = False
        self.TRANSITION= False
        self.INSTRUCTION=False
        self.WINNER= False
        self.Fase1 = True
        self.Fase2 = False
        self.init_load = False
        self.passa_fase= 0 
        
        #------Inicializando carregamento------#
        self.load_data()

        self.xp_total=0                                    # Xp acumulado total 

        self.propg= CANNONBALL_PROPG                       #Direcionamento dos tiros

        self.last_respawn=0                                #tempo para respawn        

        self.last_spawn=0                                  #Variavel para tempo de spawn       

        self.GAMEOVER = False                              #Variavel para iniciar a tela de Gameover
    
    def load_data(self):
        
        #------Caminhos para a busca de arquivo------#
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,'img')
        map_folder1 = path.join(game_folder,'map1')
        map_folder2 = path.join(game_folder,'map2N')
        
        #------Importando mapa------#
        if self.Fase1==True:
            self.map = TiledMap(path.join(map_folder1, 'map1.tmx'))
            self.map_img = self.map.make_map()
            self.map_rect = self.map_img.get_rect()
        
        elif self.Fase2==True:
            self.map = TiledMap(path.join(map_folder2, 'map2N.tmx'))
            self.map_img = self.map.make_map()
            self.map_rect = self.map_img.get_rect()
        
        #------Imagens inicias------#
        self.init_img ={}
        for imagem in INIT_IMG:
            self.init_img[imagem]=pygame.image.load(path.join(IMG_DIR, imagem)).convert_alpha()

        #------Imagens de instrução------#
        self.instruction_img ={}
        for img in INST_IMG:
            self.instruction_img[img]=pygame.image.load(path.join(IMG_DIR,img))

        #------Imagens de transição------#
        self.transition_img ={}
        for img in TRAN_IMG:
            self.transition_img[img]=pygame.image.load(path.join(IMG_DIR,img))

        #------Imagens da tela game_over------#
        self.game_over_img={}
        for img in OVER_IMG:
            self.game_over_img[img]=pygame.image.load(path.join(IMG_DIR, img)).convert_alpha()

        #------Imagens da tela de vencedor------#
        self.winner_img={}
        for imagem in WIN_IMG:
            self.winner_img[imagem]=pygame.image.load(path.join(IMG_DIR, imagem)).convert_alpha()

        #------Fontes utilizadas------#
        self.ken_pixel = path.join(FONT_DIR, 'kenpixel_blocks.TTF')
        self.romulus = path.join(FONT_DIR, 'romulus.TTF')
        self.trioDX = path.join(FONT_DIR, 'TrioDX.fon')
        self.romulus_20 = pygame.font.Font(self.romulus, 20)
        self.romulus_30 = pygame.font.Font(self.romulus, 30)
        self.romulus_80 = pygame.font.Font(self.romulus, 80)
        self.kenpixel_40 = pygame.font.Font(self.ken_pixel, 40)
        self.kenpixel_80 = pygame.font.Font(self.ken_pixel, 80)
        self.trioDX_10 = pygame.font.Font(self.trioDX, 10)
        self.trioDX_200 = pygame.font.Font(self.trioDX, 200)
        
        #------ Inicializando musicas------#
        #Inicializando músicas de fundo-da abertura
        self.abertura = pygame.mixer.Channel(1)
        self.abertura.set_volume(0.3)
        self.game_over = pygame.mixer.Channel(2)
        self.game_over.set_volume(0.3)
        self.transition = pygame.mixer.Channel(3)
        self.transition.set_volume(0.3)
        self.level1 = pygame.mixer.Channel(4)
        self.level1.set_volume(0.5)
        self.level2 = pygame.mixer.Channel(5)
        self.level2.set_volume(0.5)
        self.winner = pygame.mixer.Channel(6)
        self.winner.set_volume(0.3)

        #Dicionário com os efeitos sonoros utilizados
        self.sound_effects = {}
        self.sound_effects['abertura'] = pygame.mixer.Sound(path.join(MUSIC_DIR, 'ONE_PIECE.ogg'))
        self.sound_effects['game over'] = pygame.mixer.Sound(path.join(MUSIC_DIR, 'final.mp3'))
        self.sound_effects['level1 theme'] = pygame.mixer.Sound(path.join(MUSIC_DIR, 'pirates.ogg'))
        self.sound_effects['level2 theme'] = pygame.mixer.Sound(path.join(MUSIC_DIR, 'transition_theme.mp3'))
        self.sound_effects['new_fase'] = pygame.mixer.Sound(path.join(MUSIC_DIR, 'new_fase.mp3'))
        self.sound_effects['winner'] = pygame.mixer.Sound(path.join(MUSIC_DIR, 'winner.mp3'))
        self.sound_effects['cannonball'] = pygame.mixer.Sound(path.join(EFFECTS_DIR, 'tiro_canhão.mp3'))
        self.sound_effects['canhao']=pygame.mixer.Sound(path.join(EFFECTS_DIR,'canhao.mp3' ))
        self.sound_effects['cracken']=pygame.mixer.Sound(path.join(EFFECTS_DIR,'cracken.WAV' ))
        self.sound_effects['pirata1']=pygame.mixer.Sound(path.join(EFFECTS_DIR,'pirate1.mp3' ))
        self.sound_effects['pirata2']=pygame.mixer.Sound(path.join(EFFECTS_DIR,'pirate2.mp3' ))
        self.sound_effects['pirata3']=pygame.mixer.Sound(path.join(EFFECTS_DIR,'pirate3.mp3' ))
        self.sound_effects['pirata4']=pygame.mixer.Sound(path.join(EFFECTS_DIR,'pirate4.mp3' ))
        
        #------Importando Imagens utilizadas------#

        self.boat_img = pygame.image.load(path.join(img_folder, BOAT_IMG)).convert_alpha()
        self.cannonball_img = pygame.image.load(path.join(img_folder, CANNONBALL_IMG)).convert_alpha()
        self.cracken_img = pygame.image.load(path.join(img_folder, CRACKEN_IMG)).convert_alpha()

        #Carregando imagens de itens:
        self.carne_img=pygame.image.load(path.join(IMG_DIR,MEAT_IMG)).convert_alpha()
        self.rum_img=pygame.image.load(path.join(IMG_DIR,RUM_IMG)).convert_alpha()
        self.tesouro_img=pygame.image.load(path.join(IMG_DIR,TESOURO_IMG)).convert_alpha()
       
        #------Importando movimentação dos personagens------#

        #------Navio------#
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

        #------Piratas------#
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
        
        #Futuramente chamar last_spawn para mudança de fase
        while self.init_load:                               # carrega o Load novamente, cada vez q mudar de fase
            self.load_data()
            self.init_load = False
            self.last_respawn=  pygame.time.get_ticks()
            self.last_spawn = pygame.time.get_ticks()
        #------Criando sprites------# 
        
        self.all_sprites = pygame.sprite.Group()            #Grupo geral
        self.ilhas = pygame.sprite.Group()                  #Obstaculo
        self.crackens = pygame.sprite.Group()               #crackens
        self.cannonball = pygame.sprite.Group()             #Bala de canhão
        
        #Criando sprites dos navios em todas as direções:
        self.pirates_l1=pygame.sprite.Group()
        self.pirates_l2=pygame.sprite.Group()
        self.pirates_r1=pygame.sprite.Group()
        self.pirates_r2=pygame.sprite.Group()
        self.pirates_t1=pygame.sprite.Group()
        self.pirates_t2=pygame.sprite.Group()
        self.pirates_b1=pygame.sprite.Group()
        self.pirates_b2=pygame.sprite.Group()

        #criando sprites dos morteiros
        self.cannon1=pygame.sprite.Group()
        self.cannon2=pygame.sprite.Group()
        self.cannon3=pygame.sprite.Group()
        self.cannon4=pygame.sprite.Group()

        #Criando sprites de itens:
        self.Meat1= pygame.sprite.Group()
        self.Meat2= pygame.sprite.Group()
        self.Meat3= pygame.sprite.Group()
        self.Meat4= pygame.sprite.Group()
        self.Rum1= pygame.sprite.Group()
        self.Rum2= pygame.sprite.Group()
        self.Rum3= pygame.sprite.Group()
        self.Rum4= pygame.sprite.Group()
        self.tesouro1= pygame.sprite.Group()
        self.tesouro2= pygame.sprite.Group()
        self.tesouro3= pygame.sprite.Group()
        self.tesouro4= pygame.sprite.Group()

        #------Criando objetos no mapa------#

        for tile_object in self.map.tmxdata.objects:
            
            #Spawna o Navio no mapa
            if tile_object.name == 'boat':
                self.boat=Boat(self,tile_object.x, tile_object.y)
            #Spawna o Cracken no mapa
            if tile_object.name == 'cracken':
                Cracken(self, tile_object.x, tile_object.y)
            #Gera os limites da ilha
            if tile_object.name == 'Ilha': 
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            #Gera os obstáculos
            if tile_object.name == 'objetos': 
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            
            #Spawna navios inimigos em suas respectivas posições
            
            if tile_object.name == 'pirate_l1':
                Pirata_esquerda(self,self.pirate_esquerda[PIRATA_ESQUERDA], tile_object.x, tile_object.y)
            if tile_object.name == 'pirate_l2':
                Pirata_esquerda(self,self.pirate_esquerda[PIRATA_ESQUERDA], tile_object.x, tile_object.y)
            if tile_object.name == 'pirate_r1':
                Pirata_direita(self,self.pirate_direita[PIRATA_DIREITA], tile_object.x, tile_object.y)
            if tile_object.name == 'pirate_r2':
                Pirata_direita(self,self.pirate_direita[PIRATA_DIREITA], tile_object.x, tile_object.y)
            if tile_object.name == 'pirate_t1':
                Pirata_baixo(self,self.pirate_baixo[PIRATA_BAIXO], tile_object.x, tile_object.y)
            if tile_object.name == 'pirate_t2':
                Pirata_baixo(self,self.pirate_baixo[PIRATA_BAIXO], tile_object.x, tile_object.y)
            if tile_object.name == 'pirate_b1':
                Pirata_cima(self,self.pirate_cima[PIRATA_CIMA], tile_object.x, tile_object.y)
            if tile_object.name == 'pirate_b2':
                Pirata_cima(self,self.pirate_cima[PIRATA_CIMA], tile_object.x, tile_object.y)

            #Spawnando item Carne:
            
            if tile_object.name == 'Meat1':
                Carne(self,tile_object.x, tile_object.y)
            if tile_object.name == 'Meat2':
                Carne(self,tile_object.x, tile_object.y)
            if tile_object.name == 'Meat3':
                Carne(self,tile_object.x, tile_object.y)
            if tile_object.name == 'Meat4':
                Carne(self,tile_object.x, tile_object.y)
            
            #Spawnando item Rum:

            if tile_object.name == 'Rum1':
                Rum(self,tile_object.x, tile_object.y)
            if tile_object.name in 'Rum2':
                Rum(self,tile_object.x, tile_object.y)
            if tile_object.name in 'Rum3':
                Rum(self,tile_object.x, tile_object.y)
            if tile_object.name in 'Rum4':
                Rum(self,tile_object.x, tile_object.y)

            #Spawnando item Tesouro:
            if tile_object.name == 'Tesouro1':
                Tesouro(self,tile_object.x,tile_object.y)
            if tile_object.name == 'Tesouro2':
                Tesouro(self,tile_object.x,tile_object.y)
            if tile_object.name == 'Tesouro3':
                Tesouro(self,tile_object.x,tile_object.y)
            if tile_object.name == 'Tesouro4':
                Tesouro(self,tile_object.x,tile_object.y)
            
            #Spawnando a primeira bala de canhão
            if tile_object.name== 'cannon3':
                Cannonball2(self,vec(tile_object.x, tile_object.y),vec(-1,0))
        
        #------Camera------#
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False        

    def resnasce(self,string): 
        #Spawnando tesouros pelo mapa
        if string == 'Tesouro':
            aleatorio=choice([1,2,3,4])                             #Sorteando posição de respawn
            if aleatorio==1:
                for sprite in self.tesouro1.sprites(): 
                    sprite.kill()
                    self.last_spawn = pygame.time.get_ticks()        #Pegando tempo de spawn
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'Tesouro1':               #Posição 1
                        Tesouro(self,tile_object.x, tile_object.y)
            if aleatorio==2:
                for sprite in self.tesouro2.sprites(): 
                    sprite.kill()
                    self.last_spawn = pygame.time.get_ticks()        #Pegando tempo de spawn
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'Tesouro2':                #Posição 2
                        Tesouro(self,tile_object.x, tile_object.y)
            if aleatorio==3:
                for sprite in self.tesouro3.sprites(): 
                    sprite.kill()
                    self.last_spawn = pygame.time.get_ticks()      #Pegando tempo de spawn
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'Tesouro3':                #Posição 3
                        Tesouro(self,tile_object.x, tile_object.y) 
            if aleatorio==4:
                for sprite in self.tesouro4.sprites(): 
                    sprite.kill()
                    self.last_spawn = pygame.time.get_ticks()       #Pegando tempo de spawn
                for tile_object in self.map.tmxdata.objects:        
                    if tile_object.name == 'Tesouro4':                 #Posição 4
                        Tesouro(self,tile_object.x, tile_object.y)
        
        #Spawnando canhões nas ilhas
        if string=='cannons':
            channel2=self.sound_effects['canhao'].play() 
            sorteando=choice([1,2,3,4])
            if sorteando ==1:
                for sprite in self.cannon1.sprites():
                    self.last_respawn=pygame.time.get_ticks()
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name== 'cannon1':
                        Cannonball2(self,vec(tile_object.x, tile_object.y),vec(0,-1))
            if sorteando==2:
                for sprite in self.cannon1.sprites():
                    self.last_respawn=pygame.time.get_ticks()
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name== 'cannon2':
                        Cannonball2(self,vec(tile_object.x, tile_object.y),vec(1,0))
            if sorteando==3:
                for sprite in self.cannon1.sprites():
                        self.last_respawn=pygame.time.get_ticks()
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name== 'cannon3':
                        Cannonball2(self,vec(tile_object.x, tile_object.y),vec(-1,0))
            else:
                for sprite in self.cannon1.sprites():
                    self.last_respawn=pygame.time.get_ticks()
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name== 'cannon4':
                        Cannonball2(self,vec(tile_object.x, tile_object.y),vec(0,1))
        
        #Respawn piratas esquerda:
        if string == 'pirate_l':
            aleatorio=choice([1,2])                            #Sorteando posição
            if aleatorio ==1:
                for sprite in self.pirates_l1.sprites(): 
                    sprite.kill()
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'pirate_l1':
                        Pirata_esquerda(self,self.pirate_esquerda[PIRATA_ESQUERDA], tile_object.x, tile_object.y)
            
            else:
                for sprite in self.pirates_l2.sprites(): 
                    sprite.kill()
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'pirate_l2':
                        Pirata_esquerda(self,self.pirate_esquerda[PIRATA_ESQUERDA], tile_object.x, tile_object.y)

        #Respawn piratas direita:
        if string == 'pirate_r':
            aleatorio=choice([1,2])                            #Sorteando posição   
            if aleatorio==1:
                for sprite in self.pirates_r1.sprites(): 
                    sprite.kill()
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'pirate_r1':
                        Pirata_direita(self,self.pirate_direita[PIRATA_DIREITA], tile_object.x, tile_object.y)
            else:
                for sprite in self.pirates_r2.sprites(): 
                    sprite.kill()
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'pirate_r2':
                        Pirata_direita(self,self.pirate_direita[PIRATA_DIREITA], tile_object.x, tile_object.y)
        
        #Respawn piratas topo:
        if string == 'pirate_t':
            aleatorio=choice([1,2])                             #Sorteando posição
            if aleatorio==1:
                for sprite in self.pirates_t1.sprites(): 
                    sprite.kill()
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'pirate_t1':
                        Pirata_baixo(self,self.pirate_baixo[PIRATA_BAIXO], tile_object.x, tile_object.y)    
            else:
                for sprite in self.pirates_t2.sprites(): 
                    sprite.kill()   
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'pirate_t2':
                        Pirata_baixo(self,self.pirate_baixo[PIRATA_BAIXO], tile_object.x, tile_object.y)
        
        #Respawn piratas base:
        if string == 'pirate_b':
            aleatorio=choice([1,2])                              #Sorteando posição
            if aleatorio==1:
                for sprite in self.pirates_b1.sprites(): 
                    sprite.kill()
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'pirate_b1':
                        Pirata_cima(self,self.pirate_cima[PIRATA_CIMA], tile_object.x, tile_object.y) 
            else:
                for sprite in self.pirates_b2.sprites(): 
                    sprite.kill()
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'pirate_b2':
                        Pirata_cima(self,self.pirate_cima[PIRATA_CIMA], tile_object.x, tile_object.y)    
        
        #Respawn Carnes:
        if string == 'Meat':
            aleatorio=choice([1,2,3,4])                           #Sorteando posição de respawn
            if aleatorio==1:
                for sprite in self.Meat1.sprites(): 
                    sprite.kill()
                    self.last_spawn = pygame.time.get_ticks()     #Pegando tempo de spawn
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'Meat1':               #Posição 1
                        Carne(self,tile_object.x, tile_object.y)
            if aleatorio==2:
                for sprite in self.Meat2.sprites(): 
                    sprite.kill()
                    self.last_spawn = pygame.time.get_ticks()      #Pegando tempo de spawn
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'Meat2':                #Posição 2
                        Carne(self,tile_object.x, tile_object.y)
            if aleatorio==3:
                for sprite in self.Meat3.sprites(): 
                    sprite.kill()
                    self.last_spawn = pygame.time.get_ticks()      #Pegando tempo de spawn
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'Meat3':                #Posição 3
                        Carne(self,tile_object.x, tile_object.y) 
            if aleatorio==4:
                for sprite in self.Meat2.sprites(): 
                    sprite.kill()
                    self.last_spawn = pygame.time.get_ticks()       #Pegando tempo de spawn
                for tile_object in self.map.tmxdata.objects:        
                    if tile_object.name == 'Meat4':                 #Posição 4
                        Carne(self,tile_object.x, tile_object.y)

        #Respawn Rum:
        if string == 'Rum':
            aleatorio=choice([1,2,3,4])                             #Sorteando posição de respawn
            if aleatorio==1:
                for sprite in self.Rum1.sprites(): 
                    sprite.kill()
                    self.last_spawn = pygame.time.get_ticks()       #Pegando tempo de spawn
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'Rum1':                  #Posição 1
                        Rum(self,tile_object.x, tile_object.y)
            if aleatorio==2:
                for sprite in self.Rum2.sprites(): 
                    sprite.kill()
                    self.last_spawn = pygame.time.get_ticks()        #Pegando tempo de spawn
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'Rum2':                   #Posição 2
                        Rum(self,tile_object.x, tile_object.y)
            if aleatorio==3:
                for sprite in self.Rum3.sprites(): 
                    sprite.kill()
                    self.last_spawn = pygame.time.get_ticks()         #Pegando tempo de spawn
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'Rum3':                    #Posição 3
                        Rum(self,tile_object.x, tile_object.y) 
            if aleatorio==4:
                for sprite in self.Rum4.sprites(): 
                    sprite.kill()
                    self.last_spawn = pygame.time.get_ticks()         #Pegando tempo de spawn
                for tile_object in self.map.tmxdata.objects:
                    if tile_object.name == 'Rum4':                    #Posição 4
                        Rum(self,tile_object.x, tile_object.y)

    def run(self):
        
    #Iniciando o mixer de música
        if self.Fase1==True:
            self.level1.play(self.sound_effects['level1 theme']) 
            self.level2.stop()
            
        if self.Fase2==True:
            self.level1.stop()
            self.level2.play(self.sound_effects['level2 theme']) 
        
    #------Loop do jogo------#
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0                   # fix for Python 2.x
            self.events()
            self.update()    
            self.draw()
    

    #------Criando Tela inicial------#
    def init_screen(self):                                            # Exibe a tela inicial do jogo
        self.passagem_imagem = 1
        self.winner.stop()
        self.game_over.stop()
        self.abertura.play(self.sound_effects['abertura'])
        running = True 
        self.last_update = pygame.time.get_ticks()                                              
        
        while running:
            now = pygame.time.get_ticks()
            delta_t=now - self.last_update
            if delta_t>50:
                delta_t=0
                self.last_update=now
                self.passagem_imagem+=1
                if self.passagem_imagem>5:
                    self.passagem_imagem=1
            self.clock.tick(30)                                       #Contagem  interna pra vinda dos crackens                                 
            
            # Fundo de tela
            self.image = self.init_img['frame-{}.gif'.format(self.passagem_imagem)]  
            self.image_rect = self.image.get_rect()
            self.image_rect.center = (WIDTH/2, self.image_rect.height/2)
            self.screen.blit(self.image, self.image_rect)
            
            # Desenha o texto 
            self.draw_text("ONE BIT", self.kenpixel_80, RED, WIDTH/2, HEIGHT/2 -20)
            self.draw_text("THE GAME", self.kenpixel_40, RED, WIDTH/2, HEIGHT/2 + 40)
            self.draw_text("PRESS 'ENTER' TO START LEVEL 1", self.romulus_30, BLACK, WIDTH/2, HEIGHT/2 + 120)
            self.draw_text("LETICIA & MATHEUS PRESENTS", self.romulus_30, WHITE, WIDTH/2, HEIGHT/2 - 100)
            self.draw_text("A DESIGN SOFTWARE's PROJECT", self.romulus_30, BLACK, WIDTH/2, HEIGHT/2 - 320)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:                    
                        running = False
                        self.INSTRUCTION=True
                        self.Fase1 = False
                        self.Fase2=False
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
        self.abertura.stop()
    
    #------Criando Tela de Instruções------#
    def instruction_screen(self):                                        # Exibe a tela de instruções do jogo
        
        if self.INSTRUCTION :                                          
        
            self.passagem_imagemi = 1
            self.abertura.play(self.sound_effects['abertura'])
            running = True 
            self.last_updatei = pygame.time.get_ticks()                                              
            self.clock.tick(30)                                           #Contagem  interna pra vinda dos crackens

            while running:
                now = pygame.time.get_ticks()
                delta_t=now - self.last_updatei
                
                if delta_t>7000:
                    delta_t=0
                    self.last_updatei=now
                    self.passagem_imagemi+=1
                    if self.passagem_imagemi>2:
                        self.passagem_imagemi=1
                
                # Imagem tela de instruções:
                
                self.image = self.instruction_img['inst-{}.png'.format(self.passagem_imagemi)]
                self.instruction_img['inst-{}.png'.format(self.passagem_imagemi)] =  pygame.transform.scale(self.image, (WIDTH, HEIGHT))
                
                self.image_rect = self.image.get_rect()
                self.image_rect.center = (WIDTH/2, self.image_rect.height/2)
                self.screen.blit(self.image, self.image_rect)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        self.quit()
                    
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RETURN:                    
                            running = False
                            self.INSTRUCTION=False
                            self.Fase1 = True
                            self.Fase2=False
                        if event.key == pygame.K_ESCAPE:
                            self.quit()
            self.abertura.stop()

    #------Criando Tela de transição de fase------#
    def troca_de_fase_screen(self):                                          
        if self.TRANSITION:
            self.passagem_imagem3=1
            self.level1.stop()
            self.transition.play(self.sound_effects['new_fase'])
            running = True                                                # Configura o looping
            self.last_update3=pygame.time.get_ticks()

            while running:
                now=pygame.time.get_ticks()
                delta=now-self.last_update3
                if delta>50:
                    delta=0
                    self.last_update3=now
                    self.passagem_imagem3+=1
                    if self.passagem_imagem3>39:
                        self.passagem_imagem3=1
                self.clock.tick(30)                                        #Contagem  interna pra vinda dos crackens
                                
                # Fundo de tela
                self.image = self.transition_img['frae-{}.gif'.format(self.passagem_imagem3)]   
                self.image_rect = self.image.get_rect()
                self.image_rect.center = (WIDTH/2, self.image_rect.height/2)
                self.screen.blit(self.image, self.image_rect)
                
                # Desenha o texto 
                self.draw_text("PRESS 'ENTER' TO START LEVEL 2", self.romulus_30, WHITE, WIDTH/2, HEIGHT/2 + 120)
                self.draw_text("YOU DEFIED THE", self.kenpixel_40, YELLOW, WIDTH/2, HEIGHT/2 - 200)
                self.draw_text("WRATH OF", self.kenpixel_40, YELLOW, WIDTH/2, HEIGHT/2 - 160)
                self.draw_text("SEVEN SEAS...", self.kenpixel_40, YELLOW, WIDTH/2, HEIGHT/2 - 120)
                self.draw_text("ARE YOU  ", self.kenpixel_40, YELLOW, WIDTH/2, HEIGHT/2 - 80)
                self.draw_text("READY FOR ", self.kenpixel_40, YELLOW, WIDTH/2, HEIGHT/2 - 40)
                self.draw_text("THE CONSEQUENCES?", self.kenpixel_40, YELLOW, WIDTH/2, HEIGHT/2)
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        self.quit()
                    
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RETURN:  
                            running = False                  
                            self.Fase2 = True
                            self.Fase1 = False
                            
                        if event.key == pygame.K_ESCAPE:
                            self.quit()
            self.transition.stop()
     #------Criando Tela de game_over------#
    def game_over_screen(self):                                          # Exibe a tela de derrota do jogo
        if self.GAMEOVER:
            self.passagem_imagem2=1
            self.level1.stop()
            self.level2.stop()
            self.game_over.play(self.sound_effects['game over'])
            running = True                                               # Configura o looping
            self.last_update2=pygame.time.get_ticks()

            while running:
                now=pygame.time.get_ticks()
                delta=now-self.last_update2
                if delta>100:
                    delta=0
                    self.last_update2=now
                    self.passagem_imagem2+=1
                    if self.passagem_imagem2>14:
                        self.passagem_imagem2=1
                self.clock.tick(30)                                       #Contagem  interna pra vinda dos crackens
                
                # Fundo de tela
                self.image = self.game_over_img['fram-{}.gif'.format(self.passagem_imagem2)]  
                self.image_rect = self.image.get_rect()
                self.image_rect.center = (WIDTH/2, self.image_rect.height/2)
                self.screen.blit(self.image, self.image_rect)
                
                # Desenha o texto 
                self.draw_text("GAME OVER", self.kenpixel_80, RED, WIDTH/2, HEIGHT/2 -20)
                self.draw_text("PRESS 'ENTER' TO START AGAIN", self.romulus_30, BLACK, WIDTH/2, HEIGHT/2 + 120)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        self.quit()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RETURN:               
                            running = False
                            self.GAMEOVER= False
                            self.playing=True
                            self.Fase1 = True
                            self.Fase2=False
                            jogo.__init__()
                        if event.key == pygame.K_ESCAPE:
                            self.quit()
            self.game_over.stop()

    #------Criando Tela Vencedor------#
    def winner_screen(self):                                            # Exibe a tela inicial do jogo
        if self.WINNER:
            self.passagem_imagem1 = 1
            self.level2.stop()
            self.winner.play(self.sound_effects['winner'])
            running = True          
            self.last_update1 = pygame.time.get_ticks()                                      
            
            while running:
                now =pygame.time.get_ticks()
                delta_t1=now -self.last_update1
                if delta_t1>100:
                    delta_t1=0
                    self.last_update1=now
                    self.passagem_imagem1+=1
                    if self.passagem_imagem1>14:
                        self.passagem_imagem1=1
                self.clock.tick(30)                                     # Contagem  interna pra vinda dos crackens
                
                # Fundo de tela
                self.image = self.winner_img['mar-{}.gif'.format(self.passagem_imagem1)]  
                self.image_rect = self.image.get_rect()
                self.image_rect.center = (WIDTH/2, self.image_rect.height/2)
                self.screen.blit(self.image, self.image_rect)
                
                # Desenha o texto 
                self.draw_text("PRESS 'ENTER' TO PLAY AGAIN", self.romulus_30, WHITE, WIDTH/2, HEIGHT/2 + 150)
                self.draw_text("YOU WON!", self.kenpixel_80, BLACK, WIDTH/2, HEIGHT/2 - 160)
                self.draw_text("YOU ARE THE", self.kenpixel_80, BLACK, WIDTH/2, HEIGHT/2 - 80)
                self.draw_text("NEW KING OF", self.kenpixel_80, BLACK, WIDTH/2, HEIGHT/2 )
                self.draw_text("THE PIRATES", self.kenpixel_80, BLACK, WIDTH/2, HEIGHT/2 +80)
                pygame.display.flip()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        self.quit()
                    
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RETURN:                 
                            running = False
                            self.GAMEOVER= False
                            self.playing=True
                            self.Fase1 = True
                            self.Fase2=False
                            jogo.__init__()
                        if event.key == pygame.K_ESCAPE:
                            self.quit()
            self.winner.stop()
    
    def update(self):

        #Atualiza os elementos gráficos do jogo
        self.all_sprites.update()
        self.camera.update(self.boat)

        #Se o jogador morre
        if self.boat.health <= 0:
            self.playing = False 
            self.GAMEOVER = True
        
        #Acrescentar condição tempo para mudança de fase
        
        #------Bala de canhão atinge jogador------#
        lista_canhões=[self.cannon1,self.cannon2,self.cannon3,self.cannon4]
        for m in lista_canhões:
            hits = pygame.sprite.spritecollide(self.boat, m, True, collide_hit_rect)
            for hit in hits:
                self.boat.health -= CANNONBALL_DAMAGE2
                self.boat.speed-=CANNONBALL_LESS_SPEED
                hit.vel = vec(0, 0)

        #------Cracken atinge jogador------#
        hits = pygame.sprite.spritecollide(self.boat, self.crackens, False, collide_hit_rect)
        for hit in hits:
            channel2=self.sound_effects['cracken'].play() 
            self.boat.health -= CRACKEN_DAMAGE
            hit.vel = vec(0, 0)
            if self.boat.health <= 0:
                self.GAMEOVER = True
                self.playing = False
            if self.GAMEOVER== True:
                pygame.mixer.music.stop() 
        if hits:
            self.boat.pos += vec(CRACKEN_KNOCKBACK, 0).rotate(-hits[0].rot)
        
        #------Balas atingem Crackens------#
        hits = pygame.sprite.groupcollide(self.crackens, self.cannonball, False, True)
        for hit in hits:
            hit.health -= CANNONBALL_DAMAGE
            hit.vel = vec(0, 0)
 
        #------Balas atigem piratas--------#
        
        #Criando lista para grupos de piratas:
        lista=[self.pirates_l1,self.pirates_l2,self.pirates_r1,self.pirates_r2,self.pirates_t1,self.pirates_t2,self.pirates_b1,self.pirates_b2]
        for k in lista:
            hits = pygame.sprite.groupcollide(k, self.cannonball, False, True)                     #Colisão bala com pirata 
            for hit in hits:                                                                       # Verificando se houve colisão           
                hit.health -= CANNONBALL_DAMAGE
                hit.vel = vec(0, 0)

        #------Piratas atingem navio------#

        #Piratas Esquerda:

        hits = pygame.sprite.spritecollide(self.boat, self.pirates_l1, False, collide_hit_rect)    #Colisão barco pirata
        for hit in hits:                                                                           #Verificando se houve colisão     
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                hit.health -= CANNONBALL_DAMAGE/5
                self.boat.pos += vec(-MOB_KNOCKBACK, 0)

        hits = pygame.sprite.spritecollide(self.boat, self.pirates_l2, False, collide_hit_rect)    #Colisão barco pirata
        for hit in hits:                                                                           #Verificando se houve colisão                 
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                hit.health -= CANNONBALL_DAMAGE/5
                self.boat.pos += vec(-MOB_KNOCKBACK, 0)

        #Piratas Direita:

        hits = pygame.sprite.spritecollide(self.boat, self.pirates_r1, False, collide_hit_rect)    #Colisão barco pirata
        for hit in hits:                                                                           #Verificando se houve colisão                    
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                hit.health -= CANNONBALL_DAMAGE/5
                self.boat.pos += vec(MOB_KNOCKBACK, 0)
        
        hits = pygame.sprite.spritecollide(self.boat, self.pirates_r2, False, collide_hit_rect)    #Colisão barco pirata
        for hit in hits:                                                                           #Verificando se houve colisão                                 
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                hit.health -= CANNONBALL_DAMAGE/5
                self.boat.pos += vec(MOB_KNOCKBACK, 0)      

        #Piratas Cima:

        hits = pygame.sprite.spritecollide(self.boat, self.pirates_b1, False, collide_hit_rect)   #Colisão barco pirata
        for hit in hits:                                                                          #Verificando se houve colisão 
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                hit.health -= CANNONBALL_DAMAGE/5
                self.boat.pos += vec(0,-MOB_KNOCKBACK)
        
        hits = pygame.sprite.spritecollide(self.boat, self.pirates_b2, False, collide_hit_rect)   #Colisão barco pirata
        for hit in hits:                                                                          #Verificando se houve colisão           
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                hit.health -= CANNONBALL_DAMAGE/5
                self.boat.pos += vec(0,-MOB_KNOCKBACK)       

        #Piratas Baixo:

        hits = pygame.sprite.spritecollide(self.boat, self.pirates_t1, False, collide_hit_rect)   #Colisão barco pirata
        for hit in hits:                                                                          #Verificando se houve colisão                      
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                hit.health -= CANNONBALL_DAMAGE/5
                self.boat.pos += vec(0,MOB_KNOCKBACK)
        
        hits = pygame.sprite.spritecollide(self.boat, self.pirates_t2, False, collide_hit_rect)   #Colisão barco pirata
        for hit in hits:                                                                          #Verificando se houve colisão          
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                hit.health -= CANNONBALL_DAMAGE/5
                self.boat.pos += vec(0,MOB_KNOCKBACK)        

        #------Player colide com Itens------#
        
        lista_tesouro=[self.tesouro1, self.tesouro2, self.tesouro3, self.tesouro4]

        for i in lista_tesouro:
            hits = pygame.sprite.spritecollide (self.boat, i, False, pygame.sprite.collide_mask)
            for hit in hits:
                channel2=self.sound_effects['pirata2'].play() 
                self.xp_total+=TESOURO_XP                    
                hit.kill()
                self.resnasce('Tesouro')

        #Criando lista para armazenar carne

        lista_carne=[self.Meat1, self.Meat2, self.Meat3, self.Meat4]

        for i in lista_carne:
            hits = pygame.sprite.spritecollide (self.boat, i, False, pygame.sprite.collide_mask)
            for hit in hits:
                channel2=self.sound_effects['pirata4'].play()
                self.boat.health+= CARNE_LIFE
                self.xp_total+=CARNE_XP                   
                hit.kill()
                self.resnasce('Meat')

        #Criando lista para armazenar bebida
        lista_rum=[self.Rum1, self.Rum2, self.Rum3, self.Rum4]
        
        for i in lista_rum:
            hits = pygame.sprite.spritecollide (self.boat, i, False, pygame.sprite.collide_mask)
            for hit in hits:
                channel2=self.sound_effects['pirata3'].play()
                self.propg+=5               
                hit.kill()
                self.resnasce('Rum')

    def proxima_fase(self):
        if self.passa_fase== 0:                                 # se estava na fase inicial
            self.Fase1 = False
            self.playing = False
            self.TRANSITION=True
            self.init_load = True
            self.xp_total=0
            self.boat.health=BOAT_HEALTH
            self.boat.speed= BOAT_SPEED
            self.propg= CANNONBALL_PROPG
            self.passa_fase= 1                                   
            
        elif self.passa_fase== 1:                              
            self.Fase2 = False
            self.playing = False
            self.Fase1 = False
            self.xp_total=0
            self.passa_fase= 0                                  
            self.init_load = False
            self.TRANSITION=False
            self.GAMEOVER = False
            self.WINNER = True
            
    def draw_grid(self):
        #Desenhando linhas (grid) na tela

        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    def draw(self):
        
        #------Desenhando mapa na tela------#
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        
        #------Desenhando a barra de vida dos personagens------#
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
        
        if self.draw_debug:
            for wall in self.ilhas:
                pygame.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        draw_boat_health(self.screen, 10, 30, self.boat.health / BOAT_HEALTH)
        draw_boat_xp(self.screen,10 ,50,self.xp_total/BOAT_XP_MAX)
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

    def quit(self):

        #Fechar o jogo

        pygame.quit()
        sys.exit()

#------Inicialização------#
jogo= Jogo()

#------Loop Principal-----#

while True:
    jogo.init_screen()
    while jogo.INSTRUCTION:
        jogo.instruction_screen()
    
    while jogo.Fase1:
        jogo.new()
        jogo.run()
        jogo.troca_de_fase_screen()
        jogo.game_over_screen()
    
    while jogo.Fase2:
        jogo.new()
        jogo.run()
        jogo.winner_screen()
        jogo.game_over_screen()
        

