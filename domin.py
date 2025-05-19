FLAGNUM = 14
SIZE = 10

from datetime import datetime
import pygame, sys, random
from pygame.locals import *
import time

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 150,   0)
BLUE  = (  0,   0, 255)
NUM4  = (0,129,255)
NUM5 = (129,0,1)
NUM6 = (127,128,255)
NUM7 = (127,128,255)
NUM8 = (127,128,255)


numcol = [BLACK, BLUE, GREEN, RED, NUM4, NUM5, NUM6, NUM7, NUM8]

dx = [0, 1, 1, 1, 0, -1, -1, -1]
dy = [1, -1, 0, 1, -1, -1, 0, 1]

a = [[0 for j in range(SIZE)] for i in range(SIZE)]

time_start = time.time()

check = [[0 for i in range(SIZE)] for i in range(SIZE)] # 0: free, 1: flag, 2: opened
demflag = FLAGNUM
demchon = SIZE * SIZE - FLAGNUM


# tạo window
pygame.display.set_caption('Game do min - LogN')
pygame.init()
DISPLAYSURF = pygame.display.set_mode((50*SIZE+200, 50*SIZE))

def print_board():
    # vẽ ô
    DISPLAYSURF.fill(WHITE)
    for i in range(1, SIZE):
        pygame.draw.line(DISPLAYSURF, BLACK, (0, i*50), (50*SIZE, i*50), 1)
        pygame.draw.line(DISPLAYSURF, BLACK, (i*50, 0), (i*50, 50*SIZE), 1)
    pygame.draw.line(DISPLAYSURF, BLACK, (50*SIZE, 0), (50*SIZE, 50*SIZE), 3)
    pygame.display.update()

def Print(mess, Size, Font, Bold, Color, x, y):
    font = pygame.font.SysFont(Font, Size, Bold)
    commentSuface = font.render(mess, True, Color)
    DISPLAYSURF.blit(commentSuface, (x, y))
    pygame.display.update()


def print_mess():
    # vẽ flags
    Print('Flags:', 50, 'consolas', 1, BLACK, 50*SIZE + 10, 10)
    Print(str(FLAGNUM), 50, 'consolas', 1, BLACK, 50*SIZE + 10, 60)
    # vẽ thời gian
    Print('Time:', 50, 'consolas', 1, BLACK, 50*SIZE + 10, 110)
    # Print(str(datetime.now().strftime("%M:%S")), 50, 'consolas', 1, BLACK, 50*SIZE + 10, 260)
    # vẽ count
    Print('Count:', 50, 'consolas', 1, BLACK, 50*SIZE + 10, 210)
    Print(str(SIZE * SIZE - FLAGNUM), 50, 'consolas', 1, BLACK, 50*SIZE + 10, 260)
    # vẽ hint
    Print('Hint!', 50, 'consolas', 1, BLUE, 50*SIZE + 10, 310)

def inside(x, y):
    return 0 <= x < SIZE and 0 <= y < SIZE

def dembom(x, y):
    cnt = 0
    for i in range(8):
        u = x + dx[i]
        v = y + dy[i]
        if inside(u, v) and a[u][v] == 'X':
            cnt += 1
    return cnt

def random_flag():
    global a
    a = [[0 for j in range(SIZE)] for i in range(SIZE)]
    for z in range(FLAGNUM):
        i = random.randint(0, SIZE - 1)
        j = random.randint(0, SIZE - 1)
        while a[i][j] == 'X':
            i = random.randint(0, SIZE - 1)
            j = random.randint(0, SIZE - 1)
        a[i][j] = 'X'
    for i in range(SIZE):
        for j in range(SIZE):
            if a[i][j] == 0:
                a[i][j] = dembom(i, j)

def show(x, y): # hiển thị số cho ô (x, y)
    font = pygame.font.SysFont('consolas', 60, 2)
    if a[x][y] == 'X':
        commentSuface = font.render(str(a[x][y]), True, RED)
    else:
        commentSuface = font.render(str(a[x][y]), True, numcol[a[x][y]])

    DISPLAYSURF.blit(commentSuface, (x*50+5, y*50))
    pygame.display.update()


