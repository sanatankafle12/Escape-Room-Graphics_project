import pygame as pg
from settings import *

class ObjectRender:
    def __init__(self,game):
        self.game = game
        self.screen = game.screen
        self.load_wall_textures = self.load_wall_textures()

    def draw(self):
        self.draw_background()
        self.render_game_objects()

    def draw_background(self):
        pg.draw.rect(self.screen,FLOOR_COLOR,(0,HALF_HEIGHT,WIDTH,HEIGHT))

    def render_game_objects(self):
        list_objects = self.game.ray_casting.objects_to_render
        for depth,image,pos in list_objects:
            self.screen.blit(image,pos)

    @staticmethod
    def get_texture(path,res=(TEXTURE_SIZE,TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture,res)
    
    def load_wall_textures(self):
        return{
            1:self.get_texture('textures/wall1.jpg'),
            2:self.get_texture('textures/wall2.jpg'),
        }