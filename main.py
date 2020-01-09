import pygame
import random
import math
from pygame import mixer

# initialze the pygame
pygame.init()

# create the screen don't forget the extra ()
screen = pygame.display.set_mode((800, 600))
# title and caption
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space invaders logo.jpeg')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('background.jpg')

#background music
mixer.music.load('backgroundmusic.wav')
mixer.music.play(-1)

# player
player_image = pygame.image.load('spaceship.png')
playerX = 368
playerY = 480
playerX_Change = 0

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX =10
textY = 10
def showScore(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#gameover text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def gameOver():
    over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_image, (x, y))


# enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_enemies = 10

for i in range(num_enemies):
    enemy_image.append(pygame.image.load('poop.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 125))
    enemyX_Change.append(12)
    enemyY_Change.append(40)


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


# bullet, ready means can't see bullet on screen, fire then bullet is currently moving
bullet_image = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_Change = 28
bullet_state = "ready"


def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop that makes sure game is running until quit
running = True
while running:
    # RGB = red , green, blue
    screen.fill((0, 0, 0))
    # add background here on top of black screen but behind everything else
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_Change = -15
            if event.key == pygame.K_d:
                playerX_Change = 15
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_Change = 0
    playerX += playerX_Change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_enemies):
        #game over
        if enemyY[i]>= 440:
            over_sound = mixer.Sound('gameover.wav')
            over_sound.play(0)
            for j in range(num_enemies):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] *= -1
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 736:
            enemyX_Change[i] *= -1
            enemyY[i] += enemyY_Change[i]
        if enemyY[i] >= 480:
            enemyY[i] = 480

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            fart_sound = mixer.Sound('fart.wav')
            fart_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 125)
            enemyX_Change[i] += 3

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
