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


#----- Criando classe Jogo responsável por atualizações e tratamento de eventos -----#

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
        self.load_data()

        self.last_spawn=0     #Variavel para tempo de spawn       

    def load_data(self):
        
        #------Caminhos para a busca de arquivo------#
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder,'img')
        map_folder = path.join(game_folder,'map2')
        
        #------Importando mapa------#
        self.map = TiledMap(path.join(map_folder, 'mapa_matheus.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        
        #------Imagens inicias------#
        self.init_img = pygame.image.load(path.join(IMG_DIR, 'deixando.gif')).convert()

        #------Fontes utilizadas------#
        self.ken_pixel = path.join(FONT_DIR, 'kenpixel_blocks.TTF')
        self.romulus = path.join(FONT_DIR, 'romulus.TTF')
        self.trioDX = path.join(FONT_DIR, 'TrioDX.fon')
        self.romulus_20 = pygame.font.Font(self.romulus, 20)
        self.romulus_30 = pygame.font.Font(self.romulus, 30)
        self.kenpixel_40 = pygame.font.Font(self.ken_pixel, 40)
        self.kenpixel_80 = pygame.font.Font(self.ken_pixel, 80)
        self.trioDX_10 = pygame.font.Font(self.trioDX, 10)
        self.trioDX_200 = pygame.font.Font(self.trioDX, 200)
        
        #------ Inicializando musicas------#
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

        #------Importando Imagens utilizadas------#

        self.boat_img = pygame.image.load(path.join(img_folder, BOAT_IMG)).convert_alpha()
        self.cannonball_img = pygame.image.load(path.join(img_folder, CANNONBALL_IMG)).convert_alpha()
        self.cracken_img = pygame.image.load(path.join(img_folder, CRACKEN_IMG)).convert_alpha()

        #Carregando imagens de itens:
        self.carne_img=pygame.image.load(path.join(IMG_DIR,MEAT_IMG)).convert_alpha()
        self.rum_img=pygame.image.load(path.join(IMG_DIR,RUM_IMG)).convert_alpha()

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

        #Criando sprites de itens:
        self.Meat1= pygame.sprite.Group()
        self.Meat2= pygame.sprite.Group()
        self.Meat3= pygame.sprite.Group()
        self.Meat4= pygame.sprite.Group()
        self.Rum1= pygame.sprite.Group()
        self.Rum2= pygame.sprite.Group()
        self.Rum3= pygame.sprite.Group()
        self.Rum4= pygame.sprite.Group()

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
            
        #------Camera------#
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False        

    def respawn(self,type): 
        
        #Respawn piratas esquerda:
        if type == 'pirate_l':
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
        if type == 'pirate_r':
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
        if type == 'pirate_t':
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
        if type == 'pirate_b':
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
        if type == 'Meat':
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
        if type == 'Rum':
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
        pygame.mixer.music.play (loops=-1)

    #------Loop do jogo------#

        self.playing = True
        
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0                   # fix for Python 2.x
            self.events()
            self.update()
            self.draw()
    

    #------Criando Tela inicial------#
    def init_screen(self):                                            # Exibe a tela inicial do jogo
        
        self.abertura.play(self.sound_effects['abertura'])
        running = True                                                # Configura o looping
        
        while running:
            
            self.clock.tick(30)
            self.information = False                                  # Alterna exibição
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
                    if event.key == pygame.K_RETURN:                    # Se apertar Enter, entra no Jogo
                        running = False
                        self.Fase1 = True

        self.abertura.stop()

    def update(self):
        
        #Atualiza os elementos gráficos do jogo
        self.all_sprites.update()
        self.camera.update(self.boat)
        
        #Acrescentar condição tempo para mudança de fase
        
        #------Cracken atinge jogador------#
        hits = pygame.sprite.spritecollide(self.boat, self.crackens, False, collide_hit_rect)
        for hit in hits:
            self.boat.health -= CRACKEN_DAMAGE
            hit.vel = vec(0, 0)
            if self.boat.health <= 0:
                self.playing = False
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
                self.boat.pos += vec(-MOB_KNOCKBACK/3, 0)

        hits = pygame.sprite.spritecollide(self.boat, self.pirates_l2, False, collide_hit_rect)    #Colisão barco pirata
        for hit in hits:                                                                           #Verificando se houve colisão                 
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                self.boat.pos += vec(-MOB_KNOCKBACK/3, 0)

        #Piratas Direita:

        hits = pygame.sprite.spritecollide(self.boat, self.pirates_r1, False, collide_hit_rect)    #Colisão barco pirata
        for hit in hits:                                                                           #Verificando se houve colisão                    
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                self.boat.pos += vec(MOB_KNOCKBACK/3, 0)
        
        hits = pygame.sprite.spritecollide(self.boat, self.pirates_r2, False, collide_hit_rect)    #Colisão barco pirata
        for hit in hits:                                                                           #Verificando se houve colisão                                 
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                self.boat.pos += vec(MOB_KNOCKBACK/3, 0)        

        #Piratas Cima:

        hits = pygame.sprite.spritecollide(self.boat, self.pirates_b1, False, collide_hit_rect)   #Colisão barco pirata
        for hit in hits:                                                                          #Verificando se houve colisão 
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                self.boat.pos += vec(0,-MOB_KNOCKBACK/3)
        
        hits = pygame.sprite.spritecollide(self.boat, self.pirates_b2, False, collide_hit_rect)   #Colisão barco pirata
        for hit in hits:                                                                          #Verificando se houve colisão           
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                self.boat.pos += vec(0,-MOB_KNOCKBACK/3)        

        #Piratas Baixo:

        hits = pygame.sprite.spritecollide(self.boat, self.pirates_t1, False, collide_hit_rect)   #Colisão barco pirata
        for hit in hits:                                                                          #Verificando se houve colisão                      
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                self.boat.pos += vec(0,MOB_KNOCKBACK/3)
        
        hits = pygame.sprite.spritecollide(self.boat, self.pirates_t2, False, collide_hit_rect)   #Colisão barco pirata
        for hit in hits:                                                                          #Verificando se houve colisão          
            self.boat.health -= PIRATA_DAMAGE
            hit.vel = vec(0, 0)
            if hits:
                self.boat.pos += vec(0,MOB_KNOCKBACK/3)        

        #------Player colide com Itens------#
        
        #Criando lista para armazenar carne

        lista_carne=[self.Meat1, self.Meat2, self.Meat3, self.Meat4]

        for i in lista_carne:
            
            hits = pygame.sprite.spritecollide (self.boat, i, False, pygame.sprite.collide_mask)
            for hit in hits:
                #self.current_xp += BOAT_XP                       
                hit.kill()
                self.respawn('Meat')

                # aumenta stamina e score
                #self.stamine += BOAT_STAMINA
                #self.score += BOAT_SCORE
                
        #Criando lista para armazenar bebida

        lista_rum=[self.Rum1, self.Rum2, self.Rum3, self.Rum4]

        for i in lista_rum:
            
            hits = pygame.sprite.spritecollide (self.boat, i, False, pygame.sprite.collide_mask)
            for hit in hits:
                #self.current_xp += BOAT_XP                       
                hit.kill()
                self.respawn('Rum')

                # aumenta stamina e score
                #self.stamine += BOAT_STAMINA
                #self.score += BOAT_SCORE
                
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


    def quit(self):

        #Fechar o jogo

        pygame.quit()
        sys.exit()

#------Inicialização------#
jogo= Jogo()

#------Loop Principal-----#

while True:
    
    jogo.init_screen()
    
    while True:
        jogo.new()
        jogo.run()
        

