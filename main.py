import pygame as pg
from pygame.locals import *
import sys
import random

_fps = 60

class Ball(pg.Surface):
    x = 0
    y = 0
    color = (255, 255, 255)
    velocidad = 5
    dirx = velocidad
    diry = velocidad

    def __init__(self):
        pg.Surface.__init__(self, (16,16))
        self.fill(self.color)

    def setColor(self, color):
        self.color = color
        self.fill(self.color)

    def avanza(self):
        if self.x >= 800:
            self.dirx = -self.velocidad
        if self.x <= 0:
            self.dirx = self.velocidad
        if self.y >= 600:
            self.diry = -self.velocidad
        if self.y <= 0:
            self.diry = self.velocidad

        self.x += self.dirx
        self.y += self.diry

class Game:
    clock = pg.time.Clock()

    def __init__(self, width, height):
        self.size = (width, height)
        self.display = pg.display
        self.screen = self.display.set_mode(self.size)
        self.screen.fill((60, 60, 60))
        self.display.set_caption('Mi juego')

        self.balls = []

        for i in range(5, 15):
            b = Ball()
            b.setColor((random.randrange(256), random.randrange(256), random.randrange(256)))
            b.x = random.randrange(800)
            b.y = random.randrange(600)
            b.velocidad = random.randrange(10)

            self.balls.append(b)


        '''
        self.ball = Ball()
        #self.ball.velocidad = 1
        self.ball1 = Ball()
        self.ball1.setColor((255,0,0))
        self.ball1.x = 392
        self.ball1.y = 292
        self.ball1.velocidad = 10
        '''
        



    def start(self):
        while True:
            self.clock.tick(_fps)

            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

            #Modifica la posición de ball
            for ball in self.balls:
                ball.avanza()

            '''
            self.ball.avanza()
            self.ball1.avanza()
            '''

            #Pintar los sprites en screen
            self.screen.fill((60,60,60))
            for i in range(5):
                self.screen.blit(self.balls[i], (self.balls[i].x, self.balls[i].y))

            for ball in self.balls:
                self.screen.blit(ball, (ball.x, ball.y))

            '''    
            self.screen.blit(self.ball1, (self.ball1.x, self.ball1.y))
            self.screen.blit(self.ball, (self.ball.x, self.ball.y))
            '''


            self.display.flip()

if __name__ == '__main__':
    pg.init()
    game = Game(800, 600)
    game.start()