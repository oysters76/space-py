import pygame 
from pygame.locals import *
import random

class Enemy:
    def __init__(self, x, y, width, height, color, speed, direction, ww):
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.color = color 
        self.speed = speed
        self.direction = direction
        self.world_width = ww
        self.isAlive = True 
    
    def move(self):
        c = self.speed 
        if self.direction:
            c *= -1 
        x1 = self.x + c 
        if x1 < 0 or (x1+self.width) > self.world_width: #prevents the enemy from going off screen
            self.direction = not self.direction 
            return 
        self.x = x1 
    
    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height);
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.getRect())
    
    def destroy(self):
        self.isAlive = False

def r():
    return random.randint(0,255)

def spawn_enemy(w, h, i):
    width = 20 
    height = 10
    x = random.randint(0, w-width) 
    offset = i*5 
    y = random.randint(100+offset, h/2) 
    color = pygame.Color(r(), r(), r()) 
    speed = random.randint(5,8)
    direction = random.choice([True, False]) 
    return Enemy(x, y, width, height, color, speed, direction, w)

def spawn_enemies(w, h, size=5):
    enemies = []
    for i in range(size):
        enemies.append(spawn_enemy(w,h,i))
    return enemies 


class Projectile:
    def __init__(self, x, y, width=5, height=5, color=pygame.Color(255,255,255), speed=5):
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.color = color 
        self.speed = speed
        self.isAlive = True 
    
    def update(self):
        if self.y < 0:
            self.isAlive = False 
            return  
        self.y -= self.speed 

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.getRect()) 

class Player:
    def __init__(self, world_width, width=40, height=20, 
                 x=400, y=700, player_color=pygame.Color(0,100,0), speed=2):
        self.x = x 
        self.y = y
        self.player_color = player_color
        self.width = width 
        self.height = height 
        self.speed = speed 
        self.world_width = world_width 
        self.projectiles = []
    
    # if the direction is false, player moves to the right, otherwise to the left
    def move(self, direction=False):    
        c = self.speed 
        if direction:
            c *= -1 
        x1 = self.x + c 
        if x1 < 0 or (x1+self.width) > self.world_width: #prevents the player from going off screen
            return  
        self.x += c  
    
    def fire(self):
        offset = self.width/2
        proj = Projectile(self.x+offset, self.y)
        self.projectiles.append(proj) 

    def drawPlayer(self, surface):
        pygame.draw.rect(surface, self.player_color, self.getRect())
    
    def drawProjectiles(self, surface):
        for index, proj in enumerate(self.projectiles):
            if not proj.isAlive:
                del self.projectiles[index] 
                continue;
            proj.update()
            proj.draw(surface)

    def checkCollisions(self, enemies):
        for proj in self.projectiles:
            if not proj.isAlive:
                continue 
            proj_rect = proj.getRect()
            for enemy in enemies:
                if not enemy.isAlive:
                    continue 
                enemy_rect = enemy.getRect()
                if not proj_rect.colliderect(enemy_rect):
                    continue 
                enemy.destroy()

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


width = 800 
height = 800
black = pygame.Color(0,0,0) 

pygame.init() 
screen = pygame.display.set_mode((width, height)) 
clock = pygame.time.Clock() 
running = True 

pygame.display.set_caption("Space Invaders")


pygame.key.set_repeat(1, 10)

player = Player(width) 
enemies = spawn_enemies(width, height, 10)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:    
            keys = pygame.key.get_pressed() 
            if (keys[K_LEFT] or keys[K_RIGHT]):
                player.move(keys[K_LEFT])
            if (keys[K_z]):
                player.fire()

    screen.fill(black) 

    # render the game here 
    
    #draw the enemies 
    for index, enemy in enumerate(enemies):
        if not enemy.isAlive: 
            del enemies[index] 
        enemy.move()
        enemy.draw(screen)

    player.drawPlayer(screen)
    player.drawProjectiles(screen); 
    player.checkCollisions(enemies)

    pygame.display.flip() 
    clock.tick(60) # limits the fps to 60 

pygame.quit() 
