# --------------------------------------------
#               by oognuyh
# --------------------------------------------
import sys, os, heapq, math
import pygame as pg
from pygame.locals import *
# --------------------------------------------
# TODO:  
# 1. wrong path when user allow diagonal lines(in_in_open() not changed the cell) - FIX 2019/11/27
# --------------------------------------------
# pygame initialize
pg.init()
# center
os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.display.set_caption("A* visualization")
width = 800
height = 800
menuside = 270
screen = pg.display.set_mode((width + menuside, height))
# --------------------------------------------
# define points
PATH = 0
WALL = 1
START = 2
END = 3
# --------------------------------------------
# define colours
BLACK = (0, 0, 0) # wall, outline, background
YELLOW = (255, 192, 0) # cell in open list
RED = (157, 0, 0) # the starting point
ORANGE = (237, 125, 49) # cell in closed list
BLUE = (68, 114, 196) # the current cell
GREEN = (0, 157, 0) # the ending point
GREY = (157, 157, 157) # path
WHITE = (255, 255, 255) # text colour
# --------------------------------------------
# define cell size, grid height and grid width
cellsize = 40
gridheight = height // cellsize
gridwidth = width // cellsize
# --------------------------------------------
# define heuristic weight limit
weightlimit = 50
# --------------------------------------------
# define FPS
FPS = 60
# --------------------------------------------
# define font
optionfont = pg.font.Font("PrStart.ttf", cellsize // 2)
# --------------------------------------------
# define directions
UP = [0, -1]
DOWN = [0, 1]
LEFT = [-1, 0]
RIGHT = [1, 0]
TOPLEFT = [-1, -1]
TOPRIGHT = [1, -1]
BOTTOMLEFT = [-1, 1]
BOTTOMRIGHT = [1, 1]
# --------------------------------------------
class Cell:
    def __init__(self, coord):
        self.coord = coord
        self.parent = None # parent cell's coord
        self.G = 0 # G cost
        self.H = 0 # H cost
        self.F = 0 # F cost

    def __lt__(self, other): # define operator <
        return self.F < other.F 

    def __eq__(self, other): # define operator ==
        return self.coord == other.coord

    def draw(self, colour): 
        x, y = self.coord
        pg.display.update(pg.draw.rect(screen, colour, (x * cellsize, y * cellsize, cellsize, cellsize)))
        pg.display.update(pg.draw.rect(screen, BLACK, (x * cellsize, y * cellsize, cellsize, cellsize), 1)) # outline

class Astar:
    def __init__(self, grid, start, end, weight, using, diagonal, open_is_heapq):
        self.grid = grid
        self.start = list(start) # the starting point
        self.end = list(end) # the ending point
        self.using = using # to get heuristic
        self.diagonal = diagonal # if allow diagonal lines, True 
        self.weight = weight # heuristic weight
        self.closed = [] # closed list
        self.open = [] # open list
        self.open_is_heapq = open_is_heapq
        if self.open_is_heapq:
            heapq.heapify(self.open) # list into heap

    def is_valid(self, coord):
        x, y = coord
        return -1 < x and x < gridwidth and -1 < y and y < gridheight and self.grid[x][y] != WALL and not self.is_in_closed(coord)

    def is_in_closed(self, coord): # if the cell is already in the closed list, return true
        for exist in self.closed:
            if coord == exist.coord:
                return True
        return False

    def is_in_open(self, cell): # if the cell isn't in the open list, return False
        for exist in range(len(self.open)):
            if self.open[exist] == cell: # if already exist, compare
                if cell < self.open[exist]:
                    self.open[exist] = cell

                return True

        return False

    def calculate_heuristic(self, coord): 
        # There are 4 ways to get H cost
        # 1. Manhattan distance
        # 2. euclidean distance
        # 3. chebyshev distance
        # 4. octile distance(new)
        x, y = coord
        endX, endY = self.end
        xDiff = abs(x - endX) * self.weight
        yDiff = abs(y - endY) * self.weight

        if self.using == "manhattan":
            return xDiff + yDiff
        elif self.using == "euclidean":
            return math.sqrt(xDiff ** 2 + yDiff ** 2)
        elif self.using == "chebyshev":
            return max(xDiff, yDiff)
        elif self.using == "octile":
            return min(xDiff, yDiff) * math.sqrt(2) + max(xDiff, yDiff) - min(xDiff, yDiff)

    def neighbours(self, cell):
        # visit neighbors(4 or 8 directions)
        #     TOPLEFT   UP   TOPRIGHT
        #        LEFT  HEAD  RIGHT
        #  BOTTOMLEFT  DOWN  BOTTOMRIGHT
        up = add(cell.coord, UP)
        down = add(cell.coord, DOWN)
        right = add(cell.coord, RIGHT)
        left = add(cell.coord, LEFT)
        display = []
        if self.diagonal: # if user allowed diagonal lines, visit 8 directions
            topright = add(cell.coord, TOPRIGHT)
            topleft = add(cell.coord, TOPLEFT)
            bottomright = add(cell.coord, BOTTOMRIGHT)
            bottomleft = add(cell.coord, BOTTOMLEFT)

            if self.is_valid(topright):
                neighbour = Cell(topright)
                neighbour.parent = cell.coord
                neighbour.G = cell.G + 14
                neighbour.H = self.calculate_heuristic(neighbour.coord)
                neighbour.F = neighbour.G + neighbour.H
                if not self.is_in_open(neighbour):
                    if self.open_is_heapq:
                        heapq.heappush(self.open, neighbour)
                    else:
                        self.open.append(neighbour) # if the open list is list
            
            if self.is_valid(topleft):
                neighbour = Cell(topleft)
                neighbour.parent = cell.coord
                neighbour.G = cell.G + 14
                neighbour.H = self.calculate_heuristic(neighbour.coord)
                neighbour.F = neighbour.G + neighbour.H
                if not self.is_in_open(neighbour):
                    if self.open_is_heapq:
                        heapq.heappush(self.open, neighbour)
                    else:
                        self.open.append(neighbour) # if the open list is list
            
            if self.is_valid(bottomright):
                neighbour = Cell(bottomright)
                neighbour.parent = cell.coord
                neighbour.G = cell.G + 14
                neighbour.H = self.calculate_heuristic(neighbour.coord)
                neighbour.F = neighbour.G + neighbour.H
                if not self.is_in_open(neighbour):
                    if self.open_is_heapq:
                        heapq.heappush(self.open, neighbour)
                    else:
                        self.open.append(neighbour) # if the open list is list   

            if self.is_valid(bottomleft):
                neighbour = Cell(bottomleft)
                neighbour.parent = cell.coord
                neighbour.G = cell.G + 14
                neighbour.H = self.calculate_heuristic(neighbour.coord)
                neighbour.F = neighbour.G + neighbour.H
                if not self.is_in_open(neighbour):
                    if self.open_is_heapq:
                        heapq.heappush(self.open, neighbour)
                    else:
                        self.open.append(neighbour) # if the open list is list
        
        if self.is_valid(up):
            neighbour = Cell(up)
            neighbour.parent = cell.coord
            neighbour.G = cell.G + 10 
            neighbour.H = self.calculate_heuristic(neighbour.coord)
            neighbour.F = neighbour.G + neighbour.H # F-cost = G-cost + H-cost
            if not self.is_in_open(neighbour): # if neighbor doesn't exist in the open list, push
                if self.open_is_heapq:
                    heapq.heappush(self.open, neighbour)
                else:
                    self.open.append(neighbour) # if the open list is list

        if self.is_valid(down):
            neighbour = Cell(down)
            neighbour.parent = cell.coord
            neighbour.G = cell.G + 10
            neighbour.H = self.calculate_heuristic(neighbour.coord)
            neighbour.F = neighbour.G + neighbour.H
            if not self.is_in_open(neighbour):
                if self.open_is_heapq:
                    heapq.heappush(self.open, neighbour)
                else:
                    self.open.append(neighbour) # if the open list is list
        if self.is_valid(right):
            neighbour = Cell(right)
            neighbour.parent = cell.coord
            neighbour.G = cell.G + 10
            neighbour.H = self.calculate_heuristic(neighbour.coord)
            neighbour.F = neighbour.G + neighbour.H
            if not self.is_in_open(neighbour):
                if self.open_is_heapq:
                    heapq.heappush(self.open, neighbour)
                else:
                    self.open.append(neighbour) # if the open list is list

        if self.is_valid(left):
            neighbour = Cell(left)
            neighbour.parent = cell.coord
            neighbour.G = cell.G + 10
            neighbour.H = self.calculate_heuristic(neighbour.coord)
            neighbour.F = neighbour.G + neighbour.H
            if not self.is_in_open(neighbour):
                if self.open_is_heapq:
                    heapq.heappush(self.open, neighbour)
                else:
                    self.open.append(neighbour) # if the open list is list
        
        if not self.open_is_heapq:
            self.open = sorted(self.open) # if the open list is list

    def find(self):
        no_path = True # flag

        cell = Cell(self.start) # the first cell is starting point
        if self.open_is_heapq:
            heapq.heappush(self.open, cell) # push into the priority queue
        else:
            self.open.append(cell)

        while True: # find the shortest path
            for e in pg.event.get():
                if e.type == QUIT: # terminate the program
                    pg.quit()
                    sys.exit()

            if not self.open: break # if the open list is empty, break
            # print("---------------------")
            # print("current = ", cell.coord)
            # print("---------------------")
            # for o in self.open:
            #     print(o.coord, o.F, end = " ")
            # print("\n---------------------") # debugging
            
            if self.open_is_heapq:
                cell = heapq.heappop(self.open) # pop one cell with the smallest F-cost in the open list
            else:
                cell = self.open.pop(0) # if the open list is list

            # draw the process
            for o in self.open:
                if not (o.coord == self.start or o.coord == self.end):
                    o.draw(YELLOW)
            for c in self.closed:
                if not (c.coord == self.start or c.coord == self.end):
                    c.draw(ORANGE)
            if not (cell.coord == self.start or cell.coord == self.end):
                cell.draw(BLUE)

            pg.time.delay(70) # delay

            self.closed.append(cell) # put the cell in the closed list
            if cell.coord == self.end: # if cell.coord is the destination(e.g. the ending point is in closed list), break
                no_path = False # found path 
                break

            self.neighbours(cell) # visit neighbors
        
        pg.time.delay(1000) # delay 1 sec
        
        if no_path: # if not found, return
            return

        while True: # if found the path, trace the parent coord
            if cell.coord == self.start: # if cell.coord is the starting point, done
                break
            
            # draw the found path
            if cell.coord != self.end:
                cell.draw(GREY)

            for exist in self.closed:
                if cell.parent == exist.coord:
                    cell = exist
                    break
            
        pg.time.delay(1500) # delay 1.5 sec

class Option:
    def __init__(self, coord, text):
        self.coord = coord
        self.text = text
        self.state = False # on, off
        self.circle = None # for event

    def txt(self): # set text
        x, y = self.coord
        x = (gridwidth + x + 1) * cellsize
        y = y * cellsize + 10
        
        obj = optionfont.render(self.text, True, WHITE)
        obj_rect = obj.get_rect()
        obj_rect.topleft = x, y
        screen.blit(obj, obj_rect)

    def draw(self):
        x, y = self.coord
        x = (gridwidth + x) * cellsize + (cellsize // 2)
        y = y * cellsize + (cellsize // 2)

        self.txt()
        if self.state:
            self.circle = pg.draw.circle(screen, RED, (x, y), cellsize // 4)
        else:
            self.circle = pg.draw.circle(screen, WHITE, (x, y), cellsize // 4)

    def is_clicked(self, pos):
        if self.circle.collidepoint(pos):
            return True
        return False

# --------------------------------------------
def add(one, another): 
    result = []
    for a, b in zip(one, another):
        result.append(a + b)
    return result

# --------------------------------------------
def txt(pos, text):
    x, y = pos
    x = (gridwidth + x) * cellsize + 10
    y = y * cellsize + 10
    obj = optionfont.render(text, True, WHITE)
    obj_rect = obj.get_rect()
    obj_rect.topleft = x, y
    screen.blit(obj, obj_rect)

def draw_grid(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == WALL:
                pg.draw.rect(screen, BLACK, (x * cellsize, y * cellsize, cellsize, cellsize))
            elif grid[x][y] == PATH:
                pg.draw.rect(screen, WHITE, (x * cellsize, y * cellsize, cellsize, cellsize))
                pg.draw.rect(screen, BLACK, (x * cellsize, y * cellsize, cellsize, cellsize), 1) # outline
            elif grid[x][y] == START:
                pg.draw.rect(screen, RED, (x * cellsize, y * cellsize, cellsize, cellsize))
                pg.draw.rect(screen, BLACK, (x * cellsize, y * cellsize, cellsize, cellsize), 1)
            elif grid[x][y] == END:
                pg.draw.rect(screen, GREEN, (x * cellsize, y * cellsize, cellsize, cellsize))
                pg.draw.rect(screen, BLACK, (x * cellsize, y * cellsize, cellsize, cellsize), 1)

def draw_menu(options, diagonal, weight, open_is_heapq):
    for option in options: # draw options
        option.draw()
    diagonal.draw()
    open_is_heapq.draw()

    txt([0, 10], "press left") # explain how to control weight
    txt([0, 11], ", right key")
    weighttxt = "weight : "
    txt([0, 12], weighttxt + str(weight))
    txt([0, gridheight - 1], " PRESS ENTER") # explain how to start

# --------------------------------------------
def execute():
    # initialize grid settings
    grid = [[PATH for y in range(gridheight)] for x in range(gridwidth)] # create
    grid[0][0] = START # set the starting point
    start = 0, 0
    grid[gridwidth - 1][gridheight - 1] = END # set the ending point
    end = gridwidth - 1, gridheight - 1
    
    # initialize menu
    manhattan = Option([0, 1], "manhattan")
    manhattan.state = True
    using = manhattan.text
    euclidean = Option([0, 2], "euclidean")
    chebyshev = Option([0, 3], "chebyshev")
    octile = Option([0, 4], "octile")
    options = [manhattan, euclidean, chebyshev, octile]
    diagonal = Option([0, 7], "diagonal")
    diagonal.state = True
    weight = 10
    open_is_heapq = Option([0, 8], "using heapq")
    open_is_heapq.state = False

    # clicked 
    is_cell_clicked = False
    is_start_clicked = False
    is_end_clicked = False
    change = []

    is_running = True
    while is_running:
        pos = pg.mouse.get_pos()
        x, y = (pos[0] // cellsize, pos[1] // cellsize)

        for e in pg.event.get():
            if e.type == QUIT: # terminate the program
                pg.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_RETURN: # find the shortest path                    
                    Astar(grid, start, end, weight, using, diagonal.state, open_is_heapq.state).find()

                elif e.key == K_LEFT: # weight --
                    if 1 < weight:
                        weight = weight - 2
                elif e.key == K_RIGHT: # weight ++
                    if weight < weightlimit - 1:
                        weight = weight + 2

            elif e.type == MOUSEBUTTONDOWN: # click
                if x < gridwidth:
                    if (x, y) == start:
                        is_start_clicked = True
                    elif (x, y) == end:
                        is_end_clicked = True
                    else:
                        change.append([x, y])
                        if grid[x][y] == WALL:
                            grid[x][y] = PATH
                        elif grid[x][y] == PATH:
                            grid[x][y] = WALL 
                        is_cell_clicked = True 

                for option in options: # radio button
                    if option.is_clicked(pos):
                        option.state = True
                        using = option.text
                        for opt in options:
                            if opt.coord != option.coord:
                                opt.state = False

                if diagonal.is_clicked(pos): # check box
                    if diagonal.state:
                        diagonal.state = False
                    else:
                        diagonal.state = True
                
                if open_is_heapq.is_clicked(pos):
                    if open_is_heapq.state:
                        open_is_heapq.state = False
                    else:
                        open_is_heapq.state = True

            elif e.type == MOUSEMOTION: # move
                if x < gridwidth:
                    if is_cell_clicked:
                        if [x, y] not in change:    
                            change.append([x, y])
                            if grid[x][y] == WALL:
                                grid[x][y] = PATH
                            elif grid[x][y] == PATH:
                                grid[x][y] = WALL
                    elif is_start_clicked and not ((x, y) == end):
                        if grid[x][y] != WALL:
                            grid[start[0]][start[1]] = PATH
                            grid[x][y] = START
                            start = x, y
                    elif is_end_clicked and  not ((x, y) == start):
                        if grid[x][y] != WALL:
                            grid[end[0]][end[1]] = PATH
                            grid[x][y] = END
                            end = x, y               

            elif e.type == MOUSEBUTTONUP: # release
                if is_cell_clicked:
                    change = []
                    is_cell_clicked = False
                elif is_start_clicked:
                    is_start_clicked = False
                elif is_end_clicked:
                    is_end_clicked = False
        
        screen.fill(BLACK) # background

        draw_grid(grid)
        draw_menu(options, diagonal, weight, open_is_heapq)

        pg.display.flip() # update the screen
        pg.time.Clock().tick(FPS) # fps
 
# --------------------------------------------
if __name__ == "__main__":
    execute()