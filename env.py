import os
import random
import numpy as np
import pygame as pg
import entity

# folders probably won't use but ok
mainFolder = os.path.dirname(__file__)


# init values
class Env:
    def __init__(self):
        self.player = entity.Player()
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.reward = 0
        self.hiScore = 0
        self.bfr = -1  # bullet fire rate
        self.enemyMax = 10  # max number of self.enemies
        self.esr = -1  # enemy spawn rate
        self.efr = -1  # enemy fire rate
        self.time = 0  # play self.time in seconds
        self.done = False
        self.GAME_SURFACE = pg.display.set_mode((1000, 600))
        random.seed(None)

    def get_state(self):
        state = np.empty(83)
        state[0] = self.player.centX / 600
        state[1] = self.player.centY / 600
        state[2] = self.player.shieldT / 500
        count = 3
        for i in range(10):
            if i < len(self.enemies):
                state[count] = self.enemies[i].centX / 1000
                state[count + 1] = self.enemies[i].centY / 600
                state[count + 2] = self.enemies[i].moveH
                state[count + 3] = self.enemies[i].moveV
                count += 4
                if len(self.enemies[i].bullets) == 0:
                    state[count] = 0
                    state[count + 1] = 0
                    state[count + 2] = 0
                    state[count + 3] = 0
                elif len(self.enemies[i].bullets) == 1:
                    state[count] = self.enemies[i].bullets[0].centX / 1000
                    state[count + 1] = self.enemies[i].bullets[0].centY / 600
                    state[count + 2] = 0
                    state[count + 3] = 0
                else:
                    state[count] = self.enemies[i].bullets[0].centX / 1000
                    state[count + 1] = self.enemies[i].bullets[0].centY / 600
                    state[count + 2] = self.enemies[i].bullets[1].centX / 1000
                    state[count + 3] = self.enemies[i].bullets[1].centY / 600

                count += 4

            else:
                state[count] = 0
                state[count + 1] = 0
                state[count + 2] = 0
                state[count + 3] = 0
                state[count + 4] = 0
                state[count + 5] = 0
                state[count + 6] = 0
                state[count + 7] = 0
                count += 8

        return state.reshape((1, 83))

    def reset(self):
        self.player = entity.Player()
        self.bullets = []
        self.enemies = []
        self.score = 0
        self.reward = 0
        self.bfr = -1  # bullet fire rate
        self.enemyMax = 10  # max number of self.enemies
        self.esr = -1  # enemy spawn rate
        self.efr = -1  # enemy fire rate
        self.time = 0  # play self.time in seconds
        self.done = False

        return self.get_state()

    # main game loop
    def step(self, action):
        # 0 keyUp, 1 keyDown, 2 keyLeft, 3 keyRight, 4 keyShield, 5 keyPause

        self.player.run(action)

        self.time += 1
        self.reward = 0

        # fires self.bullets every 0.5s (fps is 30 and this fires every 15 iterations)
        self.bfr += 1
        if self.bfr is 0:
            self.bullets.append(entity.BulletP(self.player.centX, self.player.centY))
        elif self.bfr is 15:
            self.bfr = -1

        for bullet in self.bullets:
            if bullet.collide:
                self.bullets.remove(bullet)

            bullet.fire(self.GAME_SURFACE)

        # enemy spawn
        self.esr += 1
        if self.esr is 0 and len(self.enemies) < self.enemyMax:
            self.enemies.append(entity.Enemy([random.randint(200, 1000), random.randint(0, 600)]))
        elif self.esr is 30:
            self.esr = -1

        # collision detection part
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                if not self.player.shield:
                    self.player.collide = True
                enemy.collide = True
            for bullet in self.bullets:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.collide = True
                    bullet.collide = True
            for bullet in enemy.bullets:
                if bullet.rect.colliderect(self.player.rect):
                    if not self.player.shield:
                        self.player.collide = True
                    bullet.collide = True

            if enemy.collide:
                self.enemies.remove(enemy)
                self.score += 1
                self.reward += 50

            enemy.run(self.GAME_SURFACE)

        self.player.draw(self.GAME_SURFACE)

        if self.time > 600 and self.score < 8:
            self.player.collide = True

        if self.player.collide:
            self.reward = -100
            self.done = True
            if self.score > self.hiScore:
                self.hiScore = self.score

        return self.get_state(), self.reward, self.done
