import pygame
"""
i want to make a platformer

the player should be able to move in all directions except for downwards because you shoudl not go downwards becaues it is a platformer 
you should be able to fight a something
and it drops coins
and with the coins you can puchase stuff

there should also be a plot

"""
pygame.init()
clock = pygame.time.Clock()
infoObj = pygame.display.Info()
SCREEN_WIDTH = infoObj.current_w
SCREEN_HEIGHT = infoObj.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, size,swidth, color,dir,level):
        super().__init__(Obstacles)
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size[0], self.size[1])
        self.color = color
        self.lvl = level
        self.swidth = swidth
        self.dir = dir
    def draw(self): 
        self.rect.center = self.pos
        origin = (self.pos.x - self.size[0] // 2,self.pos.y + self.size[1] // 2)
        swidth = self.swidth
        numSpikes = self.size[0] // swidth
        points = []
        for i in range(0,numSpikes):
            if self.dir == 0:
                points.append((origin[0] + i * swidth,origin[1]  - self.size[1]))
                points.append((origin[0] + swidth // 2 + i * swidth,origin[1]))
                points.append((origin[0] + swidth + i * swidth,origin[1]  - self.size[1]))
            elif self.dir == 1:
                points.append((origin[0] + i * swidth,origin[1]))
                points.append((origin[0] + swidth // 2 + i * swidth,origin[1] - self.size[1]))
                points.append((origin[0] + swidth + i * swidth,origin[1]))

        pygame.draw.polygon(screen, self.color, points)
    def update(self):
        #self.pos.y  += 0.5
        if self.lvl == player.lvl:
            self.draw()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.pos = V(50, SCREEN_HEIGHT-75)
        self.respawnPos = self.pos.copy()
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 25, 25)
        self.vel = V(0,0)
        self.speed = 400
        self.jump = 810
        self.onGround = False
        self.jgrace = 0.0
        self.gracetime = 0.08
        self.lvl = 1
    def draw(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 25, 25)
        self.rect.center = self.pos
        pygame.draw.rect(screen, (255,255,255), self.rect)
    def update(self,dt):
        self.draw()
        self.move(dt)
    def move(self,dt):
        self.xMovement(dt)
        self.collideX()
        self.yMovement(dt)
        self.collideY(dt)
        for tp in Teleporters:
            if self.rect.colliderect(tp.rect):
                self.lvl += 1
                self.respawn()
                level(self.lvl)
                print("next level %s" % self.lvl)
                for ground in Grounds:
                    if ground.lvl == self.lvl - 1:
                        ground.kill()
                for obstacle in Obstacles:
                    if obstacle.lvl == self.lvl - 1:
                        obstacle.kill()
        if self.pos.x < 0 or self.pos.x > SCREEN_WIDTH or self.pos.y > SCREEN_HEIGHT:
            self.respawn()
        for obstacle in Obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.respawn()
    def xMovement(self,dt):
        if K[L]:
            self.vel.x = -self.speed
        elif K[R]:
            self.vel.x = self.speed
        else:
            if self.vel.x > 0:
                self.vel.x /= 2
            elif self.vel.x < 0:
                self.vel.x /= 2
        self.pos.x += self.vel.x * dt
        self.rect.centerx = self.pos.x
    def collideX(self):
        for ground in Grounds:
            if self.rect.colliderect(ground.rect):
                if self.vel.x > 0:
                    self.rect.right = ground.rect.left
                elif self.vel.x < 0:
                    self.rect.left = ground.rect.right
                self.vel.x = 0
                self.pos.x = self.rect.centerx
    def collideY(self,dt):
        self.onGround = False
        self.jgrace -= dt
        for ground in Grounds:
            if self.rect.colliderect(ground.rect):
                if self.vel.y > 0:
                    self.rect.bottom = ground.rect.top
                    self.onGround = True
                    self.jgrace = self.gracetime
                elif self.vel.y < 0:
                    self.rect.top = ground.rect.bottom
                self.vel.y = 0
                self.pos.y = self.rect.centery
    def yMovement(self, dt):   
        if K[U] and (self.onGround or self.jgrace > 0):
            self.onGround = False
            self.vel.y = -self.jump
        self.vel.y += 30
        self.pos.y += self.vel.y * dt
        self.rect.centery = self.pos.y
    def respawn (self):
        self.pos = self.respawnPos.copy()
        self.vel = V(0,0)

class Ground(pygame.sprite.Sprite):
    def __init__(self, pos, size, color, lvl):
        super().__init__(Grounds)
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size[0], self.size[1])
        self.color = color
        self.lvl = lvl
    def draw(self): 
        self.rect.center = self.pos
        pygame.draw.rect(screen, self.color, self.rect)
    def update(self):
        if self.lvl == player.lvl:
            self.draw()
class Teleporter(pygame.sprite.Sprite):
    def __init__(self, pos, size, color,level):
        super().__init__(Teleporters)
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size[0], self.size[1])
        self.color = color
        self.level = level
    def draw(self): 
        self.rect.center = self.pos
        pygame.draw.rect(screen, self.color, self.rect)
    def update(self):
        if self.level == player.lvl:
            self.draw()
        
U = pygame.K_w
L = pygame.K_a
R = pygame.K_d
Q = pygame.K_ESCAPE
V = pygame.Vector2
player = Player()

Grounds = pygame.sprite.Group()
Teleporters = pygame.sprite.Group()
Obstacles = pygame.sprite.Group()

def level(lvl):
    if lvl == 1:
        Ground(V(100, SCREEN_HEIGHT), (200, 100), (60, 175, 50), lvl)
        Ground(V(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 200), (200, 100), (60, 175, 50), lvl)
        Ground(V(100, SCREEN_HEIGHT - 350), (200, 100), (60, 175, 50), lvl)
        Ground(V(SCREEN_WIDTH // 2 -300, SCREEN_HEIGHT - 500), (200, 100), (60, 175, 50), lvl)
        Ground(V(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 900), (1800, 400), (60, 175, 50), lvl)
        Ground(V(SCREEN_WIDTH // 2 + 140, SCREEN_HEIGHT+200), (200, 1500), (60, 175, 50), lvl)
        Teleporter(V(SCREEN_WIDTH // 2 + 600, SCREEN_HEIGHT - 300), (200, 100), (80, 50, 35), lvl)
        Obstacle(V(SCREEN_WIDTH // 2 -300, SCREEN_HEIGHT -525.54), (25, 50), 25, (60, 175, 50), 1,lvl)
    elif lvl == 2:
        Ground(V(100, SCREEN_HEIGHT), (200, 100), (60, 175, 50), lvl) #1
        Ground(V(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 100), (300, 100), (60, 175, 50), lvl)#2
        Obstacle(V(SCREEN_WIDTH // 2 -200, SCREEN_HEIGHT -175), (100, 50), 50, (255, 255, 255), 1,lvl)
        Ground(V(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT - 200), (200, 100), (60, 175, 50), lvl)#3
        Ground(V(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 400), (450, 100), (60, 175, 50), lvl)#4
        Obstacle(V(SCREEN_WIDTH // 2 -100, SCREEN_HEIGHT -475), (100, 50), 50, (255, 255, 255), 1,lvl)
        Obstacle(V(SCREEN_WIDTH // 2 -300, SCREEN_HEIGHT -475), (100, 50), 50, (255, 255, 255), 1,lvl)
        Ground(V(SCREEN_WIDTH // 2 - 720, SCREEN_HEIGHT - 530), (120, 100), (60, 175, 50), lvl)#5
        Ground(V(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT - 650), (700, 100), (60, 175, 50), lvl)#6
        Obstacle(V(SCREEN_WIDTH // 2 -200, SCREEN_HEIGHT -725), (50, 50), 50, (255, 255, 255), 1,lvl)
        Obstacle(V(SCREEN_WIDTH // 2 -100, SCREEN_HEIGHT -840), (50, 50), 50, (255, 255, 255), 0,lvl)
        Obstacle(V(SCREEN_WIDTH // 2 -300, SCREEN_HEIGHT -840), (50, 50), 50, (255, 255, 255), 0,lvl)
        Ground(V(SCREEN_WIDTH // 2 - 500, -50), (1500, 100), (60, 175, 50), lvl)
        Teleporter(V(SCREEN_WIDTH // 2 + 750, SCREEN_HEIGHT - 550), (200, 100), (0, 0, 150),lvl)
    elif lvl == 3:
        Ground(V(100, SCREEN_HEIGHT), (200, 100), (60, 175, 50), lvl) #1
        Ground(V(410, SCREEN_HEIGHT - 100), (100, 330), (60, 175, 50), lvl) #1
        Ground(V(680, SCREEN_HEIGHT-100), (100, 500), (60, 175, 50), lvl) #1
        Ground(V(900, SCREEN_HEIGHT-100), (70, 600), (60, 175, 50), lvl) #1
        Obstacle(V(875, SCREEN_HEIGHT - 395.6), (10, 10), 10, (60, 175, 50), 1,lvl)
    else:
        pass

game_running = True

level(player.lvl)
player.respawn()


while game_running:
    deltatime = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
    K = pygame.key.get_pressed()
    screen.fill((50, 80, 200))
    Grounds.update()
    Teleporters.update()
    Obstacles.update()
    player.update(deltatime)
    if K[Q]:
        game_running = False
    pygame.display.update()

