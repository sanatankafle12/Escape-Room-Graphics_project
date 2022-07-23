from math import tan, pi
import utils.vector as vector
from utils.matrix import Matrix
import settings
import pygame

class Camera:
    def __init__(self, position, near, far, fov):
        self.position = position
        self.near = near
        self.far = far
        self.fov = fov
        self.yaw = 0
        self.phi = 0
        self.tangent = 1.0 / tan(self.fov * 0.5 / 180 * pi)
        self.direction = vector.Vector3()
        self.up = vector.Vector3()
        self.transform = Matrix.identity()
        self.target = position
        self.speed = 0.1
        self.rotationSpeed = 1.5
        self.temp = vector.Vector3()

    def HandleInput(self, dt):
        keys = pygame.key.get_pressed()
        delta = self.speed * dt
        
        if keys[pygame.K_m]:
            self.position.y += delta
        if keys[pygame.K_n]:
            self.position.y -= delta
        if keys[pygame.K_b]:
            self.position.x -= delta
        if keys[pygame.K_v]:
            self.position.x += delta

        self.temp = self.target * delta

        if keys[pygame.K_k]: #zoom in
            self.position += self.temp
        if keys[pygame.K_l]: #zoom out
            self.position -= self.temp
        if keys[pygame.K_o]:
            self.yaw -= 0.04
        if keys[pygame.K_i]:
            self.yaw += 0.04
        
    def projection(self) -> Matrix:
        matrix = Matrix()
        matrix.val = [
            [settings.aspect * self.tangent, 0.0, 0.0, 0.0],
            [0.0, self.tangent, 0.0, 0.0],
            [0.0, 0.0, self.far / (self.far - self.near), 1],
            [0.0, 0.0, (-self.far * self.near) / (self.far - self.near), 0.0],
        ]
        return matrix
