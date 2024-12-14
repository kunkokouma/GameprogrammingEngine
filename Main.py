import pygame
import random
import time
import os
from quadTree import *
from Constants import *
from GameObject import Circle, getRandomCircle

class Main:
    def __init__(self):
        self.done = False
        self.circleList = []
        self.circleMod = True 
        self.quadTreeMode = False
        self.m = 0
        self.f = 0
        pygame.init()
        pygame.display.set_caption('Collision Demo')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.quadTree = QuadTree(0, Bound(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.stars = [(random.randint(1, SCREEN_WIDTH-1), random.randint(1, SCREEN_HEIGHT-1)) for _ in range(300)]

    def resetGameObjects(self):
        self.circleList.clear()

    def loadCircles(self):
        for _ in range(1000):
            circle = getRandomCircle(self.circleList)
            self.circleList.append(circle)

    def run(self):
        while not self.done:
            start_time = time.time()
            if self.m == 0:
                self.m = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        new_circle = getRandomCircle(self.circleList)
                        self.circleList.append(new_circle)
                    elif event.key == pygame.K_d:
                        self.quadTreeMode = not self.quadTreeMode
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        self.done = True
                    elif event.key == pygame.K_r:
                        self.resetGameObjects()
                    elif event.key == pygame.K_1:
                        self.circleMod = True

            self.screen.fill(BLACK)
            for star in self.stars:
                pygame.draw.circle(self.screen, WHITE, star, 1)

            self.quadTree.clear()

            for circle in self.circleList:
                circle.update()
                self.quadTree.insertObject(circle)

            self.quadTree.handleCircleCollision(self.circleList)

            for circle in self.circleList:
                pygame.draw.circle(self.screen, RED, (int(round(circle.cX)), int(round(circle.cY))), circle.cR)

            if self.quadTreeMode:
                for node in self.quadTree.getAllNodes([]):
                    pygame.draw.rect(self.screen, GREEN,
                                     (node.getX(), node.getY(), node.getWidth(), node.getHeight()),
                                     2)

            pygame.display.update()
            cur_time = time.time()
            self.f += 1
            if self.f == FRAME_CAP:
                me = time.time()
                self.m = 0
                self.f = 0
            dif = cur_time - start_time
            delay_required = TPF - dif * 1000
            if delay_required > 0:
                time.sleep(delay_required / 1000)

MainLoop = Main()
MainLoop.loadCircles()
MainLoop.run()
