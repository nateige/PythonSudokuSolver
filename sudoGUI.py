import pygame, sys
import random
import tkinter as tk
import os
from tkinter import *
from pygame.locals import *


BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (200,200,200)

windowLength = 500
windowWidth = 500
windowSize = 90
windowMult = 5

windowLength = int(windowSize * windowMult)
windowWidth = int(windowSize * windowMult)
squareSize = int((windowSize * windowMult)/3)
cellSize = int(squareSize/3)

root = tk.Tk()

menubar = Menu(root)
root.config(menu=menubar)

bottomFrame = tk.Frame(root)
bottomFrame.pack(side=BOTTOM)

embed = tk.Frame(root, width=450, height = 450)
#embed.grid(columnspan = 500, rowspan = 500)
embed.pack(side = "left")
embed.config(bg = "blue")

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

DISPLAYSURF = pygame.display.set_mode((windowLength,windowWidth))
pygame.display.set_caption("Cool Sudoku")
DISPLAYSURF.fill(WHITE)

pygame.display.init()
pygame.display.update()


global BASICFONT, BASICFONTSIZE
BASICFONTSIZE = 45
pygame.font.init()
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)


gridRand = [ [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0] ]

sudokuVals = [1,2,3,4,5,6,7,8,9]

def generatePuzzle():

    global gridRand
    gridRand = [ [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0] ]

    # Grab a random pair of indeces in the diagonal 3x3 grids
    diagGrid_1 = [[0,0], [0,1] , [0,2] , [1,0] , [1,1] , [1,2], [2,0], [2,1] , [2,2]]
    diagGrid_2 = [[3,3], [3,4] , [3,5] , [4,3] , [4,4] , [4,5], [5,3], [5,4] , [5,5]]
    diagGrid_3 = [[6,6], [6,7] , [6,8] , [7,6] , [7,7] , [7,8], [8,6], [8,7] , [8,8]]

    diagSelection1 = random.sample(diagGrid_1, k=5)
    diagSelection2 = random.sample(diagGrid_2, k=5)
    diagSelection3 = random.sample(diagGrid_3, k=5)

    randDiag1 = random.sample(sudokuVals, k=5)
    randDiag2 = random.sample(sudokuVals, k=5)
    randDiag3 = random.sample(sudokuVals, k=5)

    # Place random sudoku values in the randomly selected indeces
    for i in range(0,5):
        d1x = diagSelection1[i][0]
        d1y = diagSelection1[i][1]
        d2x = diagSelection2[i][0]
        d2y = diagSelection2[i][1]
        d3x = diagSelection3[i][0]
        d3y = diagSelection3[i][1]
        
        gridRand[d1x][d1y] = randDiag1[i]
        gridRand[d2x][d2y] = randDiag2[i]
        gridRand[d3x][d3y] = randDiag3[i]
      
    clearGrid()
    fillGrid()

    return None


# Solve and Fill Grid
def solveFill():
    generatePuzzle()
    clearGrid()

    solveGrid()
    fillGrid()

# Check for duplicate values in each column
def checkColumn(y_index):
    
    global gridRand
    currentColumn = []
    for i in range(0,9):
        currentColumn.append(gridRand[i][y_index])
        
    filteredColumn = list(filter(lambda x: x !=0, currentColumn))
    if len(set(filteredColumn)) == len(filteredColumn):
        return True
    else:
        return False

# Check for duplicate values in each Row  
def checkRow(x_index):

    global gridRand
    filteredColumn = list(filter(lambda x: x !=0, gridRand[x_index]))
    if len(set(filteredColumn)) == len(filteredColumn):
        return True
    else:
        return False
 
# Check for duplicate values in reach 3x3 grid 
def checkGrid(x_index, y_index):

    global gridRand

    currentGrid = []

    #Integer division here splits input indexes (0,8) into 3 groups
    box_x = x_index // 3
    box_y = y_index // 3

    for i in range(box_x*3, box_x*3 + 3):
        for j in range(box_y * 3, box_y * 3 + 3):
            currentGrid.append(gridRand[i][j])
    
    filteredGrid = list(filter(lambda x: x !=0, currentGrid))
    if len(set(filteredGrid)) == len(filteredGrid):
        return True
    else:
        return False
    
    return False

    
# Determine if adding a value is valid by checking the row, column, and 3x3 grid of the current cell
def isValid(x_index, y_index):
    
    global gridRand
    if checkColumn(y_index) == False:
        return False
    
    if checkRow(x_index) == False:
        return False
    
    if checkGrid(x_index, y_index) == False:
        return False
    
    return True

# Find a zero in the sudoku grid
def find_zero():
    global gridRand
    for x_index, row in enumerate(gridRand):
        for y_index, val in enumerate(row):
            if val == 0:
                return (x_index, y_index)
    
    return None

# Solve the sudoku Grid
def solveGrid():

    global gridRand
    src_val = find_zero()
    if not src_val:
        return True
    else:
        row, col = src_val
    
    for i in range (1,10):
        gridRand[src_val[0]][src_val[1]] = i

        # Backtracking occurs here by recursively calling solveGrid(grid)
        if isValid(src_val[0], src_val[1]) and solveGrid():
            return True

    gridRand[src_val[0]][src_val[1]] = 0
        
    return False

# Draw the sudoku grid using pygame library
def drawGrid():

    for x in range(0, windowWidth, cellSize):
        pygame.draw.line(DISPLAYSURF, GREY, (x,0), (x, windowLength))
    for y in range(0, windowLength, cellSize):
        pygame.draw.line(DISPLAYSURF, GREY, (0,y), (windowWidth,y))
    
    for x in range(0, windowWidth, squareSize):
        pygame.draw.line(DISPLAYSURF, BLACK, (x,0), (x, windowLength))
    for y in range(0, windowLength, squareSize):
        pygame.draw.line(DISPLAYSURF, BLACK, (0,y), (windowWidth, y))

    return None

def clearGrid():
    DISPLAYSURF.fill(WHITE)
    drawGrid()

def fillGrid():

    global gridRand
    xCoordinate = 13
    yCoordinate = 7

    for row in gridRand:
        for index, val in enumerate(row):
            drawNumber(val, xCoordinate, yCoordinate)
            xCoordinate = xCoordinate + 50

            if index == 8:
                xCoordinate = 13
                yCoordinate = yCoordinate + 50
            

# Draw numbers into the sudoku Grid based on x,y coordinates                
def drawNumber(cellData, x, y):
    cellSurf = BASICFONT.render('%s' %(cellData), True, BLACK)
    cellRect = cellSurf.get_rect()
    cellRect.topleft = (x, y)
    DISPLAYSURF.blit(cellSurf, cellRect)

menubar.add_cascade(label="Generate Puzzle", command=generatePuzzle)
menubar.add_cascade(label="Solve Puzzle", command=solveFill)

def main():
    #pygame.init()
    solveGrid()
    drawGrid() 
    fillGrid()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        root.update()   
main()