import pygame
from random import *
from config import *
from tilemap_codigo import *
vec = pygame.math.Vector2

# ----- Inicia estruturas de dados (Classes)
class Boat(pygame.sprite.Sprite):
    #Definindo o navio

    def __init__(self, jogo, x, y):
        
        self.groups = jogo.all_sprites

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
        
        #hits tomados
        self.hit_rect = BOAT_HIT_RECT

        #vida do barco
        self.health = BOAT_HEALTH

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
                channel2=self.jogo.sound_effects['cannonball'].play()  
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
        self.last_dir = self.dir
        dir = self.last_dir  
        # Pequeno impulso para trás do disparo

    #Atualizando para o jogo
    def update(self):
        self.teclas()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.jogo.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_ilhas(self, self.jogo.ilhas, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_ilhas(self, self.jogo.ilhas, 'y')
        self.rect.center = self.hit_rect.center

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

class Cracken(pygame.sprite.Sprite):
    def __init__(self, jogo, x, y):
        self.groups = jogo.all_sprites, jogo.crackens
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
        self.image = jogo.cracken_img
        self.rect = self.image.get_rect()
        self.hit_rect = CRACKEN_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = CRACKEN_HEALTH
        self.speed = choice(CRACKEN_SPEEDS)

    def avoid_mobs(self):
        for mob in self.jogo.crackens:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.rot = (self.jogo.boat.pos - self.pos).angle_to(vec(1, 0))
        self.image = pygame.transform.rotate(self.jogo.cracken_img, self.rot)
        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.jogo.dt
        self.pos += self.vel * self.jogo.dt + 0.5 * self.acc * self.jogo.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_ilhas(self, self.jogo.ilhas, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_ilhas(self, self.jogo.ilhas, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / CRACKEN_HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 7)
        if self.health < CRACKEN_HEALTH:
            pygame.draw.rect(self.image, col, self.health_bar)

class Cannonball(pygame.sprite.Sprite):
    #definindo a bola de canhão

    def __init__(self,jogo,pos,dir):
        
        self.elementos = jogo.all_sprites, jogo.cannonball
        
        #Definindo o construtor
        pygame.sprite.Sprite.__init__(self,self.elementos)
        
        self.jogo = jogo
        self.image= jogo.cannonball_img
        self.rect= self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.hit_rect = self.rect

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
        if pygame.sprite.spritecollideany(self, self.jogo.ilhas):
            self.kill()
        #Condição para que a bala sumir após determindado tempo:

        if pygame.time.get_ticks() - self.tempo_spaw  > CANNONBALL_LIFETIME: 
            self.kill()

class Ilhas (pygame.sprite.Sprite):
        def __init__(self, jogo, x, y):
        
            self.groups = jogo.all_sprites, jogo.ilhas
            
            #Definindo construtor:
            pygame.sprite.Sprite.__init__(self, self.groups)
            self.jogo = jogo
            self.rect = self.image.get_rect()
            self.x = x
            self.y = y
            self.rect.x = x * TILESIZE
            self.rect.y = y * TILESIZE

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, jogo, x, y, w, h):
        self.groups = jogo.ilhas
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.jogo = jogo
        self.rect = pygame.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Pirata_esquerda(pygame.sprite.Sprite):
    def __init__(self,jogo,img,x,y):
        self.groups = jogo.all_sprites, jogo.pirates
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.jogo=jogo
        self.image = img
        self.rect = self.image.get_rect()
        self.hit_rect = PIRATA_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.dir = vec(-1,0)
        self.speed= PIRATA_SPEED
        self.vel = self.dir *self.speed
        self.last_position = vec(x,y)
        self.health =PIRATA_HEALTH
        self.distance = vec(0,0)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        delta_t = now -self.last_update
        self.vel = self.dir *self.speed
        self.pos += self.vel* self.jogo.dt
        self.rect.center = self.pos
        self.hit_rect.centerx= self.pos.x
        collide_with_ilhas(self, self.jogo.ilhas, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_ilhas(self, self.jogo.ilhas, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
    
    def draw_health(self):
        if self.health > 15:
            col = GREEN
        elif self.health > 10:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / PIRATA_HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 6)
        if self.health < PIRATA_HEALTH:
            pygame.draw.rect(self.image, col, self.health_bar)

        distance = self.pos - self.last_position
        #D = distance.length()
        #if D>=WIDTH:
            #self.kill()

class Pirata_direita(pygame.sprite.Sprite):
    def __init__(self,jogo,img,x,y):
        self.groups = jogo.all_sprites, jogo.pirates
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.jogo=jogo
        self.image = img
        self.rect = self.image.get_rect()
        self.hit_rect = PIRATA_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.dir = vec(1,0)
        self.speed= PIRATA_SPEED
        self.vel = self.dir *self.speed
        self.last_position = vec(x,y)
        self.distance = vec(0,0)
        self.health =PIRATA_HEALTH
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        delta_t = now -self.last_update
        self.vel = self.dir *self.speed
        self.pos += self.vel* self.jogo.dt
        self.rect.center = self.pos
        self.hit_rect.centerx= self.pos.x
        collide_with_ilhas(self, self.jogo.ilhas, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_ilhas(self, self.jogo.ilhas, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
    
    def draw_health(self):
        if self.health > 15:
            col = GREEN
        elif self.health > 10:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / PIRATA_HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 6)
        if self.health < PIRATA_HEALTH:
            pygame.draw.rect(self.image, col, self.health_bar)

        distance = self.pos - self.last_position
        #D = distance.length()
        #if D>=WIDTH:
            #self.kill()

class Pirata_cima(pygame.sprite.Sprite):
    def __init__(self,jogo,img,x,y):
        self.groups = jogo.all_sprites, jogo.pirates
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.jogo=jogo
        self.image = img
        self.rect = self.image.get_rect()
        self.hit_rect = PIRATA_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.dir = vec(0,-1)
        self.speed= PIRATA_SPEED
        self.vel = self.dir *self.speed
        self.last_position = vec(x,y)
        self.distance = vec(0,0)
        self.health =PIRATA_HEALTH
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        delta_t = now -self.last_update
        self.vel = self.dir *self.speed
        self.pos += self.vel* self.jogo.dt
        self.rect.center = self.pos
        self.hit_rect.centerx= self.pos.x
        collide_with_ilhas(self, self.jogo.ilhas, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_ilhas(self, self.jogo.ilhas, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
    
    def draw_health(self):
        if self.health > 15:
            col = GREEN
        elif self.health > 10:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / PIRATA_HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 6)
        if self.health < PIRATA_HEALTH:
            pygame.draw.rect(self.image, col, self.health_bar)


        distance = self.pos - self.last_position
        #D = distance.length()
        #if D>=WIDTH:
            #self.kill()

class Pirata_baixo(pygame.sprite.Sprite):
    def __init__(self,jogo,img,x,y):
        self.groups = jogo.all_sprites, jogo.pirates
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.jogo = jogo
        self.image = img
        self.rect = self.image.get_rect()
        self.hit_rect = PIRATA_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x,y)
        self.rect.center = self.pos
        self.dir = vec(0,1)
        self.speed= PIRATA_SPEED
        self.vel = self.dir *self.speed
        self.last_position = vec(x,y)
        self.distance = vec(0,0)
        self.health =PIRATA_HEALTH
        self.last_update = pygame.time.get_ticks()


    def update(self):
        now = pygame.time.get_ticks()
        delta_t = now -self.last_update
        self.vel = self.dir *self.speed
        self.pos += self.vel* self.jogo.dt
        self.rect.center = self.pos
        self.hit_rect.centerx= self.pos.x
        collide_with_ilhas(self, self.jogo.ilhas, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_ilhas(self, self.jogo.ilhas, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
    
    def draw_health(self):
        if self.health > 15:
            col = GREEN
        elif self.health > 10:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / PIRATA_HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 6)
        if self.health < PIRATA_HEALTH:
            pygame.draw.rect(self.image, col, self.health_bar)
        distance = self.pos - self.last_position
        #D = distance.length()
        #if D>=WIDTH:
            #self.kill()

    #Barra de vida do barco
def draw_boat_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


   

    