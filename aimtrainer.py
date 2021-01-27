''' Own personal aim trainer using pygame '''

import pygame, sys
import random
from pygame.locals import *
import math
from tkinter import *


def game():
    ''' Main function that handles entire game '''
    # initialize pygame
    pygame.init()

    # set frames per second
    FPS = 60
    fpsClock = pygame.time.Clock()

    # create display surface and set caption
    DISPLAYSURF = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Personalized Aim Trainer')

    # initialize main menu
    gameMode1Rect, gameMode2Rect = main_menu(DISPLAYSURF, False)
    
    # variables to use in main game loop
    gameStarted = False
    gameMode = None
    r,g,b = 0,0,0
    mousex, mousey = 0,0
    mouseClicked = False
    total_targets = 10
    targets_remaining = 10
    targets_scored = 0
    radius = 13
    x,y = 400,300
    start = None

    while True:  # main game loop          
        if mouseClicked:
            targets_remaining -= 1
            x, y = newTarget(DISPLAYSURF, x, y, radius, gameMode, targets_remaining)
            mouseClicked = False

        if targets_remaining == 0:
            end_screen(DISPLAYSURF, start, targets_scored, total_targets)
            gameMode1Rect, gameMode2Rect = main_menu(DISPLAYSURF, False)
            
            # reset critical variables
            gameStarted = False
            x, y = 400, 300
            targets_remaining = total_targets
            targets_scored = 0

        if not gameStarted:
            main_menu(DISPLAYSURF, True)
            for _ in range(5):
                crosshair = pygame.image.load('crosshair revamped.png')
                rand_x, rand_y = random.randint(5,795), random.randint(5,595)
                DISPLAYSURF.blit(crosshair, (rand_x,rand_y))

            mousex, mousey = pygame.mouse.get_pos()
            if mousex >= gameMode1Rect.topleft[0] and mousex <= gameMode1Rect.topright[0] and \
                mousey >= gameMode1Rect.topleft[1] and mousey <= gameMode1Rect.bottomright[1]:
                fontObj = pygame.font.SysFont('cooper black', 30)
                textSurfaceObj = fontObj.render('Reaction Training', True, (255,0,0), (0,0,0))
                gameMode1Rect = textSurfaceObj.get_rect()
                gameMode1Rect.center = (400, 250)
                DISPLAYSURF.blit(textSurfaceObj, gameMode1Rect)

            elif mousex >= gameMode2Rect.topleft[0] and mousex <= gameMode2Rect.topright[0] and \
                mousey >= gameMode2Rect.topleft[1] and mousey <= gameMode2Rect.bottomright[1]:
                fontObj = pygame.font.SysFont('cooper black', 30)
                textSurfaceObj = fontObj.render('Flicking Training', True, (255,0,0), (0,0,0))
                gameMode2Rect = textSurfaceObj.get_rect()
                gameMode2Rect.center = (400, 350)
                DISPLAYSURF.blit(textSurfaceObj, gameMode2Rect)
            
            else:
                draw_menu_buttons(DISPLAYSURF)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif (event.type == KEYUP and event.key == K_ESCAPE) and gameStarted:  #implement pause menu
                pass
            
            elif event.type == MOUSEMOTION and gameStarted:
                mousex, mousey = event.pos
                DISPLAYSURF.fill((0,0,0))
                pygame.draw.circle(DISPLAYSURF, (0,0,255), (x, y), radius, 0)
                crosshair = pygame.image.load('crosshair revamped.png')
                DISPLAYSURF.blit(crosshair, (mousex,mousey))
            
            elif event.type == MOUSEMOTION and not gameStarted:
                pass

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if gameStarted:
                    soundObj = pygame.mixer.Sound('gunshot.wav')
                    soundObj.play()

                    crosshair = pygame.image.load('crosshair revamped.png')
                    DISPLAYSURF.blit(crosshair, (mousex,mousey))
                    mouseClicked = True
                    
                    if math.sqrt(((mousex - x) ** 2) + ((mousey - y) ** 2)) < radius:
                        targets_scored += 1
                        pygame.draw.circle(DISPLAYSURF, (255,0,0), (x, y), radius, 0)
                    else:
                        DISPLAYSURF.fill((255,0,0))

                else:
                    if mousex >= gameMode1Rect.topleft[0] and mousex <= gameMode1Rect.topright[0] and \
                        mousey >= gameMode1Rect.topleft[1] and mousey <= gameMode1Rect.bottomright[1]:
                        # switch to reaction time game mode
                        gameMode = 1
                        setGameMode(DISPLAYSURF, x, y, radius)
                        start = pygame.time.get_ticks()
                        gameStarted = True

                    elif mousex >= gameMode2Rect.topleft[0] and mousex <= gameMode2Rect.topright[0] and \
                        mousey >= gameMode2Rect.topleft[1] and mousey <= gameMode2Rect.bottomright[1]:
                        # switch to flicking game mode
                        gameMode = 2
                        setGameMode(DISPLAYSURF,x,y, radius)
                        start = pygame.time.get_ticks()
                        gameStarted = True
                    
                            
        pygame.display.update()
        fpsClock.tick(FPS)

