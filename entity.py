# contains classes for player
import pygame as pg
import random


class Enemy:
    def __init__(self, spawn):
        self.SURF = pg.Surface((20, 20))
        self.SURF.fill((98, 20, 137))

        self.rect = self.SURF.get_rect()

        self.hSpeed = 0
        self.vSpeed = 0
        self.mSpeed = 5
        self.moveH = random.randint(-1, 1)
        self.moveV = random.randint(-1, 1)

        self.centX = spawn[0]
        self.centY = spawn[1]

        self.bfr = 0
        self.bullets = []

        self.collide = False

    def run(self, surface):
        self.bfr += 1
        if self.bfr is 60:
            self.bfr = -1
        self.hSpeed = self.moveH * self.mSpeed
        self.vSpeed = self.moveV * self.mSpeed

        self.centX += self.hSpeed
        if self.centX < 200:
            self.moveH = 1
            self.moveV = random.randint(-1, 1)
        elif self.centX > 968:
            self.moveH = -1
            self.moveV = random.randint(-1, 1)

        self.centY += self.vSpeed
        if self.centY < 0:
            self.moveH = random.randint(-1, 1)
            self.moveV = 1
        elif self.centY > 568:
            self.moveH = random.randint(-1, 1)
            self.moveV = -1

        self.rect.x = self.centX
        self.rect.y = self.centY

        if self.bfr is 0:
            self.bullets.append(BulletE(self.centX, self.centY))

        for bullet in self.bullets:
            if bullet.collide:
                self.bullets.remove(bullet)

            bullet.fire(surface)

        surface.blit(self.SURF, [self.centX, self.centY])


class BulletE:
    def __init__(self, x, y):
        self.SURF = pg.Surface((10, 4))
        self.SURF.fill((255, 0, 0))
        self.rect = self.SURF.get_rect()

        self.mSpeed = 10
        self.centX = x
        self.centY = y + 8
        self.collide = False

    def fire(self, surface):
        surface.blit(self.SURF, [self.centX, self.centY])
        self.centX -= self.mSpeed

        self.rect.x = self.centX
        self.rect.y = self.centY

        if self.centX < 0:
            self.collide = True


class Player:
    def __init__(self):
        self.SURF = pg.Surface((32, 32))
        self.SURF.fill((255, 255, 0))
        self.barSurf = pg.Surface((200, 10))
        self.barSurf.fill((255, 255, 0))
        self.barProg = pg.Surface((200, 10))
        self.barProg.fill((0, 0, 255))

        self.rect = self.SURF.get_rect()
        self.rect.x = 100
        self.rect.y = 290

        self.hSpeed = 0
        self.vSpeed = 0
        self.mSpeed = 8

        self.centX = 100
        self.centY = 290

        self.shieldT = 500
        self.shield = False
        self.collide = False

    def run(self, keyList):
        # 0 keyUp, 1 keyDown, 2 keyLeft, 3 keyRight, 4 keyShield
        moveH = keyList[2] + keyList[3]
        moveV = keyList[0] + keyList[1]

        self.hSpeed = moveH * self.mSpeed
        self.vSpeed = moveV * self.mSpeed

        self.centX += self.hSpeed
        if self.centX < 0:
            self.centX = 0
        elif self.centX > 600:
            self.centX = 600

        self.centY += self.vSpeed
        if self.centY < 0:
            self.centY = 0
        elif self.centY > 568:
            self.centY = 568

        self.rect.x = self.centX
        self.rect.y = self.centY

        if self.shieldT <= 500:
            self.barProg = pg.Surface((int(self.shieldT*200/500), 10))
            self.barProg.fill((0, 0, 255))
            self.shieldT += 1

        if self.shield:
            if self.shieldT > 60:
                self.shield = False
                self.SURF.fill((255, 255, 0))
            elif self.shieldT > 55:
                self.SURF.fill((0, 0, 255))
            elif self.shieldT > 50:
                self.SURF.fill((255, 255, 0))
            elif self.shieldT > 40:
                self.SURF.fill((0, 0, 255))
            elif self.shieldT > 35:
                self.SURF.fill((255, 255, 0))

        if keyList[4]:
            if not self.shield and self.shieldT >= 500:
                self.shield = True
                self.shieldT = 0
                self.SURF.fill((0, 0, 255))

    def draw(self, surface):
        surface.blit(self.SURF, [self.centX, self.centY])
        surface.blit(self.barSurf, [250, 15])
        surface.blit(self.barProg, [250, 15])


class BulletP:
    def __init__(self, x, y):
        self.SURF = pg.Surface((10, 4))
        self.SURF.fill((0, 255, 0))
        self.rect = self.SURF.get_rect()

        self.mSpeed = 20
        self.centX = x + 22
        self.centY = y + 15
        self.collide = False

    def fire(self, surface):
        surface.blit(self.SURF, [self.centX, self.centY])
        self.centX += self.mSpeed

        self.rect.x = self.centX
        self.rect.y = self.centY

        if self.centX > 1000:
            self.collide = True
