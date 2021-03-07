# MIT License
# 
# Copyright (c) 2017 Stephens Nunnally and Scidian Software
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ----- Imports
import sys
import pygame
import pygcurse
from random import *


# ----- Global variables
WINWIDTH, WINHEIGHT, FPS = 40, 25, 20
hasMoved = False

win = pygcurse.PygcurseWindow(WINWIDTH, WINHEIGHT, fullscreen=False)
pygame.display.set_caption('PyThon Snake')
win.autoupdate = False
clock = pygame.time.Clock()


# ----- Resets all variables for new game
def reset_game(new_game):
    global pos, length, direction, speed, increment, alive
    global stage, level, score, current, objx, objy, growth
    direction = [1, 0]
    increment = [0.0, 0.0]
    if new_game:
        alive = True
        stage = 1
        score = 0
    current = 1
    get_level = load_level(stage)
    level = get_level[0]
    length = get_level[1]
    speed = get_level[2]
    growth = get_level[3]
    pos = [[10, 10]]
    for i in range(0, WINWIDTH):
        for j in range(0, WINHEIGHT):
            if level[j][i:i+1] == "S":
                pos = [[i, j]]
    for i in range(0, length):
        pos.append([pos[0][0] - 1, pos[0][1]])
    load_number()


# ----- Main loop
def main():
    while True:
        handle_events()
        if alive:
            update_snake()
        draw_screen()
        clock.tick(FPS)


# ----- Draws everything onto the screen
def draw_screen():
    win.fill(bgcolor='white')
    win.putchars("Stage " + str(stage), 0, 0, 'black')
    win.putchars("Score " + str(score), 16, 0, 'black')
    win.putchars("Speed " + str(speed[0]), 31, 0, 'black')

    for i in range(0, len(pos)):
        if alive:
            win.fill('#', 'black', 'black', region=(pos[i][0], pos[i][1], 1, 1))
        else:
            win.fill('#', 'red', 'red', region=(pos[i][0], pos[i][1], 1, 1))
            win.putchars("PRESS SPACEBAR TO RESET", 8, 12, 'blue')

    for i in range(0, WINWIDTH):
        for j in range(0, WINHEIGHT):
            if level[j][i:i+1] == "A":
                win.fill('#', 'black', 'black', region=(i, j, 1, 1))
            elif level[j][i:i+1] == "O":
                win.fill(str(current)[-1], 'white', 'blue', region=(i, j, 1, 1))

    win.update()


# ----- Updates the snakes location, interaction with the level
def update_snake():
    global alive, score, current, stage, hasMoved
    hasMoved = True

    # Add speed to an incremental variable, move snake if we've moved more than one block
    increment[0] += (speed[0] * direction[0])
    increment[1] += (speed[1] * direction[1])
    while (abs(increment[0]) > 1) or (abs(increment[1]) > 1):
        for i in range(len(pos) - 1, 0, -1):
            pos[i][0] = pos[i - 1][0]
            pos[i][1] = pos[i - 1][1]

        if abs(increment[0]) > 1:
            pos[0][0] += direction[0]
            increment[0] -= direction[0]
        if abs(increment[1]) > 1:
            pos[0][1] += direction[1]
            increment[1] -= direction[1]

    # Check for snake wrap around
    if pos[0][0] < 0:
        pos[0][0] = WINWIDTH - 1
    if pos[0][0] > WINWIDTH - 1:
        pos[0][0] = 0
    if pos[0][1] < 1:
        pos[0][1] = WINHEIGHT - 1
    if pos[0][1] > WINHEIGHT - 1:
        pos[0][1] = 1

    # Check if snake has hit himself or a wall
    newGame = False
    for i in range(1, len(pos)):
        if not newGame:
            if (pos[0][0] == pos[i][0]) and (pos[0][1] == pos[i][1]):
                alive = False
            if (pos[0][0] == objx) and (pos[0][1] == objy):
                current += 1
                score += 1
                if current > 9:
                    stage += 1
                    reset_game(False)
                    newGame = True
                else:
                    for j in range(0, growth):
                        pos.append([pos[-1][0], pos[-1][1]])
                    load_number()
    if level[pos[0][1]][pos[0][0]] == "A":
        alive = False


