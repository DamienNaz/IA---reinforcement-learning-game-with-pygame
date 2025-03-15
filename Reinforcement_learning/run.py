from pygame.locals import *
import pygame
import time
import random
from scripts.Naive_gauss import processar_log, prepare_input_for_model, train_and_evaluate_model
from scripts.Matrix_IA import Matrix

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

value = 'empty'
steps = 0

df = processar_log('score_log.txt')
direction_predicted = train_and_evaluate_model(df)

while steps <= 19:
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    ai_move = direction_predicted[steps]

    steps += 1
    time.sleep(0.3)
    print(f"Steps: {steps}, AI Move: {ai_move}")

    # Reset clicked flags
    isLeftClicked = False
    isRightClicked = False
    isUpClicked = False
    isDownClicked = False
    isEClicked = False

    # Perform the chosen move
    if ai_move == 'left':
        isLeftClicked = True
        if m.valid_movement(isLeftClicked, isRightClicked, isUpClicked, isDownClicked):
            m.matrix[m.yIron, m.xIron] = value
            value = m.matrix[m.yIron, m.xIron - 1]
            m.moveIronMan('left')
            m.write_score_to_txt(action="left", step=steps)
        else:
            m.give_score(-5)

    elif ai_move == 'right':
        isRightClicked = True
        if m.valid_movement(isLeftClicked, isRightClicked, isUpClicked, isDownClicked):
            m.matrix[m.yIron, m.xIron] = value
            value = m.matrix[m.yIron, m.xIron + 1]
            m.moveIronMan('right')
            m.write_score_to_txt(action="right", step=steps)
        else:
            m.give_score(-5)

    elif ai_move == 'down':
        isDownClicked = True
        if m.valid_movement(isLeftClicked, isRightClicked, isUpClicked, isDownClicked):
            m.matrix[m.yIron, m.xIron] = value
            value = m.matrix[m.yIron + 1, m.xIron]
            m.moveIronMan('down')
            m.write_score_to_txt(action="down", step=steps)
        else:
            m.give_score(-5)

    elif ai_move == 'Up':
        isUpClicked = True
        if m.valid_movement(isLeftClicked, isRightClicked, isUpClicked, isDownClicked):
            m.matrix[m.yIron, m.xIron] = value
            value = m.matrix[m.yIron - 1, m.xIron]
            m.moveIronMan('up')
            m.write_score_to_txt(action="up", step=steps)
        else:
            m.give_score(-5)

    elif ai_move == 'E':
        isEClicked = True
        if m.is_garbage_there(value):
            m.give_score(10)
            value = 'empty'
        else:
            m.give_score(-1)

        m.moveIronMan('E')
        m.write_score_to_txt(action="E", step=steps)
        print("Tecla E clicada")




    m.drawMatrix(boardGame, _image_iron_man, _image_garbage, iconSize)
    pygame.display.flip()
