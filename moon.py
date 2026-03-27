import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Moving Moon Animation")

# Colors
WHITE = (255,255,255)
MOON = (245,245,200)
CRATER = (220,220,180)

SKY_TOP = (20,20,70)
SKY_BOTTOM = (0,0,0)


BACK_MOUNTAIN = (0,15,0)
FRONT_MOUNTAIN = (0,30,0)

TREE = (20,80,20)
TRUNK = (90,50,20)
SHADOW = (10,10,10)

FIREFLY = (255,255,120)

# Moon properties
moon_radius = 40
moon_x = -moon_radius
moon_y = HEIGHT//4
speed = 1.2

# Stars
stars = [[random.randint(0,WIDTH),
          random.randint(0,HEIGHT//2),
          random.randint(1,2)] for _ in range(60)]

# Fireflies
fireflies = [[random.randint(0,WIDTH),
              random.randint(380,450)] for _ in range(10)]

# Shooting stars
shooting_stars = []

clock = pygame.time.Clock()

# Gradient sky
def draw_sky():
    for y in range(HEIGHT):
        ratio = y/HEIGHT
        r = int(SKY_TOP[0]*(1-ratio) + SKY_BOTTOM[0]*ratio)
        g = int(SKY_TOP[1]*(1-ratio) + SKY_BOTTOM[1]*ratio)
        b = int(SKY_TOP[2]*(1-ratio) + SKY_BOTTOM[2]*ratio)
        pygame.draw.line(screen,(r,g,b),(0,y),(WIDTH,y))

# Mountains
def draw_mountains():

    # back layer
    pygame.draw.polygon(screen, BACK_MOUNTAIN, [(0,450),(140,320),(280,450)])
    pygame.draw.polygon(screen, BACK_MOUNTAIN, [(250,450),(420,300),(590,450)])
    pygame.draw.polygon(screen, BACK_MOUNTAIN, [(520,450),(680,320),(820,450)])

    # front layer
    pygame.draw.polygon(screen, FRONT_MOUNTAIN, [(150,450),(300,330),(450,450)])
    pygame.draw.polygon(screen, FRONT_MOUNTAIN, [(420,450),(600,340),(780,450)])

# Trees
def draw_trees():
    for x in range(50, WIDTH, 150):

        pygame.draw.rect(screen, TRUNK,(x+10,HEIGHT-80,10,30))

        pygame.draw.polygon(screen, TREE,
        [(x,HEIGHT-80),(x+15,HEIGHT-110),(x+30,HEIGHT-80)])

        pygame.draw.polygon(screen, SHADOW,
        [(x+10,HEIGHT-50),(x+40,HEIGHT-50),(x+25,HEIGHT-70)])

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_sky()

    # Twinkling stars
    for star in stars:
        pygame.draw.circle(screen, WHITE,(star[0],star[1]),star[2])
        star[2] = random.randint(1,2)

    # Generate  shooting stars
    if random.randint(0,120) == 1:
        shooting_stars.append([
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT//3)
        ])

    # Draw shooting stars
    for star in shooting_stars[:]:

        pygame.draw.line(screen, WHITE,
                         (star[0],star[1]),
                         (star[0]+25,star[1]+6),2)

        star[0] += 8
        star[1] += 3

        if star[0] > WIDTH or star[1] > HEIGHT:
            shooting_stars.remove(star)

    # Moon glow
    for r in range(moon_radius+15, moon_radius, -1):
        pygame.draw.circle(screen,(210,210,180),
        (int(moon_x),moon_y),r,1)

    # Moon
    pygame.draw.circle(screen, MOON,(int(moon_x),moon_y),moon_radius)

    # Moon craters
    pygame.draw.circle(screen, CRATER,(int(moon_x-10),moon_y-5),6)
    pygame.draw.circle(screen, CRATER,(int(moon_x+8),moon_y+6),5)
    pygame.draw.circle(screen, CRATER,(int(moon_x-5),moon_y+12),4)
    pygame.draw.circle(screen, CRATER,(int(moon_x+5),moon_y-10),4)

    draw_mountains()
    draw_trees()

    # Fireflies
    for f in fireflies:
        pygame.draw.circle(screen, FIREFLY,(f[0],f[1]),2)
        f[0] += random.choice([-1,1])
        f[1] += random.choice([-1,1])

    # Moon movement
    moon_x += speed
    moon_y = HEIGHT//4 

    if moon_x - moon_radius > WIDTH:
        moon_x = -moon_radius

    pygame.display.update()

pygame.quit()
sys.exit()