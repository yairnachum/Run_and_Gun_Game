import math
import random
import pygame
from pygame import VIDEORESIZE

# Finals
width = 1200
height = 800
fps_cap = 30
ground = 530

# Title and Icon
pygame.display.set_caption("Space Runner")
icon = pygame.image.load('space runner logo.png')
pygame.display.set_icon(icon)

# Images
background = pygame.image.load('newBG.png')
bg_width = background.get_width()
restart_button = pygame.image.load('Asset 2.png')
quit_button = pygame.image.load('Asset 3.png')
playerImg = pygame.image.load('newCharacter.png')
playerJump = pygame.image.load('characterJumping.png')
playerSlide = pygame.image.load('characterSliding.png')
shieldImg = pygame.image.load('shield.png')
shieldStateActive = pygame.image.load('shield.png')
shieldStateNotActive = pygame.image.load('shieldNotActivated.png')
gameOverImg = pygame.image.load('Asset 1.png')

# Scrolling variables
tiles = math.ceil(width / bg_width) + 1
scroll = 0
fullscreen = False

# Initialize the game
pygame.init()

# Sounds
bgsound = pygame.mixer.Sound('background.wav')
bgsound.set_volume(0.05)
bgsound.play(-1)
laserSound = pygame.mixer.Sound('laser.wav')
laserSound.set_volume(0.075)
explosionSound = pygame.mixer.Sound('explosion.wav')
explosionSound.set_volume(0.045)

# Creating the screen
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Initializing the player
playerX = 300
playerY = ground
playerY_slide = ground + 40
gravity = 5
jumpHeight = 50
jumpVelocity = 50
jumping = False
sliding = False


def player():
    if playerY <= 0:
        screen.blit(playerJump, (playerX, 0))
    elif jumping:
        screen.blit(playerJump, (playerX, playerY))
    elif sliding:
        screen.blit(playerSlide, (playerX, playerY))
    else:
        screen.blit(playerImg, (playerX, playerY))


# end of player


# enemies
ufoImg = []
enemyX = []
enemyY = []
ufoVelocity = 5
num_of_enemies = 3

for i in range(num_of_enemies):
    ufoImg.append(pygame.image.load('ufo.png'))
    enemyX.append(1200)
    enemyY.append(random.randint(50, ground))


def enemy():
    for j in range(num_of_enemies):
        screen.blit(ufoImg[j], (enemyX[j], enemyY[j]))


# end of enemies

# shield
shieldX = random.randint(width, width*6)
shieldY = random.randint(0, ground - 50)
shieldVelocity = 5
shieldActivated = False


def shield():
    if not shieldActivated:
        screen.blit(shieldImg, (shieldX, shieldY))


# end of shield

# bullets
bulletImg = []
bulletY = []
bulletX = []
bulletVelocity = []
bulletIsShot = []
magazineSize = 3
for i in range(magazineSize):
    bulletImg.append(pygame.image.load('laserNew.png'))
    bulletY.append(playerY + 25)
    bulletX.append(360)
    bulletVelocity.append(25)
    bulletIsShot.append(False)


def bullet(j):
    screen.blit(bulletImg[j], (bulletX[j] + bulletVelocity[j], bulletY[j]))


# end of bullets


