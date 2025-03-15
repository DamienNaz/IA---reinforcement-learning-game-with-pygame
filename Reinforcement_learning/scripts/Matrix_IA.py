import pygame
import numpy as np
import random


class Matrix(object):

    def __init__(self, height, width, iconSize):
        self._height = height
        self._width = width
        self._iconSize = iconSize
        self._matrixRows = self._height // iconSize[0]
        self._matrixCols = self._width // iconSize[1]
        self.matrix = np.ndarray((self._matrixRows, self._matrixCols), dtype=object)
        self.matrix[:, :] = 'empty'
        self.yIron = None
        self.xIron = None
        self.score = 0

    isLeftClicked = False
    isRightClicked = False
    isUpClicked = False
    isDownClicked = False
    isEClicked = False

    def fillEmptyMatrix(self, y, x):

        self.matrix[y, x] = 'empty'

    def fillIronMatrix(self, y, x):
        # if self.yIron is not None:
        #   self.fillEmptyMatrix(self.yIron, self.xIron)
        self.matrix[y, x] = 'iron'
        self.yIron = y
        self.xIron = x

    def spwanGarbageRandom(self, numberOfTimes):

        for _ in range(numberOfTimes):
            while True:
                x = random.randrange(0, self._matrixCols, 1)
                y = random.randrange(0, self._matrixRows, 1)

                if self.matrix[y, x] != 'empty':
                    continue
                else:
                    # print(f'Appel->{[self.y, self.x]}')
                    # print(f'Snake->{tmp}')
                    self.matrix[y, x] = 'garbage'
                    break

    def drawMatrix(self, surface, _image_iron_man, _image_garbage, iconSize):

        surface.fill((255, 255, 255))

        for y in range(self._matrixRows):
            for x in range(self._matrixCols):
                if self.matrix[y, x] == 'iron':
                    surface.blit(_image_iron_man, (x * iconSize[1], y * iconSize[0]), (0, 0, iconSize[1], iconSize[0]))
                elif self.matrix[y, x] == 'garbage':
                    surface.blit(_image_garbage, (x * iconSize[1], y * iconSize[0]), (0, 0, iconSize[1], iconSize[0]))

        for y in range(0, self._height, self._iconSize[0]):
            pygame.draw.line(surface, (0, 0, 0), (0, y), (self._width - 1, y), 2)

        for x in range(0, self._width, self._iconSize[1]):
            pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, self._height - 1), 2)

    pass

    def moveIronMan(self, direction):
        if direction == 'up' and self.yIron > 0:
            self.fillIronMatrix(self.yIron - 1, self.xIron)
        elif direction == 'down' and self.yIron < self._matrixRows - 1:
            self.fillIronMatrix(self.yIron + 1, self.xIron)
        elif direction == 'left' and self.xIron > 0:
            self.fillIronMatrix(self.yIron, self.xIron - 1)
        elif direction == 'right' and self.xIron < self._matrixCols - 1:
            self.fillIronMatrix(self.yIron, self.xIron + 1)
        print(f"IronMan's position: ({self.yIron}, {self.xIron})")
        print({
            'IronPosition': (self.yIron, self.xIron),
            'UpperCell': self.matrix[self.yIron - 1, self.xIron] if self.yIron > 0 else 'wall',
            'LowerCell': self.matrix[self.yIron + 1, self.xIron] if self.yIron < self._matrixRows - 1 else 'wall',
            'LeftCell': self.matrix[self.yIron, self.xIron - 1] if self.xIron > 0 else 'wall',
            'RightCell': self.matrix[self.yIron, self.xIron + 1] if self.xIron < self._matrixCols - 1 else 'wall'})

    def valid_movement(self, isLeftClicked, isRightClicked, isUpClicked, isDownClicked):

        next_x = self.xIron
        next_y = self.yIron

        if isLeftClicked:
            next_x = self.xIron - 1
        elif isRightClicked:
            next_x = self.xIron + 1
        elif isUpClicked:
            next_y = self.yIron - 1
        elif isDownClicked:
            next_y = self.yIron + 1

        if next_x < 0 or next_y < 0 or next_x > self._matrixCols - 1 or next_y > self._matrixRows - 1:
            return False
        else:
            return True

    def give_score(self, points):
        self.score += points
        print(f"IronMan's position: ({self.yIron}, {self.xIron})")
        print(f"Current Score: {self.score}")


    def write_score_to_txt(self,action,step):

        try:
            with open('scripts\score_log_IA.txt', 'a') as file:
                file.write(f"Steps: {step}\n")
                file.write(f"IronPosition: ({self.yIron}, {self.xIron})\n")
                file.write(f"UpperCell: {self.matrix[self.yIron - 1, self.xIron] if self.yIron > 0 else 'wall'}\n")
                file.write(f"LowerCell: {self.matrix[self.yIron + 1, self.xIron] if self.yIron < self._matrixRows - 1 else 'wall'}\n")
                file.write(f"LeftCell: {self.matrix[self.yIron, self.xIron - 1] if self.xIron > 0 else 'wall'}\n")
                file.write(f"RightCell: {self.matrix[self.yIron, self.xIron + 1] if self.xIron < self._matrixCols - 1 else 'wall'}\n")
                file.write(f"Current Score: {self.score}\n")
                file.write(f"Action: {action}\n")
                #current_cell_state = self.matrix[self.yIron, self.xIron]
                #file.write(f"CurrentCellState: {current_cell_state}\n")
                file.write("\n")
        except Exception as e:
            print(f"Erro ao abrir o ficheiro: {e}")

    def is_garbage_there(self, value):
        if value == 'garbage':
            return True
        else:
            return False

