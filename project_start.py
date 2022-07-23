import pygame as pg 
import sys
from settings import *
from game_map import *
from player import *
from ray_casting import *
from object_render import *

class SoftwareRender:
    def __init__(self):
        pg.init()
        self.HEIGHT, self.WIDTH = 1600,900
        self.H_HEIGHT, self.H_WIDTH = self.HEIGHT//2, self.WIDTH//2
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time  = 1 
        self.new_game()
    
    def draw(self):
        self.screen.fill((172,214,236))
        self.object_render.draw()


    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_render = ObjectRender(self)
        self.ray_casting = RayCasting(self)


    def run(self):   
        self.draw()
        self.player.update()
        self.ray_casting.update()
        pg.display.set_caption("ESCAPE ROOOM!!")
        pg.display.flip()               
        self.delta_time = self.clock.tick(FPS)
