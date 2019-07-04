import pygame as pg
from pygame.locals import *
import sys, os
import random

_fps = 60

def between(valor, liminf, limsup):
    return liminf <= valor <= limsup

class Raquet(pg.sprite.Sprite):
    x = 0
    y = 0
    w = 16
    h = 96
    color = (255, 255, 255)
    velocidad = 5
    diry = 1
    sigueA = None
    esComputadora = False

    def __init__(self, objetivo=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((self.w, self.h))
        self.rect = self.image.get_rect()
        self.image.fill(self.color)

        self.sigueA = objetivo
        if self.sigueA:
            self.esComputadora = True

    def setColor(self, color):
        self.color = color
        self.image.fill(self.color)

    def avanza(self):
        self.y += self.diry * self.velocidad

        if self.y <=0:
            self.y = 0
 
        if self.y >= 600 - self.h:
            self.y = 600 - self.h

    def watch(self):
        if self.sigueA:
            if self.sigueA.x <= 400:
                deltaY = self.sigueA.y - self.y
                if deltaY > 0: 
                    self.diry = +1
                elif deltaY < 0:
                    self.diry = -1
                else:
                    self.diry = 0
                self.avanza()

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y





class Ball(pg.sprite.Sprite):
    x = 0
    y = 0
    w = 16
    h = 16
    color = (255, 255, 255)
    velocidad = 5
    dirx = 1
    diry = 1
    cuentatoques = 0

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.getcwd()+"/assets/beach-ball.png")
        self.rect = self.image.get_rect()

        self.ping = pg.mixer.Sound(os.getcwd()+'/assets/ping.wav')
        self.lost = pg.mixer.Sound(os.getcwd()+'/assets/lost-point.wav')

        #self.sound = pg.mixer.Sound(os.getcwd()+'/assets/sonido.aiff')

    '''
    def color(self, valor=None):
        #Actua como getter
        if valor == None:
            return self._color
        #Actua como setter    
        self._color = valor
        self.fill(self._color) 
    '''
    
    def saque(self, ganador):
        self.x = 392
        self.y = 292
        self.diry = random.choice([-1,1])
        self.cuentatoques = 0
        self.velocidad = 5

        self.lost.play()

        if ganador == 1:
            self.dirx = -1
        else:
            self.dirx = 1


    def avanza(self):
        if self.x >= 800:
            self.saque(1)
            return 2

        if self.x <= 0:
            self.saque(2)
            return 1

        if self.y >= 584:
            self.diry = -1
        if self.y <= 0:
            self.diry = 1

        self.x += self.dirx * self.velocidad
        self.y += self.diry * self.velocidad

        return None

    def comprobarChoque(self, spriteGroup):
        if pg.sprite.spritecollide(self, spriteGroup, False):
            self.dirx = self.dirx * -1
            self.x += self.dirx * self.w

            self.ping.play()

            if self.velocidad <= 14:
                self.velocidad += 0.5 

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y






class Game:
    clock = pg.time.Clock()
    pause = False
    puntuaciones = {1: 0, 2: 0}
    winScore = 15
    winner = None

    def __init__(self, width, height):
        self.size = (width, height)
        self.display = pg.display
        self.screen = self.display.set_mode(self.size)
        self.screen.fill((60, 60, 60))
        self.display.set_caption('Mi juego')

        self.allSprites = pg.sprite.Group()
        self.playersGroup = pg.sprite.Group()

        self.ball1 = Ball()

        self.player1 = Raquet()
        self.playersGroup.add(self.player1)
        self.player2 = Raquet(self.ball1)
        self.playersGroup.add(self.player2)
        self.allSprites.add(self.playersGroup)
        self.allSprites.add(self.ball1)

        self.fuente = pg.font.Font(os.getcwd()+'/assets/font.ttf', 48)
        self.iniciopartida()
        
    def iniciopartida(self):
        self.ball1.x = 392
        self.ball1.y = 292
        self.ball1.diry = random.choice([-1,1])
        self.ball1.dirx = random.choice([-1, 1])
        self.ball1.velocidad = random.randrange(5, 11)

        self.player1.x = 768
        self.player1.y = 252

        self.player2.y = 252
        self.player2.x = 16

        self.puntuaciones[1] = 0
        self.puntuaciones[2] = 0

        self.winner = None

        self.marcador1 = self.fuente.render(str(self.puntuaciones[1]), 1, (255, 255, 255))
        self.marcador2 = self.fuente.render(str(self.puntuaciones[2]), 1, (255, 255, 255))


    def gameover(self):
        pg.quit()
        sys.exit()

    def handleevent(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.gameover() 

            # Controlamos pulsaciones de teclas
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.player1.diry = -1
                    self.player1.velocidad = 5
                    self.player1.avanza()

                if event.key == K_DOWN:
                    self.player1.diry = 1
                    self.player1.velocidad = 5
                    self.player1.avanza()

                if event.key == K_q and not self.player2.esComputadora:
                    self.player2.diry = -1
                    self.player2.velocidad = 5
                    self.player2.avanza()

                if event.key == K_a and not self.player2.esComputadora:
                    self.player2.diry = 1
                    self.player2.velocidad = 5
                    self.player2.avanza()

                if event.key == K_SPACE:
                    if self.winner:
                        self.iniciopartida()
                    self.pause = False

            
        # Controlamos teclas mantenidas
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[K_UP]:
            self.player1.diry = -1
            if self.player1.velocidad < 15:
                self.player1.velocidad += 1
            self.player1.avanza()

        if keys_pressed[K_DOWN]:
            self.player1.diry = 1
            if self.player1.velocidad < 15:
                self.player1.velocidad += 1
            self.player1.avanza()                

        if not self.player2.esComputadora:
            if keys_pressed[K_q]:
                self.player2.diry = -1
                if self.player2.velocidad < 15:
                    self.player2.velocidad += 1
                self.player2.avanza()

            if keys_pressed[K_a]:
                self.player2.diry = 1
                if self.player2.velocidad < 15:
                    self.player2.velocidad += 1
                self.player2.avanza()                

        else:
            self.player2.watch()


    def recalculate(self):
        #Modifica la posición de ball y comprueba sus
        if not self.pause:
            p = self.ball1.avanza()
            if p:
                self.pause = True
                self.puntuaciones[p] += 1


                self.marcador1 = self.fuente.render(str(self.puntuaciones[1]), 0, (255, 255, 255))
                self.marcador2 = self.fuente.render(str(self.puntuaciones[2]), 1, (255, 255, 255))

                if self.puntuaciones[1] >= self.winScore or self.puntuaciones[2] >= self.winScore:
                    self.winner = self.fuente.render("Ganador jugador {}".format(p), 1, (255, 255, 0))


        self.ball1.comprobarChoque(self.playersGroup)

    def render(self):
        #Pintar los sprites en screen
        self.screen.fill((60,60,60))

        self.allSprites.update()
        self.allSprites.draw(self.screen)

        #calcular x de marcador 1 para que su derecha sea siempre 784

        self.screen.blit(self.marcador2, (40, 8))
        self.screen.blit(self.marcador1, (760-self.marcador1.get_rect().w, 8))

        if self.winner:
            rect = self.winner.get_rect()
            self.screen.blit(self.winner, ((800 - rect.w)//2, (600 - rect.h) // 2) )

        

        self.display.flip()

    def start(self):
        while True:
            self.clock.tick(_fps)

            self.handleevent()

            self.recalculate()

            self.render()

if __name__ == '__main__':
    pg.init()
    game = Game(800, 600)
    game.start()