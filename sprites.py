import pygame
from config import *
vetor=pygame.math.Vector2


# ----- Inicia estruturas de dados (Classes)
class Boat(pygame.sprite.Sprite):
    #Definindo o navio

    def __init__(self, jogo, x, y):
        
        self.groups = game.todos_elementos

        #Inicializando construtor:

        pg.sprite.Sprite.__init__(self, self.groups)
        
        #Configurações gerais
        self.jogo = jogo
        self.image = jogo.boat_img
        self.rect = self.image.get_rect()
        self.boat_width = BOAT_WIDTH
        self.boat_height= BOAT_HEIGHT
        self.rect.center = (x + self.boat_width/2 ,y + self.boat_height/2)
        self.last_update= pygame.time.get_ticks()
        self.pos = vetor(x,y)
        self.dir = vetor(1,0)
        self.vel = vetor(0,0)

        #Movimentações iniciais
    def teclas(self):
        self.vel = vetor(0,0)
        teclas= pygame.key.get_pressed()

        #Movimento para direita
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.vel = vec(PLAYER_SPEED, 0)
            self.dir = vec (1, 0)

        #Movimento para esquerda
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.vel = vec(-PLAYER_SPEED, 0)
            self.dir = vec (-1, 0)

        #Movimento para cima
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.vel = vec(0,-PLAYER_SPEED)
            self.dir = vec (0,-1)
        
        #Movimento para baixo
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.vel = vec(0,PLAYER_SPEED)
            self.dir = vec (0,1)

        self.last_dir = self.dir #guarda última direção escolhida

    #Atualizando para o game
    def update(self):
        self.teclas()
        self.image=pygame.transform.rotate(self.game.boat_img)
        self.rect.center = self.pos

class Cannonball(pygame.sprite.Sprite):
    #definindo a bola de canhão

    def __init__(self,jogo,pos,dir):
        
        self.elementos = jogo.todos_elementos, jogo.cannonballs
        
        #definindo o construtor
        
        pygame.sprite.Sprite.__init__(self,self.elementos)
        self.jogo = jogo
        self.image= jogo.cannonball_img
        self.rect= self.image.get_rect()
        self.pos = vetor(pos)
        self.rect.center = pos

    #Atualizando o trajeto da bala
    def update(self):
        self.rect.center = self.pos



   

    