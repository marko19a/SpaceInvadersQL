import os
import sys
import entity
import random
import pygame as pg
import userControl as uc
import networkModel as model
import numpy as np

# initialize pygame
pg.init()
pg.mixer.init()

# folders probably won't use but ok
mainFolder = os.path.dirname(__file__)

# Settings

GAME_TITLE = 'SpaceInvaders'

WIDTH = 1000
HEIGHT = 600
FPS = 30

clock = pg.time.Clock()

pg.display.set_caption(GAME_TITLE)
GAME_SURFACE = pg.display.set_mode((WIDTH, HEIGHT))

# Color stuff

font = pg.font.SysFont('arial', 18)


class Pallet:
    def __init__(self):
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)


# exits game
def leave():
    pg.quit()
    sys.exit(0)


def drawText(x, y, text):
    txt = font.render(str(text), True, (200, 200, 200))
    GAME_SURFACE.blit(txt, (x, y))


# init values
col = Pallet()
user = uc.Interactor()
player = entity.Player()
bullets = []
enemies = []
score = 0
reward = 0
hiScore = 0
bfr = -1  # bullet fire rate
enemyMax = 10  # max number of enemies
esr = -1  # enemy spawn rate
efr = -1  # enemy fire rate
time = 0  # play time in seconds
random.seed(None)
agent = model.DQNAgent(83, 5)
agent.load('checkPoint0.h5')
batch_size = 60


def get_state():
    state = np.empty(83)
    state[0] = player.centX / 600
    state[1] = player.centY / 600
    state[2] = player.shieldT / 500
    count = 3
    for i in range(10):
        if i < len(enemies):
            state[count] = enemies[i].centX / 1000
            state[count + 1] = enemies[i].centY / 600
            state[count + 2] = enemies[i].moveH
            state[count + 3] = enemies[i].moveV
            count += 4
            if len(enemies[i].bullets) == 0:
                state[count] = 0
                state[count + 1] = 0
                state[count + 2] = 0
                state[count + 3] = 0
            elif len(enemies[i].bullets) == 1:
                state[count] = enemies[i].bullets[0].centX / 1000
                state[count + 1] = enemies[i].bullets[0].centY / 600
                state[count + 2] = 0
                state[count + 3] = 0
            else:
                state[count] = enemies[i].bullets[0].centX / 1000
                state[count + 1] = enemies[i].bullets[0].centY / 600
                state[count + 2] = enemies[i].bullets[1].centX / 1000
                state[count + 3] = enemies[i].bullets[1].centY / 600

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


# main game loop
while user.running:
    clock.tick(FPS)

    # keyInput = user.run() # returns list with inputs (no need to use variable)
    # 0 keyUp, 1 keyDown, 2 keyLeft, 3 keyRight, 4 keyShield, 5 keyPause
    state = get_state()
    action = agent.model.predict(state)  # agent acting
    move = np.zeros(5)
    move[np.argmax(move[0])] = 1
    player.run(move)

    if user.reset:  # press r for reset
        player = entity.Player()
        bullets = []
        enemies = []
        score = 0
        bfr = -1  # bullet fire rate
        enemyMax = 10  # max number of enemies
        esr = -1  # enemy spawn rate
        efr = -1  # enemy fire rate
        time = 0  # play time in seconds
        user.keyPause = False
        user.reset = False

    if user.keyPause:  # press p for pause
        continue

    time += 1
    reward = -1
    # draw stuff
    GAME_SURFACE.fill(col.BLACK)

    # fires bullets every 0.5s (fps is 30 and this fires every 15 iterations)
    bfr += 1
    if bfr is 0:
        bullets.append(entity.BulletP(player.centX, player.centY))
    elif bfr is 15:
        bfr = -1

    for bullet in bullets:
        if bullet.collide:
            bullets.remove(bullet)

        bullet.fire(GAME_SURFACE)

    # enemy spawn
    esr += 1
    if esr is 0 and len(enemies) < enemyMax:
        enemies.append(entity.Enemy([random.randint(200, 1000), random.randint(0, 600)]))
    elif esr is 30:
        esr = -1

    # collision detection part
    for enemy in enemies:
        if enemy.rect.colliderect(player.rect):
            if not player.shield:
                player.collide = True
            enemy.collide = True
        for bullet in bullets:
            if bullet.rect.colliderect(enemy.rect):
                enemy.collide = True
                bullet.collide = True
        for bullet in enemy.bullets:
            if bullet.rect.colliderect(player.rect):
                if not player.shield:
                    player.collide = True
                bullet.collide = True

        if enemy.collide:
            enemies.remove(enemy)
            score += 1
            reward += 50

        enemy.run(GAME_SURFACE)

    drawText(10, 10, 'Score: %d  Time: %.2fs' % (score, time / FPS))

    player.draw(GAME_SURFACE)

    if time > 900 and score < 10:
        player.collide = True

    if player.collide:
        reward = -100
        user.reset = True
        if score > hiScore:
            hiScore = score
        pg.display.set_caption(GAME_TITLE + '  HIGH SCORE: ' + str(hiScore))

    # update screen
    pg.display.update()

leave()