# ----- Places next objective into screen
def load_number():
    global level, current, objx, objy

    for x in range(0, WINWIDTH):
        for y in range(0, WINHEIGHT):
            if level[y][x:x + 1] == "O":
                str1 = level[y]
                list1 = list(str1)
                list1[x] = " "
                str1 = ''.join(list1)
                level[y] = str1

    placed = False
    while not placed:
        x = randint(0, WINWIDTH - 1)
        y = randint(1, WINHEIGHT - 1)

        # Don't put number in snake or in wall
        isSnake = False
        for i in range(1, len(pos)):
            if (pos[i][0] == x) and (pos[i][1] == y):
                isSnake = True
        if not isSnake and (level[y][x:x + 1] == " "):
            str1 = level[y]
            list1 = list(str1)
            list1[x] = "O"
            str1 = ''.join(list1)
            level[y] = str1
            objx, objy = x, y
            placed = True


# ----- Watches for user input
def handle_events():
    global direction, increment, speed, hasMoved

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                terminate()
            if event.key == pygame.K_UP:
                if (direction[0] != 0) and hasMoved:
                    direction = [0, -1]
                    increment = [0, speed[1] * -1]
                    hasMoved = False
            if event.key == pygame.K_DOWN:
                if (direction[0] != 0) and hasMoved:
                    direction = [0, 1]
                    increment = [0, speed[1]]
                    hasMoved = False
            if event.key == pygame.K_LEFT:
                if (direction[1] != 0) and hasMoved:
                    direction = [-1, 0]
                    increment = [speed[0] * -1, 0]
                    hasMoved = False
            if event.key == pygame.K_RIGHT:
                if (direction[1] != 0) and hasMoved:
                    direction = [1, 0]
                    increment = [speed[0], 0]
                    hasMoved = False
            if event.key == pygame.K_SPACE:
                reset_game(True)
            if event.key == pygame.K_z:
                if speed[0] > .2:
                    speed[0] -= .2
                    speed[1] -= .2
                speed = [round(speed[0], 1), round(speed[1], 1)]
            if event.key == pygame.K_x:
                speed[0] += .2
                speed[1] += .2
                speed = [round(speed[0], 1), round(speed[1], 1)]


# ----- Exit application
def terminate():
    pygame.quit()
    sys.exit()


def load_level(level_to_load):
    level_data = []
    for i in range(0, 41):
        level_data.append(" ")

    start_length = 1
    grow_rate = 1
    start_speed = [1, 1]

    if level_to_load == 1:
        start_length = 10
        grow_rate = 1
        start_speed = [.7, .7]
        level_data[0] =  "                                        "
        level_data[1] =  "AAAAAAAAAAAAAA          AAAAAAAAAAAAAAAA"
        level_data[2] =  "A                                      A"
        level_data[3] =  "A                                      A"
        level_data[4] =  "A                                      A"
        level_data[5] =  "A                                      A"
        level_data[6] =  "A     S                                A"
        level_data[7] =  "A                                      A"
        level_data[8] =  "A                                      A"
        level_data[9] =  "A                                      A"
        level_data[10] = "                                        "
        level_data[11] = "                                        "
        level_data[12] = "                                        "
        level_data[13] = "                                        "
        level_data[14] = "                                        "
        level_data[15] = "A                                      A"
        level_data[16] = "A                                      A"
        level_data[17] = "A                                      A"
        level_data[18] = "A                                      A"
        level_data[19] = "A                                      A"
        level_data[20] = "A                                      A"
        level_data[21] = "A                                      A"
        level_data[22] = "A                                      A"
        level_data[23] = "A                                      A"
        level_data[24] = "AAAAAAAAAAAAAA          AAAAAAAAAAAAAAAA"
    elif level_to_load >= 2:
        start_length = 10
        grow_rate = 2
        start_speed = [1.0, 1.0]
        level_data[0] =  "                                        "
        level_data[1] =  "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        level_data[2] =  "A                                      A"
        level_data[3] =  "A                                      A"
        level_data[4] =  "A                                      A"
        level_data[5] =  "A                                      A"
        level_data[6] =  "A                                      A"
        level_data[7] =  "A                                      A"
        level_data[8] =  "A                                      A"
        level_data[9] =  "A                                      A"
        level_data[10] = "A                                      A"
        level_data[11] = "A                                      A"
        level_data[12] = "A            AAAAAAAAAAAAAA            A"
        level_data[13] = "A                                      A"
        level_data[14] = "A                                      A"
        level_data[15] = "A                                      A"
        level_data[16] = "A                                      A"
        level_data[17] = "A                                      A"
        level_data[18] = "A                                      A"
        level_data[19] = "A                                      A"
        level_data[20] = "A                                      A"
        level_data[21] = "A    S                                 A"
        level_data[22] = "A                                      A"
        level_data[23] = "A                                      A"
        level_data[24] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

    return level_data, start_length, start_speed, grow_rate


# ----- Starts the game
if __name__ == '__main__':
    reset_game(True)
    main()