def main_menu(surf, music_started):
    ''' Initializes the main menu '''
    background = pygame.image.load('background.jpg')
    surf.blit(background, (0, 0))

    if not music_started:
        pygame.mixer.music.load('music_zapsplat_lazy_days_137.mp3')
        pygame.mixer.music.play(-1,0.0)

    # menu header
    fontObj = pygame.font.SysFont('cooper black', 70)
    textSurfaceObj = fontObj.render("AIM EXERCISES", True, (255,255,255), (0,0,0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 60)
    surf.blit(textSurfaceObj, textRectObj)

    rects = draw_menu_buttons(surf)
    pygame.display.update()
    
    return rects

def draw_menu_buttons(surf):
    ''' Draws menu buttons '''
    # reaction time game mode option
    fontObj = pygame.font.SysFont('cooper black', 30)
    textSurfaceObj = fontObj.render('Reaction Training', True, (0,255,255), (0,0,0))
    gameMode1Rect = textSurfaceObj.get_rect()
    gameMode1Rect.center = (400, 250)
    surf.blit(textSurfaceObj, gameMode1Rect)

    # game mode 2 - my version of spidershot
    fontObj = pygame.font.SysFont('cooper black', 30)
    textSurfaceObj = fontObj.render('Flicking Training', True, (0,255,255), (0,0,0))
    gameMode2Rect = textSurfaceObj.get_rect()
    gameMode2Rect.center = (400, 350)
    surf.blit(textSurfaceObj, gameMode2Rect)

    return (gameMode1Rect, gameMode2Rect)
        
def setGameMode(surf, x, y, radius):
    ''' Switch to appropriate game mode and initialize display '''
    surf.fill((0,0,0))

    fontObj = pygame.font.SysFont('cooper black', 40)
    textSurfaceObj = fontObj.render('Starting in 5 seconds!', True, (255,255,255), (0,0,0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 300)
    surf.blit(textSurfaceObj, textRectObj)

    pygame.mouse.set_visible(False)

    pygame.display.update()
    pygame.mixer.music.stop()
    pygame.time.wait(5000)

    surf.fill((0,0,0))
    pygame.draw.circle(surf, (0,0,255), (x, y), radius, 0)
    pygame.mouse.set_pos([400,300])


def newTarget(surf, x, y, radius, mode, targets_left):
    ''' Draw new target on mouse click. Position (and, later, size) depends
        on game mode '''
    surf.fill((0,0,0))
    pygame.draw.circle(surf, (0,0,0), (x, y), radius, 0)

    if not mode % 2 and not targets_left % 2:
        x, y = 400, 300
    else:
        x,y = random.randint(100, 700), random.randint(100,500)
    
    pygame.draw.circle(surf, (0,0,255), (x, y), radius, 0)
    return (x, y)

def end_screen(surf, start_time, targets_scored, total_targets):
    ''' Display screen for when game mode is completed '''
    end = pygame.time.get_ticks()
    surf.fill((0,0,0))
    pygame.mouse.set_visible(True)

    pygame.mixer.music.load('end_screen_music.mp3')
    pygame.mixer.music.play(-1,0.0)

    final_score = "Your accuracy was " + str(round(targets_scored/total_targets * 100, 2)) + "%"
    fontObj = pygame.font.SysFont('cooper black', 40)
    textSurfaceObj = fontObj.render(final_score, True, (255,255,255), (0,0,0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 280)
    surf.blit(textSurfaceObj, textRectObj)

    time_taken = "Your final time was " + str(round((end - start_time)/1000, 2)) + " seconds."
    fontObj = pygame.font.SysFont('cooper black', 40)
    textSurfaceObj = fontObj.render(time_taken, True, (255,255,255), (0,0,0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 340)
    surf.blit(textSurfaceObj, textRectObj)

    pygame.display.update()
    pygame.time.wait(8000)
    pygame.mixer.music.stop()

    surf.fill((0,0,0))
    pygame.display.update()

    

if __name__ == "__main__":
    game()