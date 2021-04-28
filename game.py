import pygame
import chess
import os

def make_matrix(board):
       pgn = board.epd()
       foo = []
       pieces = pgn.split(" ", 1)[0]
       rows = pieces.split("/")
       for row in rows:
           foo2 = []
           for thing in row:
               if thing.isdigit():
                   for i in range(0, int(thing)):
                       foo2.append('.')
               else:
                   foo2.append(thing)
           foo.append(foo2)
       return foo

board = chess.Board()
pygame.init()

screen = pygame.display.set_mode([700, 700])
seguisy80 = pygame.font.SysFont("segoeuisymbol", 70)

image_dir = os.path.abspath("images")
bP = pygame.image.load(os.path.join(image_dir, 'bP.png'))

def draw_board(screen):
    flag = False
    x = 0
    y = 0
    step = 70
    for i in range(10):
        for j in range(10):
            if flag:
                pygame.draw.rect(screen, (202, 179, 159), (x, y, step, step))
                flag = False
            else:
                pygame.draw.rect(screen, (64, 37, 18), (x, y, step, step))
                flag = True
            x+= step
        flag = not flag
        y += step
        x = 0
    
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 700, 70))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 70, 700))
    pygame.draw.rect(screen, (255, 255, 255), (0, 630, 700, 70))
    pygame.draw.rect(screen, (255, 255, 255), (630, 0, 70, 700))
    pygame.draw.rect(screen, (0, 0, 0), (70, 70, 560, 560), 8)
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 700, 700), 8)

    x = 82
    y = -15
    AA = "A"
    for i in range(8):
        A = seguisy80.render(chr(ord(AA) + i), True, (0,0,0))
        screen.blit(A, (x, y))
        x+=step
    
    x = 20
    y = 55
    AA = "1"
    for i in range(8):
        A = seguisy80.render(chr(ord(AA) + i), True, (0,0,0))
        screen.blit(A, (x, y))
        y+=step
    
    matrix = make_matrix(board)

    for i in range(8):
        for j in range(8):
            if matrix[i][j] == "p":
                screen.blit(bP, ((j+1)*70, (i+1)*70))





# Run until the user asks to quit
running = True
draw_board(screen)
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            second_pos = pos
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    second_pos = pygame.mouse.get_pos()
                    break
            print(pos, second_pos)
            
    pygame.display.flip()

    
