from asyncio import windows_events
from turtle import window_height
import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
TIGERMINSIZE = 30
TIGERMAXSIZE = 50
TIGERMINSPEED = 1
TIGERMAXSPEED = 2
ADDNEWTIGERRATE = 40
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.type == K_ESCAPE: # Người chơi ấn ESC thoát game
                    terminate()
                return

def playerHasHitTiger(playerRect, tigers):
    for t in tigers:
        if playerRect.colliderect(t["rect"]):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Thiet lap pygame, cua so game, va chuot
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Run for life")
pygame.mouse.set_visible(False)

# Thiet lap fonts
font = pygame.font.SysFont(None, 48)

# Thiet lap am thanh
gameOverSound = pygame.mixer.Sound("gameover.mp3")
pygame.mixer.music.load("background.mp3")

# Thiet lap hinh anh
playerImage = pygame.image.load("player.png")
playerRect = playerImage.get_rect()
tigerImage = pygame.image.load("tiger.png")

# Hien thi man hinh Bat dau tro choi
drawText("THE SQUIRREL AND TIGERS", font, windowSurface, (WINDOWWIDTH / 4), (WINDOWHEIGHT / 3))
drawText("Press a key to start", font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # Thiet lap luc bat dau game
    tigers = []
    score = 0 
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    tigerAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # Vong lap game chay khi mot phan cua game dang choi
        score += 1 # Tang diem cua nguoi choi

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord("z"):
                    reverseCheat = True
                if event.key == ord("x"):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord("a"):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord("d"):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord("w"):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord("s"):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord("z"):
                    reverseCheat = False
                    score = 0
                if event.key == ord("x"):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord("a"):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord("d"):
                    moveRight = False
                if event.key == K_UP or event.key == ord("w"):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord("s"):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # Neu nguoi  choi di chuyen chuot, chuyen nhan vat den cho tro chuot
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        #Them nhieu ho o phia tren man hinh game, neu can thiet
        if not reverseCheat and not slowCheat:
            tigerAddCounter += 1
        if tigerAddCounter == ADDNEWTIGERRATE:
            tigerAddCounter = 0
            tigerSize = random.randint(TIGERMINSIZE, TIGERMAXSIZE)
            newTiger = {"rect" : pygame.Rect(random.randint(0, WINDOWWIDTH-tigerSize), 0 - tigerSize, tigerSize, tigerSize),
            "speed" : random.randint(TIGERMINSPEED, TIGERMAXSPEED),
            "surface" : pygame.transform.scale(tigerImage, (tigerSize, tigerSize)), }
            tigers.append(newTiger)

        # di chuyen nhan vat
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Di chuyen con tro chuot de phoi hop voi nhan vat
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # di chuyen ho xuong
        for t in tigers:
            if not reverseCheat and not slowCheat:
                t["rect"].move_ip(0, t["speed"])
            elif reverseCheat:
                t["rect"].move_ip(0, -5)
            elif slowCheat:
                t["rect"].move_ip(0, 1)

        # Xoa nhung con ho va cham voi day
        for t in tigers:
            if t["rect"].top > WINDOWHEIGHT:
                tigers.remove(t)
                    
        # Ve giao dien game tren cua so game
        windowSurface.fill(BACKGROUNDCOLOR)
        # Thiet lap diem so tro choi va diem cao nhat
        drawText("Score: %s" %(score), font, windowSurface, 10, 0)
        drawText("Top Score: %s" % (topScore), font, windowSurface, 10, 40)

        # Ve khoi chu nhat cua nhan vat
        windowSurface.blit(playerImage, playerRect)
        
        # Ve tung con ho
        for t in tigers:
            windowSurface.blit(t["surface"], t["rect"])
        
        pygame.display.update()

        # Kiem tra neu ho va cham nhan vat
        if playerHasHitTiger(playerRect, tigers):
            if score > topScore:
                topScore = score # thiet lap diem cao nhat moi
            break

        mainClock.tick(FPS)

    # Dung game va hien thi Game Over ra man hinh
    pygame.mixer.music.stop()
    gameOverSound.play()
    drawText("GAME OVER", font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT/3))
    drawText("Press a key to play again", font, windowSurface, (WINDOWWIDTH/3) -80, (WINDOWHEIGHT/3) +50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()








