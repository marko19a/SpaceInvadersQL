# classes controller, player,
import pygame as pg

pg.init()


class Interactor:
    # interact for objects
    def __init__(self):
        self.keyUp = 0
        self.keyDown = 0
        self.keyLeft = 0
        self.keyRight = 0

        self.keyPause = False
        self.reset = False
        self.keyShield = False
        self.running = True

        self.keyPressed = [
            self.keyUp,
            self.keyDown,
            self.keyLeft,
            self.keyRight,

            self.keyShield,
        ]

    def run(self):
        # running script returns list
        for event in pg.event.get():
            if pg.KEYDOWN == event.type:
                if pg.K_a == event.key:
                    self.keyLeft = -1

                elif pg.K_d == event.key:
                    self.keyRight = 1

                elif pg.K_w == event.key:
                    self.keyUp = -1

                elif pg.K_s == event.key:
                    self.keyDown = 1

                elif pg.K_SPACE == event.key:
                    self.keyShield = True

                elif pg.K_p == event.key:
                    if self.keyPause:
                        self.keyPause = False
                    else:
                        self.keyPause = True

                elif pg.K_ESCAPE == event.key:
                    self.running = False

                elif pg.K_r == event.key:
                    self.reset = True

            elif pg.KEYUP == event.type:
                if pg.K_a == event.key:
                    self.keyLeft = 0

                elif pg.K_d == event.key:
                    self.keyRight = 0

                elif pg.K_w == event.key:
                    self.keyUp = 0

                elif pg.K_s == event.key:
                    self.keyDown = 0

                elif pg.K_SPACE == event.key:
                    self.keyShield = False

                elif pg.K_r == event.key:
                    self.reset = False

            elif pg.QUIT == event.type:
                self.running = False

        self.keyPressed[0] = self.keyUp
        self.keyPressed[1] = self.keyDown
        self.keyPressed[2] = self.keyLeft
        self.keyPressed[3] = self.keyRight
        self.keyPressed[4] = self.keyShield

        return self.keyPressed
