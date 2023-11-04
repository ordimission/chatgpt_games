import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load spaceship image
spaceship_img = pygame.image.load("spaceship.png")
spaceship_img = pygame.transform.scale(spaceship_img, (20, 60))

# Load enemy image
enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (60, 60))

# Load projectile image
projectile_img = pygame.image.load("projectile.png")
projectile_img = pygame.transform.scale(projectile_img, (8, 8))

# Load enemy projectile image
enemy_projectile_img = pygame.image.load("enemy_projectile.png")
enemy_projectile_img = pygame.transform.scale(enemy_projectile_img, (8, 8))

# Spaceship class
class Spaceship:
    def __init__(self):
        self.x = WIDTH // 2
        self.xdir = 0

    def show(self):
        screen.blit(spaceship_img, (self.x, HEIGHT - 20))

    def move(self):
        self.x += self.xdir * 5

    def set_dir(self, dir):
        self.xdir = dir

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xdir = 1
        self.speed = 2
        self.amplitude = 50
        self.frequency = 0.02
        self.offset = random.uniform(0, 100)

    def show(self):
        screen.blit(enemy_img, (self.x, self.y))

    def move(self):
        self.x += self.xdir * self.speed
        self.y += math.sin((pygame.time.get_ticks() + self.offset) * self.frequency) * self.amplitude * self.frequency
        if self.x > WIDTH or self.x < 0:
            self.xdir *= -1
            self.y += 20

# Projectile class
class Projectile:
    def __init__(self, x, y, is_enemy=False):
        self.x = x
        self.y = y
        self.to_delete = False
        self.is_enemy = is_enemy

    def show(self):
        if self.is_enemy:
            screen.blit(enemy_projectile_img, (self.x, self.y))
        else:
            screen.blit(projectile_img, (self.x, self.y))

    def move(self):
        self.y += 5 if self.is_enemy else -5

    def hits(self, target):
        d = math.sqrt((self.x - target.x) ** 2 + (self.y - target.y) ** 2)
        return d < 30

    def destroy(self):
        self.to_delete = True

# Initialize game objects
spaceship = Spaceship()
enemies = [Enemy(i * 80 + 80, 60) for i in range(10)]
projectiles = []
enemy_projectiles = []

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectiles.append(Projectile(spaceship.x, HEIGHT - 20))
            elif event.key == pygame.K_RIGHT:
                spaceship.set_dir(1)
            elif event.key == pygame.K_LEFT:
                spaceship.set_dir(-1)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                spaceship.set_dir(0)

    spaceship.show()
    spaceship.move()

    for projectile in projectiles:
        projectile.show()
        projectile.move()
        for i in range(len(enemies) - 1, -1, -1):
            if projectile.hits(enemies[i]):
                del enemies[i]
                projectile.destroy()

    for enemy_projectile in enemy_projectiles:
        enemy_projectile.show()
        enemy_projectile.move()
        if enemy_projectile.hits(spaceship):
            print("Game Over")
            running = False

    for enemy in enemies:
        enemy.show()
        enemy.move()
        if random.random() < 0.001:
            enemy_projectiles.append(Projectile(enemy.x, enemy.y, True))

    projectiles = [p for p in projectiles if not p.to_delete]
    enemy_projectiles = [p for p in enemy_projectiles if not p.to_delete]

    pygame.display.flip()

pygame.quit()