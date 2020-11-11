#Definindo classes:
class Boat(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        
        self.groups = game.all_sprites

        #Inicializando construtor:

        pg.sprite.Sprite.__init__(self, self.groups)

   

    