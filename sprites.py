import pygame
from random import *
from config import *
vec = pygame.math.Vector2

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
        
        #Vetor posição
        self.pos = vec(x,y)
        #Vetor direção
        self.dir = vec(x,y)
        #Vetor velocidade
        self.vel = vec(0,0)

        #Pegando a ultima direção e tiro
        self.last_dir = self.dir
        self.last_shot = 0

        #Controle e direção:
    
        self.esquerda = ""
        self.direita = ""
        self.cima = ""
        self.baixo = ""

        #Movimentações iniciais
    def teclas(self):
        
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel = vec(-BOAT_SPEED, 0)
            self.dir = vec (-1, 0)
            self.esquerda = "esquerda"
            self.direita = ""
            self.cima = ""
            self.baixo = ""
            

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel = vec(BOAT_SPEED, 0)
            self.dir = vec (1, 0)
            self.esquerda = ""
            self.direita = "direita"
            self.cima = ""
            self.baixo = ""

        
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel = vec(0,-BOAT_SPEED)
            self.dir = vec (0,-1)
            self.esquerda = ""
            self.direita = ""
            self.cima = "cima"
            self.baixo = ""

        
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel = vec(0,BOAT_SPEED)
            self.dir = vec (0,1)
            self.esquerda = ""
            self.direita = ""
            self.cima = ""
            self.baixo= "baixo"
 
        
        else:
            self.cima = ""
            self.baixo = ""
            self.esquerda = ""
            self.direita = ""
        self.last_dir = self.dir # guarda última direção

        if keys[pygame.K_SPACE]:
            
            now=pygame.time.get_ticks()
            
            #Verificando se o tempo passado já é maior que o intervalo estipulado entre um tiro e outro:

            if now - self.last_shot > dt_shot: 
                self.last_shot = now # se passou tempo mínimo, grava novo 'último tiro'
                self.charge = 0
                
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
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.jogo.dt

        #Falta configurações de colisão    

        now = pygame.time.get_ticks()
        delta_t = now - self.last_update

        if self.esquerda == "esquerda":
            self.image = self.jogo.boat_left['D0 (3).png']
            self.image = pygame.transform.scale(self.image, (self.boat_width, self.boat_height))

        # Direita
        elif self.direita == "direita":
            self.image = self.jogo.boat_right['Navio.png']
            self.image = pygame.transform.scale(self.image, (self.boat_width, self.boat_height))

        # Baixo
        elif self.baixo == "baixo":
            self.image = self.jogo.boat_down['D0 (2).png']
            self.image = pygame.transform.scale(self.image, (self.boat_width, self.boat_height))

        # Cima
        elif self.cima == "cima":
            self.image = self.jogo.boat_up['D0 (1).png']
            self.image = pygame.transform.scale(self.image, (self.boat_width, self.boat_height))

class Cannonball(pygame.sprite.Sprite):
    #definindo a bola de canhão

    def __init__(self,jogo,pos,dir):
        
        self.elementos = jogo.todos_elementos, jogo.cannonballs
        
        #Definindo o construtor
        pygame.sprite.Sprite.__init__(self,self.elementos)
        
        self.jogo = jogo
        self.image= jogo.cannonball_img
        self.rect= self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos

        #Definindo velocidade:
        propg = uniform(-CANNONBALL_PROPG, 0)
        self.vel = dir.rotate(propg) * CANNONBALL_SPEED

        #Controlando tempo de aparição:
        self.tempo_spaw = pygame.time.get_ticks()

    #Atualizando o trajeto da bala
    def update(self):
        self.pos += self.vel * self.jogo.dt
        self.rect.center = self.pos

        #FALTA ACRESCENTAR CONDIÇÃO DE COLISÃO
        #Condição para que a bala sumir após determindado tempo:
        if pygame.time.get_ticks() - self.spawn_time > CANNONBALL_LIFETIME: 
            self.kill()

class Ilhas (pygame.sprite.Sprite):
        def __init__(self, jogo, x, y):
        
            self.groups = jogo.todos_elementos, jogo.Ilhas
       
            #Definindo construtor:
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.jogo = jogo

            #FALTA COMPLEMENTO
        pass


   

    