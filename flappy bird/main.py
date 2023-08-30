
import pygame as py, sys
from random import randint
from pygame import mixer
from time import sleep

#initialize pygame and mixer
py.init()
mixer.init()

#dimensions
dimen = width, height = 700, 700

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#variables
GRAVITY = .5
FPS = 60
pipe_gap = 100
score = 0

#font
font = py.font.Font("assets/fonts/vampire-wars.ttf", 32)

#clock
clock = py.time.Clock()

#screen
screen = py.display.set_mode(dimen)
py.display.set_caption("Flappy bird")

#images
bg = py.image.load("assets/images/background.png").convert_alpha()
flappyimg = py.image.load("assets/images/flappyBird.png").convert_alpha()

#to setup the text
def set_text(string, x, y):
    text = font.render(string, True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    return (text, text_rect)

#sounds
die = mixer.Sound("assets/sound/die.mp3")
flap = mixer.Sound("assets/sound/flap.mp3")
hit = mixer.Sound("assets/sound/hit.mp3")
point = mixer.Sound("assets/sound/point.mp3")

#player class
class Player:
    def __init__(self, x, y):
        self.image = flappyimg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velY = 0

    def draw(self):
        #delta vars
        dy = 0

        screen.blit(self.image, self.rect)

        self.velY += GRAVITY
        dy += self.velY
        self.rect.y += dy

        #checking if above the screen
        if self.rect.y < 0:
            self.rect.y = 0

#pipe class
class Pipe(py.sprite.Sprite):
    def __init__(self, x, y, pos):
        super().__init__()
        self.image = py.image.load("assets/images/pipe.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        if pos == 1:
            self.image = py.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_gap]
        elif pos == 2:
            self.rect.topleft = [x, y + pipe_gap]

#player instance
player = Player(width // 2 - 100, height // 2)

#pipe group and instance
botmpipe = Pipe(500, 500, 1)
topPipe = Pipe(500, 500, 2)
pipe_group = py.sprite.Group()
pipe_group.add(botmpipe, topPipe)

#playing background music
mixer.music.load("assets/sound/backgroundsong.mp3")
mixer.music.play(-1)

#game loop
while True:
    #blitting the background
    screen.blit(bg, (0, 0))

    #showing score
    scoretext = set_text(f"Score: {score}", width // 2, height // 2)
    screen.blit(scoretext[0], scoretext[1])

    #drawing pipe
    pipe_group.draw(screen)

    #drawing the bird
    player.draw()

    

    #event loop
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        elif event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                py.quit()
                sys.exit()
            elif event.key == py.K_SPACE:
                mixer.Sound.play(flap)
                player.velY -= 15

    #increasing the y velocity of player whenever it hits the ceiling
    if player.rect.y == 0:
        player.velY += 10
    
    #checking if player under the screen
    if player.rect.y > 800:
        mixer.Sound.play(die)
        sleep(1)
        py.quit(); sys.exit()

    botmpipe.rect.x -= 5
    topPipe.rect.x -= 5

    toppipecoll = player.rect.colliderect(topPipe.rect)
    botmpipecoll = player.rect.colliderect(botmpipe.rect)

    if topPipe.rect.right < 0:
        mixer.Sound.play(point)
        score += 1
        newpipeplace = randint(240, 500)
        topPipe.rect.x = 780
        botmpipe.rect.x = 780
        topPipe.rect.y = newpipeplace
        botmpipe.rect.y = newpipeplace - 800

    if toppipecoll or botmpipecoll:
        mixer.Sound.play(hit)
        sleep(1)
        py.quit(); sys.exit()

    clock.tick(FPS)
    py.display.update()
