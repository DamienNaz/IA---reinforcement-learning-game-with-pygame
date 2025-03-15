from pygame.locals import *
import pygame
import random
from scripts.Matrix1 import Matrix

iconSize = (150, 150)  # (y, x)
totalWidthAndHeight = 5
windowWidth = iconSize[0] * totalWidthAndHeight
windowHeight = iconSize[0] * totalWidthAndHeight

pygame.init()
boardGame = pygame.display.set_mode((windowWidth, windowHeight), pygame.HWSURFACE)
boardGame.fill((255, 255, 255))
pygame.display.set_caption('Hulk IA')

_image_iron_man = pygame.image.load("textures/pngegg.png").convert_alpha()
_image_iron_man = pygame.transform.scale(_image_iron_man, (iconSize[0], iconSize[1]))

_image_garbage = pygame.image.load("textures/garbage.jpg").convert_alpha()
_image_garbage = pygame.transform.scale(_image_garbage, (iconSize[0], iconSize[1]))

m = Matrix(windowHeight, windowWidth, iconSize)
m.fillIronMatrix(random.randint(0, 4), random.randint(0, 4))

totalSquares = totalWidthAndHeight * totalWidthAndHeight
garbagePercentage = int(0.3 * totalSquares)
m.spwanGarbageRandom(garbagePercentage)

isLeftClicked = False
isRightClicked = False
isUpClicked = False
isDownClicked = False
isEClicked = False
value = 'empty'
steps = 0

while steps <= 19 and True:
    pygame.event.pump()
    keys = pygame.key.get_pressed()

    if keys[K_ESCAPE]:
        break

    isEProcessed = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            steps += 1

            print(f'steps: {steps}')
            print(f"Current Score: {m.score}")
            print(m.matrix)
            if event.key == pygame.K_LEFT and not isLeftClicked:
                isLeftClicked = True

                if m.valid_movement(isLeftClicked, isRightClicked, isUpClicked, isDownClicked):
                    m.matrix[m.yIron, m.xIron] = value
                    value = m.matrix[m.yIron, m.xIron - 1]
                    m.moveIronMan('left')
                    m.write_score_to_txt(action="left", step=steps)
                else:
                    m.give_score(-5)


            elif event.key == pygame.K_RIGHT and not isRightClicked:
                isRightClicked = True

                if m.valid_movement(isLeftClicked, isRightClicked, isUpClicked, isDownClicked):
                    m.matrix[m.yIron, m.xIron] = value
                    value = m.matrix[m.yIron, m.xIron + 1]
                    m.moveIronMan('right')
                    m.write_score_to_txt(action="right",step=steps)
                else:
                    m.give_score(-5)


            elif event.key == pygame.K_UP and not isUpClicked:
                isUpClicked = True

                if m.valid_movement(isLeftClicked, isRightClicked, isUpClicked, isDownClicked):
                    m.matrix[m.yIron, m.xIron] = value
                    value = m.matrix[m.yIron - 1, m.xIron]
                    m.moveIronMan('up')
                    m.write_score_to_txt(action="Up",step=steps)
                else:
                    m.give_score(-5)


            elif event.key == pygame.K_DOWN and not isDownClicked:
                isDownClicked = True
                # ficheiro txt celulus vizinhas
                if m.valid_movement(isLeftClicked, isRightClicked, isUpClicked, isDownClicked):

                    m.matrix[m.yIron, m.xIron] = value
                    value = m.matrix[m.yIron + 1, m.xIron]
                    m.moveIronMan('down')
                    m.write_score_to_txt(action="down",step=steps)
                else:
                    m.give_score(-5)


            elif event.key == pygame.K_e and not isEClicked:
                isEClicked = True

                if m.is_garbage_there(value):
                    m.give_score(10)

                    value = 'empty'
                else:
                    m.give_score(-1)

                m.moveIronMan('e')
                m.write_score_to_txt(action="E",step=steps)
                print("Tecla E clicada")


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and isLeftClicked:
                isLeftClicked = False
            elif event.key == pygame.K_RIGHT and isRightClicked:
                isRightClicked = False
            elif event.key == pygame.K_UP and isUpClicked:
                isUpClicked = False
            elif event.key == pygame.K_DOWN and isDownClicked:
                isDownClicked = False
            elif event.key == pygame.K_e and isEClicked:
                # m.tryCollectGarbage()  # Tenta coletar o lixo na posição atual
                isEClicked = False


    m.drawMatrix(boardGame, _image_iron_man, _image_garbage, iconSize)
    pygame.display.flip()

