# subscribe to my youtube
# https://www.youtube.com/c/Auctux
import sys
import pygame
from pygame.locals import *
from settings import *
from event import HandleEvent
from utils.vector import Vector3
from utils.camera import Camera
from utils.light import Light
from utils.mesh.base import Mesh
from utils.mesh.meshes import *
from utils.matrix import *
from utils.tools import *
from utils.world import Scene
from project_start import *

pygame.init()
flags = DOUBLEBUF
screen = pygame.display.set_mode(RES, flags, 16)
clock = pygame.time.Clock()

fps = 60


# cube = Mesh()
# cube.triangles = CubeTriangles((225,225,84))
# cube.position = Vector3(3, 0, 0)

# cube1 = Mesh()
# cube1.triangles = CubeTriangles((225,200,84))
# cube1.position = Vector3(-3, 0, 0)

player = Mesh()
player.triangles = LoadMesh("assets/player.obj", (255, 255, 0))
player.position = Vector3(5,-10,-5)


scene = Scene()
# scene.world.append(cube)
# scene.world.append(cube1)
scene.world.append(player)
#camera setup
camera = Camera(Vector3(0, 0, 0), 0.1, 100.0, 75.0)
camera.speed = 0.5
camera.rotationSpeed = 0.8

#light setup
light = Light(Vector3(-3, 2, -10))
hue = 0

angle = 0
moveLight = True
run = True
app = SoftwareRender()
while run:
    clock.tick(FPS)
    app.delta_time = clock.tick(FPS)
    app.draw()
    app.player.update()
    app.ray_casting.update()
    dt = clock.tick(fps)/100
    frameRate = clock.get_fps()
    run = HandleEvent(camera, dt)
    hue = 0
    #handle input
    camera.HandleInput(dt)
    if moveLight == True and light != None:
        mx, my = pygame.mouse.get_pos()
        _x = translateValue( mx, 0,  WIDTH,  -1,  1)
        _y = translateValue( my, 0, HEIGHT, -1, 1)    
        light = Light(Vector3(_x, -_y, -1))


    # apply the transformation matrix here
    # cube.transform = Matrix.scaling(0.5)@Matrix.rotation_x(angle)
    # cube1.transform =Matrix.scaling(2)
    # player.transform = Matrix.scaling(3)
    scene.update(
        dt = dt,
        camera=camera,
        light=light,
        screen=screen,
        fill=True,
        wireframe=False,
        vertices=False,
        depth=True,
        clippingDebug=False,
        showNormals=False,
        radius=9,
        verticeColor=False,
        wireframeColor=(255, 255, 255),
        ChangingColor=hue)
    pygame.display.flip()
    angle += 0.01

pygame.quit()
sys.exit()
