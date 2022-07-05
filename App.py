import os
import pygame
from pygame.math import Vector2
from pygame import Rect

os.environ['SDL_VIDEO_CENTERED'] = '1'

array = [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0,
         0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0,
         0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0,
         1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1,
         1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1,
         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
         1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1,
         1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1,
         0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0,
         0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0,
         0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
row = 11
col = 11
wallColor = (200, 200, 200)


class GameState():
    def __init__(self):
        self.tankPos = Vector2(row // 2, col // 2)
        self.worldSize = Vector2(row, col)

    def update(self, moveTankCommand):
        self.tankPos += moveTankCommand

        if array[int(self.tankPos.y) * col + int(self.tankPos.x)] == 1:
            self.tankPos -= moveTankCommand
            return

        if self.tankPos.x < 0:
            self.tankPos.x = 0
        elif self.tankPos.x >= self.worldSize.x:
            self.tankPos.x = self.worldSize.x - 1

        elif self.tankPos.y < 0:
            self.tankPos.y = 0
        elif self.tankPos.y >= self.worldSize.y:
            self.tankPos.y = self.worldSize.y - 1


class UserInterface():
    def __init__(self):
        pygame.init()

        self.gameState = GameState()

        self.cellSize = Vector2(32, 32)
        self.unitsTexture = pygame.image.load("icon.png")

        windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode(
            (int(windowSize.x), int(windowSize.y)))
        pygame.display.set_icon(pygame.image.load("icon.png"))
        self.moveTankCommand = Vector2(0, 0)

        self.clock = pygame.time.Clock()
        self.running = True

    def processInput(self):
        self.moveTankCommand = Vector2(0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    print("left")
                    self.moveTankCommand = Vector2(1, 0)
                elif event.key == pygame.K_LEFT:
                    print("right")
                    self.moveTankCommand = Vector2(-1, 0)
                elif event.key == pygame.K_DOWN:
                    print("down")
                    self.moveTankCommand = Vector2(0, 1)
                elif event.key == pygame.K_UP:
                    print("up")
                    self.moveTankCommand = Vector2(0, -1)

    def update(self):
        self.gameState.update(self.moveTankCommand)

    def render(self):
        self.window.fill((0, 0, 0))
        self.genWall()

        spritePoint = self.gameState.tankPos.elementwise()*self.cellSize
        texturePoint = Vector2(1, 0).elementwise()*self.cellSize
        textureRect = Rect(int(texturePoint.x), int(
            texturePoint.y), int(self.cellSize.x), int(self.cellSize.y))
        self.window.blit(self.unitsTexture, spritePoint, textureRect)

        pygame.display.update()

    def genWall(self):
        for y in range(row):
            for x in range(col):
                if (array[y * col + x] == 1):
                    pos = Vector2(x, y).elementwise()*self.cellSize
                    pygame.draw.rect(self.window, wallColor, pygame.Rect(
                        int(pos.x), int(pos.y), int(self.cellSize.x), int(self.cellSize.y)))

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)


userInterface = UserInterface()
userInterface.run()

pygame.quit()
