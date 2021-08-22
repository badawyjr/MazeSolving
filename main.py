import pygame
import math
import random
from queue import PriorityQueue

#_INITIALISE
WIDTH, HEIGHT = 800, 800
cellSize = 20
rows = WIDTH // cellSize
cols = HEIGHT // cellSize
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze')

#_COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (190, 190, 190)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (10,189,198)
SKY_BLUE = (19,62,124)
DARK_BLUE = (9,24,51)
PURPLE = (128, 0, 128)
PINK = (234,0,217)
DARK_PURPLE = (113,28,145)
ORANGE= (255, 165, 0)
YELLOW = (255, 255, 0)

#_CELL
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * cellSize
        self.y = col * cellSize
        self.color = WHITE
        self.neighbours  = []

    def setWall(self):
        self.color = BLACK

    def setStart(self):
        self.color = PURPLE

    def setEnd(self):
        self.color = BLUE

    def setOpen(self):
        self.color = SKY_BLUE

    def setClosed(self):
        self.color = LIGHT_BLUE

    def setPath(self):
        self.color = PURPLE

    def reset(self):
        self.color = WHITE


    def draw(self):
        pygame.draw.rect(WINDOW, self.color, (self.x, self.y, cellSize, cellSize))    

    def getPos(self):
        return self.row, self.col

    def getColor(self):
        return self.color

    def isWall(self):
        return self.color == BLACK

    def isStart(self):
        return self.color == GREEN

    def isEnd(self):
        return self.color == BLUE

    def update_neighbours(self, maze):
        self.neighbours = []
        #Down
        if self.row < WIDTH/cellSize - 1 and not maze[self.row + 1][self.col].isWall(): 
            self.neighbours.append(maze[self.row + 1][self.col])

        if self.row > 0 and not maze[self.row - 1][self.col].isWall():
            self.neighbours.append(maze[self.row - 1][self.col])

        if self.col < HEIGHT/cellSize - 1 and not maze[self.row][self.col + 1].isWall():
            self.neighbours.append(maze[self.row][self.col + 1])

        if self.row < 0 - 1 and not maze[self.row][self.col - 1].isWall():
            self.neighbours.append(maze[self.row][self.col - 1])


    def __lt__(self, value):
        return False
        
#_Algorithm
# Calculating the heuristic using Manhattan distance
def heurisitc(cell1,cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    manhattan  = abs(x2-x1) + abs(y2-y1)
    return manhattan

def create_path(CameFrom, current, draw):

    while current in CameFrom:
        current = CameFrom[current]
        current.setPath()
        draw()

def AStar(draw, maze, start, end):
    ctr = 0
    OpenSet = PriorityQueue()
    OpenSet.put((0, ctr, start)) #We put start cell in the open set 
    CameFrom = {} #What node came from where

    GScore = {cell: float("inf") for row in maze for cell in row} #Local shortest path
    GScore[start] = 0

    FScore = {cell: float("inf") for row in maze for cell in row} #GFlobal Shortest path
    FScore[start] = heurisitc(start.getPos(), end.getPos())

    OpenSetHash = {start}

    while not OpenSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        current = OpenSet.get()[2] #current node we are looking at
        OpenSetHash.remove(current)

        if current == end:
            end.setPath()
            create_path(CameFrom, current, draw)
            return True

        for neighbour in current.neighbours:
            tmpG = GScore[current] + 1

            if tmpG < GScore[neighbour]:
                CameFrom[neighbour] = current
                GScore[neighbour] = tmpG
                FScore[neighbour] = tmpG + heurisitc(neighbour.getPos(), end.getPos())
                if neighbour not in OpenSetHash:
                    ctr += 1
                    OpenSet.put((FScore[neighbour], ctr , neighbour))
                    OpenSetHash.add(neighbour)
                    neighbour.setOpen()
        
        draw()

        if current != start:
            current.setClosed()

    return False

#_Maze
def create_maze():
    rows = WIDTH // cellSize
    cols = HEIGHT // cellSize
    maze = []
    for i in range(rows):
        maze.append([])
        for j in range(cols):
            cell = Cell(i, j)
            if (random.randint(1, 5) == 1):
                cell.setWall()
            maze[i].append(cell)       
    return maze

def draw_grid(WINDOW):
    for i in range(rows):
        pygame.draw.line(WINDOW, WHITE, (0, i * cellSize), (WIDTH, i * cellSize))
        for j in range(cols):
            pygame.draw.line(WINDOW, WHITE, (j * cellSize, 0), (j * cellSize, HEIGHT))

def draw_maze(WINDOWS, grid):

    WINDOW.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw()

    draw_grid(WINDOW)
    pygame.display.update()

def click_pos(pos):
    x, y  = pos
    return x // cellSize , y // cellSize

def main():
    STATE = True
    start  = None
    end  = None
    started = False
    maze = create_maze()

    while STATE:

        draw_maze(WINDOW, maze)
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                STATE = False

            if pygame.mouse.get_pressed()[0]:
                row , col  = click_pos(pygame.mouse.get_pos())
                cell = maze[row][col]

                if not start :
                    start  = cell
                    start.setStart()

                elif not end and cell != start:
                    end  = cell
                    end.setEnd()
                
                elif cell != start and cell != end:
                    cell.setWall()

            if pygame.mouse.get_pressed()[2]:
                row , col  = click_pos(pygame.mouse.get_pos())
                cell = maze[row][col]
                cell.reset()
                if cell  == start :
                    start = None                  
                elif cell == end :
                    end = None

            if event.type  == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in maze:
                        for cell  in row:
                            cell.update_neighbours(maze) 

                    AStar(lambda: draw_maze(WINDOW, maze), maze, start, end)    

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    maze = create_maze()        

    pygame.quit()

if __name__ == "__main__":
    main()