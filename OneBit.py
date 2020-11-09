""" 
ONEBIT GAME!

Jogo criado por: Leticia Coêlho Barbosa e Matheus Silva
na disciplina de Design de Software

Professor orientador: Luciano Soares,
1A- ENG
INSPER 2020.2

Créditos no arquivo README.md
"""

# ===== Inicialização =====
# ----- Importa e inicia pacotes

import pygame

pygame.init()

#----- Gera tela inicial

WIDTH = 700
HEIGHT = 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('OneBit Game')

# ----- Inicia assets
BOAT_WIDTH = 50
BOAT_HEIGHT = 38

CANNONBALL_WIDTH=20
CANNONBALL_HEIGHT=10

font = pygame.font.SysFont(None, 48)

#Criando dicionario assets:

assets={}

#Carregando imagens:
map_init = pygame.image.load('../Imagens/Fundoinicial.jpg').convert()  
boat_img = pygame.image.load('../Imagens/navio_inicial.png').convert_alpha()
cannonball_img = pygame.image.load('../Imagens/balacanhao_1.png').convert_alpha()

#Redimensionando:

assets['map_init'] = pygame.transform.scale(map_inicial,(WIDTH,HEIGHT))
assets['boat_img'] = pygame.transform.scale(boat_img, (BOAT_WIDTH, BOAT_HEIGHT))
assets['cannonball_img'] = pygame.transform.scale(cannonball_img, (CANNONBALL_WIDTH,CANNONBALL_HEIGHT))

# ----- Inicia estruturas de dados (Classes)

class Boat(pygame.sprite.Sprite):
    def __init__(self, assets):
        
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['boat_img']
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT/2
        self.assets=assets

    def shoot (self):
        pass

    def update(self):
        pass

class Cannonball(pygame.sprite.Sprite):
    def __init__(self, assets):
        
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)   

        self.image = assets['cannonball_img']
        self.rect = self.image.get_rect()

    def update(self):
        pass

game = True

# ===== Loop principal =====
while game:



# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados