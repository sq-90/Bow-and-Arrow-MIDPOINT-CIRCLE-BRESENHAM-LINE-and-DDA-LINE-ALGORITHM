import pygame
import math
import random

# Initialize pygame
pygame.init()

# Setup display
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Archery - 2D Graphics Algorithms")

# Fonts
font = pygame.font.SysFont("sans-serif", 24, bold=True)
small_font = pygame.font.SysFont("sans-serif", 16)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
GRAY = (200, 200, 200)
BROWN = (210, 105, 30)
LIME = (0, 255, 0)

# Game State
bowCenterX = 80
bowCenterY = 200
arrowX = bowCenterX + 20
arrowY = bowCenterY
arrowSpeed = 0
isShooting = False
gameOver = False
targetX = 700
targetY = 200
targetRadius = 40
message = ""
message_color = WHITE
score = 0

def reset_game():
    global bowCenterY, arrowX, arrowY, targetY, arrowSpeed, isShooting, gameOver, message
    bowCenterY = 200
    arrowX = bowCenterX + 20
    arrowY = bowCenterY
    # Start target at random height just like JS version
    targetY = 100 + random.random() * 200
    arrowSpeed = 0
    isShooting = False
    gameOver = False
    message = ""

def put_pixel(surface, x, y, color):
    # Pygame's set_at method expects integer coordinates
    x, y = int(round(x)), int(round(y))
    if 0 <= x < width and 0 <= y < height:
        surface.set_at((x, y), color)

# --- 1. DDA LINE ALGORITHM ---
def draw_dda_line(surface, x1, y1, x2, y2, color):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        put_pixel(surface, x1, y1, color)
        return
    xInc = dx / steps
    yInc = dy / steps
    x, y = x1, y1
    for _ in range(int(steps) + 1):
        put_pixel(surface, x, y, color)
        x += xInc
        y += yInc

# --- 2. BRESENHAM LINE ALGORITHM ---
def draw_bresenham_line(surface, x1, y1, x2, y2, color):
    x1, y1 = int(round(x1)), int(round(y1))
    x2, y2 = int(round(x2)), int(round(y2))
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        put_pixel(surface, x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

# --- 3. MIDPOINT CIRCLE ALGORITHM ---
def draw_midpoint_circle(surface, xc, yc, r, color, right_half_only=False):
    xc, yc, r = int(round(xc)), int(round(yc)), int(round(r))
    x, y = 0, r
    p = 1 - r

    def plot(px, py):
        if right_half_only and px < xc:
            return
        put_pixel(surface, px, py, color)

    while x <= y:
        plot(xc + x, yc + y)
        plot(xc - x, yc + y)
        plot(xc + x, yc - y)
        plot(xc - x, yc - y)
        plot(xc + y, yc + x)
        plot(xc - y, yc + x)
        plot(xc + y, yc - x)
        plot(xc - y, yc - x)
        
        if p <= 0:
            p += 2 * x + 3
        else:
            p += 2 * (x - y) + 5
            y -= 1
        x += 1

def draw_thick_midpoint_circle(surface, xc, yc, r, thick, color, right_half_only=False):
    for i in range(thick):
        draw_midpoint_circle(surface, xc, yc, r - i, color, right_half_only)

# Main loop initialization
clock = pygame.time.Clock()
reset_game()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not isShooting and not gameOver:
                isShooting = True
                arrowSpeed = 20
            elif event.key == pygame.K_UP and not isShooting and bowCenterY > 50:
                bowCenterY -= 10
                arrowY = bowCenterY
            elif event.key == pygame.K_DOWN and not isShooting and bowCenterY < height - 50:
                bowCenterY += 10
                arrowY = bowCenterY
            elif event.key == pygame.K_r:
                reset_game()

    # Update logic
    if isShooting and not gameOver:
        arrowX += arrowSpeed
        
        distY = arrowY - targetY
        
        # Arrow intersects the target vertically and has reached the center X
        if abs(distY) <= targetRadius and arrowX >= targetX:
            points = 0
            hit_dist = abs(distY)
            if hit_dist <= 10:
                points = 100
            elif hit_dist <= 20:
                points = 50
            elif hit_dist <= 30:
                points = 25
            else:
                points = 10
            
            score += points
            message = f"HIT! +{points} pts. Press R to restart."
            message_color = LIME
            gameOver = True
            arrowSpeed = 0
            arrowX = targetX  # Snap the arrow tip visually inside the target
        elif arrowX > targetX + targetRadius + 20:
            message = "MISS! Press R to restart."
            message_color = RED
            gameOver = True
            arrowSpeed = 0

    # Draw everything
    screen.fill((34, 34, 34)) # background #222

    # Draw canvas box equivalent
    canvas_rect = pygame.Rect(0, 50, width, height - 50)
    pygame.draw.rect(screen, BLACK, canvas_rect)

    # Draw Target
    draw_thick_midpoint_circle(screen, targetX, targetY, targetRadius, 3, RED)
    draw_thick_midpoint_circle(screen, targetX, targetY, targetRadius - 10, 3, WHITE)
    draw_thick_midpoint_circle(screen, targetX, targetY, targetRadius - 20, 3, RED)
    draw_thick_midpoint_circle(screen, targetX, targetY, targetRadius - 30, 3, WHITE)
    for r in range(1, 11):
        draw_midpoint_circle(screen, targetX, targetY, r, RED)

    # Draw Bow
    draw_thick_midpoint_circle(screen, bowCenterX, bowCenterY, 50, 2, BROWN, right_half_only=True)
    
    # Draw Bow String
    stringPull = 0 if isShooting else -20
    draw_bresenham_line(screen, bowCenterX, bowCenterY - 50, bowCenterX + stringPull, bowCenterY, GRAY)
    draw_bresenham_line(screen, bowCenterX + stringPull, bowCenterY, bowCenterX, bowCenterY + 50, GRAY)

    # Draw Arrow
    tailX = arrowX - 50
    if not isShooting:
        tailX = bowCenterX + stringPull
        
    draw_dda_line(screen, tailX, arrowY, arrowX, arrowY, GOLD) # shaft
    draw_dda_line(screen, tailX, arrowY, tailX - 5, arrowY - 3, WHITE) # fletching
    draw_dda_line(screen, tailX, arrowY, tailX - 5, arrowY + 3, WHITE)
    draw_dda_line(screen, arrowX, arrowY, arrowX - 5, arrowY - 4, GRAY) # head
    draw_dda_line(screen, arrowX, arrowY, arrowX - 5, arrowY + 4, GRAY)
    draw_dda_line(screen, arrowX - 5, arrowY - 4, arrowX - 5, arrowY + 4, GRAY)

    # UI text rendering
    controls_text = small_font.render("Press SPACE to shoot! Use UP/DOWN arrows to aim. Press R to reset.", True, (170, 170, 170))
    screen.blit(controls_text, (width//2 - controls_text.get_width()//2, 10))

    score_text = font.render(f"Score: {score}", True, GOLD)
    screen.blit(score_text, (20, 10))

    if message:
        msg_text = font.render(message, True, message_color)
        screen.blit(msg_text, (width//2 - msg_text.get_width()//2, 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
