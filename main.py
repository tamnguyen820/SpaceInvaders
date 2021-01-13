import pygame
from pygame import mixer
import random
import math

# Initialize the pygame
pygame.init()

# Create the screen, background, and sound
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("247re.jpg")
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)

# Player
pIcon = pygame.image.load("ship_big.png")
pX = 370
pY = 480
deltaX = 0
inputList = [False, False]

# Enemies
eIcon = []
eX = []
eY = []
betaX = []
betaY = []
num_enemies = 6

for i in range(num_enemies):
    eIcon.append(pygame.image.load("ufo.png"))
    eX.append(random.randint(0, 735))
    eY.append(random.randint(50, 150))
    betaX.append(0.3)
    betaY.append(100)

# Bullet
bulletIcon = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_delta = 1.5
bulletShot = False

# Texts
score_value = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = score_font.render(
        "Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


def player(x, y):
    screen.blit(pIcon, (x, y))


def enemy(x, y, i):
    screen.blit(eIcon[i], (x, y))


def fire(x, y):
    global bulletShot
    bulletShot = True
    screen.blit(bulletIcon, (x+16, y+10))


def hit(eX, eY, bX, bY):
    d = math.sqrt((eX-bX)**2 + (eY-bY)**2)
    if d < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                inputList[0] = True
            if event.key == pygame.K_RIGHT:
                inputList[1] = True
            if event.key == pygame.K_SPACE:
                if not bulletShot:
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = pX
                    fire(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                inputList[0] = False
            if event.key == pygame.K_RIGHT:
                inputList[1] = False

    # Smooth key control
    if inputList[0]:
        deltaX = -0.7
    if inputList[1]:
        deltaX = 0.7
    if not inputList[0] and not inputList[1]:
        deltaX = 0

    # Add movements and check boundaries
    # Player movement
    pX += deltaX
    if pX < 0:
        pX = 0
    elif pX > 736:
        pX = 736

    # Enemies movement
    for i in range(num_enemies):

        # Game over
        if eY[i] > 420:
            for i in range(num_enemies):
                eY[i] = 2000
            game_over()
            break

        eX[i] += betaX[i]
        if eX[i] < 0:
            betaX[i] = 0.3
            eY[i] += betaY[i]
        elif eX[i] > 736:
            betaX[i] = -0.3
            eY[i] += betaY[i]

        # Collision
        collision = hit(eX[i], eY[i], bulletX, bulletY)
        if collision:
            collisionSound = mixer.Sound("explosion.wav")
            collisionSound.play()
            bulletY = 480
            bulletShot = False
            score_value += 1
            eX[i] = random.randint(0, 735)
            eY[i] = random.randint(50, 150)

        enemy(eX[i], eY[i], i)

    # Bullet movement
    if bulletY < -4:
        bulletY = 480
        bulletShot = False
    if bulletShot:
        fire(bulletX, bulletY)
        bulletY -= bulletY_delta

    player(pX, pY)
    show_score(textX, textY)
    pygame.display.update()