def showflag():
    pygame.draw.rect(DISPLAYSURF, WHITE, (50*SIZE + 10, 60, 100, 50))
    Print(str(demflag), 50, 'consolas', 1, BLACK, 50*SIZE + 10, 60)
    pygame.draw.rect(DISPLAYSURF, WHITE, (50*SIZE + 10, 260, 100, 50))
    Print(str(demchon), 50, 'consolas', 1, BLACK, 50*SIZE + 10, 260)
    pygame.display.update()

def show2(x, y):
    # vẽ cờ *
    font = pygame.font.SysFont('consolas', 60, 2)
    commentSuface = font.render('*', True, BLACK)
    commentSize = commentSuface.get_size()
    DISPLAYSURF.blit(commentSuface, (x*50+5, y*50+8))
    pygame.display.update()

firsttime = 0
def click(x, y):
    global firsttime, a
    firsttime += 1
    if check[x][y] == 2:
        return

    if check[x][y] == 1:
        erase(x, y)
        global demflag
        demflag -= 1
        showflag()

    global demchon
    demchon -= 1
    check[x][y] = 2
    show(x, y)
    showflag()

    if a[x][y] == 0:
        for i in range(8):
            u = x + dx[i]
            v = y + dy[i]
            if inside(u, v):
                click(u, v)

    if a[x][y] == 'X':
        if firsttime == 1:
            reset()
            return

        Print('YOU LOSE !!!', 100, 'consolas', 2, RED, 50, 200)
        pygame.display.update()
        time.sleep(5)
        reset()

    if demchon == 0:
        Print('YOU WIN !!!', 100, 'consolas', 2, RED, 50, 200)
        pygame.display.update()
        time.sleep(5)
        reset()

def erase(x, y): # xóa ô (x, y)
    check[x][y] = 0
    pygame.draw.rect(DISPLAYSURF, WHITE, (x*50+1, y*50+1, 49, 49))
    pygame.display.update()

def flag(x, y):
    if check[x][y] == 2:
        return
    global demflag
    if check[x][y] == 1:
        erase(x, y)
        demflag += 1
        showflag()
        return
    if demflag > 0:
        check[x][y] = 1
        demflag -= 1
        show2(x, y)
        showflag()

def hint():
    for i in range(SIZE):
        for j in range(SIZE):
            if check[i][j] == 2 and a[i][j] != 0:
                cntsafe = 0    
                cntinside = 0
                cntbom = 0
                for k in range(8):
                    x = i + dx[k]
                    y = j + dy[k]
                    if inside(x, y):
                        cntinside += 1
                        if check[x][y] == 2:
                            cntsafe += 1
                        if check[x][y] == 1:
                            cntbom += 1
                if cntsafe + a[i][j] == cntinside:
                    pygame.draw.rect(DISPLAYSURF, RED, ((x + 1)*50+1, (y - 1)*50+1, 49, 49), 3)
                if cntbom == a[i][j]:
                    pygame.draw.rect(DISPLAYSURF, BLUE, ((x + 1)*50+1, (y - 1)*50+1, 49, 49), 3)

def reset():
    global time_start, firsttime
    firsttime = 0
    time_start = int(time.time())
    global check, demflag, demchon
    check = [[0 for i in range(SIZE)] for i in range(SIZE)]
    demflag = FLAGNUM
    demchon = SIZE * SIZE - FLAGNUM
    print_board()
    random_flag()
    print_mess()

def main():
    running = True
    pygame.display.update()
    reset()
    while running:
        pygame.draw.rect(DISPLAYSURF, WHITE, (50*SIZE + 10, 160, 200, 50))
        Print(str(int(time.time() - time_start)), 50, 'consolas', 1, BLACK, 50*SIZE + 10, 160)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                exit(0) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    vt = pygame.mouse.get_pos()
                    x, y = vt[0] // 50, vt[1] // 50
                    if inside(x, y):
                        click(x, y)
                    if 50*SIZE + 10 <= vt[0] and 310 <= vt[1] :
                        hint()
                if pygame.mouse.get_pressed()[2]:
                    vt = pygame.mouse.get_pos()
                    x, y = vt[0] // 50, vt[1] // 50
                    if inside(x, y):
                        flag(x, y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit() 
                    exit(0)
main()