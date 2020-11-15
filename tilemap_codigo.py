import pygame as pg
import pytmx
from config import *

class TiledMap:

    #Configurações gerais da classe:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    #Renderizando o mapa
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        #Criando superfície onde o mapa será desenhado:
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    
    #Configurações gerais da classe:
    def __init__(self, width, height):
        
        #Fazendo retângulo:
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):

        #Posicionando câmera com alvo (jogador):

        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # Limite de scrolling do mapa:

        x = min(0, x)                         # Esquerda
        y = min(0, y)                         # Topo
        x = max(-(self.width - WIDTH), x)     # Direita
        y = max(-(self.height - HEIGHT), y)   # Base
        
        self.camera = pg.Rect(x, y, self.width, self.height)