# button class
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def isPressed(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return pygame.mouse.get_pressed()[0]


# end of button class


# Collision check
def bulletHit(j):
    if bulletIsShot[j]:
        for k in range(num_of_enemies):
            distance = math.sqrt(
                math.pow(enemyX[k] - (bulletX[j] + bulletVelocity[j]), 2) + math.pow(enemyY[k] - bulletY[j], 2))
            if distance < 36:
                return [True, k]
    return [False, -1]


def ufoHit(j):
    distance = math.sqrt(math.pow(enemyX[j] - playerX, 2) + math.pow(enemyY[j] - playerY, 2))
    if distance < 64:
        return True
    return False


def shieldCollected():
    distance = math.sqrt(math.pow(playerX - shieldX, 2) + math.pow(playerY - shieldY, 2))
    if distance < 64:
        return True
    return False
# end of collision check


# Score
scoreValue = 0
font = pygame.font.Font('GillSans.ttc', 64)
textX = 20
textY = 20


def displayScore():
    score = font.render("score: " + str(scoreValue), True, (65, 225, 242))
    screen.blit(score, (textX, textY))


def displayShieldState():
    if shieldActivated:
        screen.blit(shieldStateActive, (20, 100))
    else:
        screen.blit(shieldStateNotActive, (20, 100))


# game over screen
game_over_font = pygame.font.Font('GillSans.ttc', 75)
game_over = False


def gameOverScreen():
    score = font.render("score:" + str(scoreValue), True, (65, 225, 242))
    screen.blit(gameOverImg, (width/2 - 300, height/2 - 120))
    screen.blit(score, (width / 2 - 110, height / 2))


quitButton = Button(width / 2 + width / 48, height / 2 + height / 8, quit_button)
restartButton = Button(width / 2 - width / 12, height / 2 + height / 8, restart_button)
# end of game over screen


running = True
while running:
    clock.tick(fps_cap)

    # ending the Game
    if game_over:
        gameOverScreen()
        quitButton.draw()
        restartButton.draw()
        for event in pygame.event.get():
            if restartButton.isPressed():
                print("clicked")
                game_over = False
                playerY = ground
                scoreValue = 0
                shieldX = random.randint(width, width*6)
                jumping = False
                sliding = False
                for i in range(num_of_enemies):
                    enemyX[i] = width
                    enemyY[i] = random.randint(50, ground)
                    bulletY[i] = playerY + 25
                    bulletX[i] = 360
                    bulletVelocity[i] = 25
                    bulletIsShot[i] = False
            if quitButton.isPressed():
                running = False
                print("quit")
    # end of ending the game

    else:

        # scrolling background
        for i in range(0, tiles):
            screen.blit(background, (i * bg_width + scroll, 0))
        if not game_over:
            scroll -= 5
        if abs(scroll) > bg_width:
            scroll = 0
        # end of scrolling background

        # keyboard tracking
        for event in pygame.event.get():
            if pygame.event == pygame.QUIT:
                running = False
            if event.type == VIDEORESIZE:
                fullscreen = True
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                width = event.w
                height = event.h
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jumping = True
                    if playerY - jumpVelocity >= 120:
                        jumpVelocity = 50
                if event.key == pygame.K_d:
                    for i in range(magazineSize):
                        if bulletIsShot[i] is False:
                            bulletIsShot[i] = True
                            laserSound.play()
                            bulletY[i] = playerY + 25
                            break
                if event.key == pygame.K_DOWN and not jumping:
                    sliding = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    sliding = False
                    playerY = ground
        # end of keyboard tracking

        # objects movement
        for i in range(num_of_enemies):
            enemyX[i] -= ufoVelocity

        shieldX -= 5

        # jumping mechanics
        if jumping:
            if sliding:
                playerY = ground
                sliding = False
            playerY -= jumpVelocity
            if playerY < 120:
                gravity = 10
            else:
                gravity = 5
            jumpVelocity -= gravity
            if jumpVelocity < -jumpHeight and playerY >= ground:
                playerY = ground
                jumping = False
                jumpVelocity = jumpHeight
        # end of jumping mechanics

        # sliding mechanics
        if sliding:
            if not jumping:
                playerY = playerY_slide
        # end of objects movement

        # collision checking
        for i in range(num_of_enemies):
            if ufoHit(i):
                if not shieldActivated:
                    game_over = True
                    jumpVelocity = 0
                    break
                else:
                    shieldActivated = False
                    explosionSound.play()
                    shieldX = random.randint(width, width * 6)
                    shieldY = random.randint(0, ground - 50)
                    enemyX[i] = width
                    enemyY[i] = random.randint(50, ground)

        for i in range(magazineSize):
            hit = []
            hit = bulletHit(i)
            if hit[0]:
                explosionSound.play()
                bulletIsShot[i] = False
                bulletVelocity[i] = 25
                scoreValue += 1
                enemyX[hit[1]] = width
                enemyY[hit[1]] = random.randint(50, ground)

        if shieldCollected():
            shieldActivated = True
        # end of collision check

        if not game_over:
            player()
            enemy()
            displayScore()
            displayShieldState()
            if not shieldActivated:
                shield()
            for i in range(magazineSize):
                if bulletIsShot[i]:
                    bullet(i)
                    bulletVelocity[i] += 35
                    if bulletX[i] + bulletVelocity[i] > width:
                        bulletIsShot[i] = False
                        bulletVelocity[i] = 25
            for i in range(num_of_enemies):
                if enemyX[i] <= 0:
                    enemyX[i] = width
                    enemyY[i] = random.randint(50, ground)
            if shieldX <= 0 or shieldActivated:
                shieldX = width * 6

    pygame.display.update()
pygame.display.update()
pygame.quit()
