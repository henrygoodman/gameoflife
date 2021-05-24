import numpy
import pygame
import sys
import random

width = 1000
height = 1000
RESOLUTION = 50
SQUARESIZE = width / RESOLUTION
size = width, height
screen = pygame.display.set_mode(size)
screen.fill((50,50,50))
pygame.init()
font = pygame.font.SysFont("Arial", 75)

def button(screen, position, text):
    text_render = font.render(text, 1, (255, 0, 0))
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))
    return screen.blit(text_render, (x, y))

def create_grid():
    grid = numpy.zeros((int(RESOLUTION), int(RESOLUTION)))
    return numpy.flipud(grid)

grid = create_grid()

def draw_board(grid):
    for x in range(RESOLUTION):
        for y in range(RESOLUTION):
            if (grid[x,y] == 0):
                pygame.draw.rect(screen, (0,0,0), (x * SQUARESIZE, y * SQUARESIZE, SQUARESIZE-SQUARESIZE/20, SQUARESIZE-SQUARESIZE/20) )
            else :
                pygame.draw.rect(screen, (255,255,255), (x * SQUARESIZE, y * SQUARESIZE, SQUARESIZE-SQUARESIZE/20, SQUARESIZE-SQUARESIZE/20) )
    pygame.display.update()


# Take x, y between 0 - width (height), normalize it to a value between 0 - RESOLUTION, set grid[newX, newY] to 1. 
def set_live(x , y):
    scaleFactor = width / RESOLUTION
    newX = x / scaleFactor
    newY = y / scaleFactor
    grid[int(newX), int(newY)] = 1
    return

over = False
draw_board(grid)
last_pos = (-1,-1)

def count(x,y):
    count = 0
    for i in range (-1, 2):
        for j in range (-1, 2):
            count += grid[x + i, y + j]
    return count - grid[x,y]

newGrid = create_grid()

def step(grid):
    for x in range(1, RESOLUTION-1):
        for y in range(1, RESOLUTION-1):
            if grid[x,y] == 1:
                if count(x,y) < 2 or count(x,y) > 3:
                    newGrid[x,y] = 0
                else: 
                    newGrid[x,y] = 1
            else:
                if count(x,y) == 3:
                    newGrid[x,y] = 1

    for x in range(1, RESOLUTION-1):
        for y in range(1, RESOLUTION-1):
            grid[x,y] = newGrid[x,y]
    pygame.display.update()
    draw_board(grid)



while not over:

    b1 = button(screen, (50,50), "START")
    mouse_pos = pygame.mouse.get_pos()
    if ( mouse_pos != last_pos ):
        x,y = mouse_pos
        last_pos = mouse_pos

    # Event loop
    for event in pygame.event.get():
        pygame.display.update()

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0] == True:
            if b1.collidepoint(mouse_pos):
                flag = True
                while flag:
                    b2 = button(screen, (50,50), "STOP!!")   
                    step(grid)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0] == True:
                            if b2.collidepoint(mouse_pos):
                                flag = False

            x_pos = mouse_pos[0]
            y_pos = mouse_pos[1]
            set_live(x_pos, y_pos)
            draw_board(grid) 

    pygame.display.update()