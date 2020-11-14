import pygame
from config import *
vetor=pygame.math.Vector2


# ----- Inicia estruturas de dados (Classes)
class Boat(pygame.sprite.Sprite):
    #Definindo o navio

    def __init__(self, jogo, x, y):
        
        self.groups = jogo.todos_elementos

        #Inicializando construtor:

        pygame.sprite.Sprite.__init__(self, self.groups)
        
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

        #Controle e direção:
    
        self.LEFT = False
        self.RIGHT = False
        self.UP = False
        self.DOWN = False

        #Movimentações iniciais
    def teclas(self):
        self.vel = vetor(0,0)

        #Verificando aquelas teclas que foram apertadas:
        teclas= pygame.key.get_pressed()

        #Movimento para direita
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.vel = vec(BOAT_SPEED, 0)
            self.dir = vec (1, 0)

            #Atualizando lista de teclas apertadas:

            self.LEFT = False
            self.RIGHT = True
            self.UP = False
            self.DOWN = False           

        #Movimento para esquerda
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.vel = vec(-BOAT_SPEED, 0)
            self.dir = vec (-1, 0)
            
            #Atualizando lista de teclas apertadas:
            
            self.LEFT = True
            self.RIGHT = False
            self.UP = False
            self.DOWN = False
        
        #Movimento para cima
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.vel = vec(0,-BOAT_SPEED)
            self.dir = vec (0,-1)

            #Atualizando lista de teclas apertadas:

            self.LEFT = False
            self.RIGHT = False
            self.UP = True
            self.DOWN = False            
        
        #Movimento para baixo
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.vel = vec(0,BOAT_SPEED)
            self.dir = vec (0,1)

            #Atualizando lista de teclas apertadas:

            self.LEFT = False
            self.RIGHT = False
            self.UP = False
            self.DOWN = True

        self.last_dir = self.dir #guarda última direção escolhida

        if keys[pg.K_SPACE]:
            
            now=pygame.time.get_ticks()
            
            #Verificando se o tempo passado já é maior que o intervalo estipulado entre um tiro e outro:

            if now - self.last_shot > dt_shot: 
                self.last_shot = now # se passou tempo mínimo, grava novo 'último tiro'
                self.charge = 0
                
                # Ajusta posição do disparo dependendo da movimentação que o navio estava
                if self.LEFT:
                    pos = self.pos + vec(-self.rect.width/2, 0)
                elif self.RIGHT:
                    pos = self.pos + vec(self.rect.width, 0)
                elif self.UP:
                    pos = self.pos + vec(0, -self.rect.height)
                elif self.DOWN:
                    pos = self.pos + vec(0, self.rect.height)
                else:
                    # Ajusta posição do bala de canhão quando o navio está parado
                    if self.last_dir == vec (1, 0):
                        pos = self.pos + vec(self.rect.width, 0)            
                    elif self.last_dir == vec (-1, 0):
                        pos = self.pos + vec(-self.rect.width/2, 0)           
                    elif self.last_dir == vec (0, -1):
                        pos = self.pos + vec(0, -self.rect.height)          
                    else: 
                        pos = self.pos + vec(0, self.rect.height)        

                dir = self.last_dir                  # "Pegando" última direção
                Cannonball(self.jogo, pos, dir)
                self.vel = vec(BOAT_KICKBACK, 0)
        
        dir = self.last_dir  
        # Pequeno impulso para trás do disparo

    #Atualizando para o jogo
    def update(self):
        self.teclas()
        self.image=pygame.transform.rotate(self.jogo.boat_img)
        self.rect.center = self.pos

class Cannonball(pygame.sprite.Sprite):
    #definindo a bola de canhão

    def __init__(self,jogo,pos,dir):
        
        self.elementos = jogo.todos_elementos, jogo.cannonballs
        
        #Definindo o construtor
        pygame.sprite.Sprite.__init__(self,self.elementos)
        
        self.jogo = jogo
        self.image= jogo.cannonball_img
        self.rect= self.image.get_rect()
        self.pos = vetor(pos)
        self.rect.center = pos

        #Definindo velocidade:
        propg = uniform(-CANNONBALL_PROPG, CANNONBALL_PROPG)
        self.vel = dir.rotate(propg) * CANNONBALL_SPEED

    #Atualizando o trajeto da bala
    def update(self):
        self.rect.center = self.pos





   

    