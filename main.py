import pygame, os
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

def getImages(path):
    images = []
    for file in os.listdir(path):
        image = pygame.image.load(path + "/" + file)
        images.append(image)
    return images

cannonImgs = getImages("cannon")
fireballImgs = getImages("ball") 
cometImgs = getImages("comet")
playerImg = pygame.image.load("dog (1).png")
playerImg = pygame.transform.scale_by(playerImg, 0.12)
woodImg = pygame.image.load("wood.png")
# playerImg = pygame.transform.flip(playerImg, True, False)

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
        self.image = playerImg
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))
        self.vel = V(0,0)
        self.speed = 405
        self.jump = 820
        self.onGround = False
        self.jgrace = 0.0
        self.gracetime = 0.08
        self.lvl = 5
        self.isRight = True
    def draw(self):
        if self.isRight:
            self.image = pygame.transform.flip(playerImg, True, False)
        else:
            self.image = playerImg
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))
        # pygame.draw.rect(screen, (255,255,255), self.rect)
        screen.blit(self.image, self.rect)
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
                for tramp in Trampolines:
                    if tramp.lvl == self.lvl - 1:
                        tramp.kill()
                for tele in Teleporters:
                    if tele.lvl == self.lvl - 1:
                        tele.kill()
        if self.pos.x < 0 or self.pos.x > SCREEN_WIDTH or self.pos.y > SCREEN_HEIGHT:
            self.respawn()
        for obstacle in Obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.respawn()
        if pygame.sprite.spritecollide(self, Fireballs, True, pygame.sprite.collide_mask):
            self.respawn()
    def xMovement(self,dt):
        if K[L]:
            self.vel.x = -self.speed
            self.isRight = False
        elif K[R]:
            self.vel.x = self.speed
            self.isRight = True
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
        for ground in Trampolines:
            if self.rect.colliderect(ground.rect):
                if self.vel.y > 0:
                    self.rect.bottom = ground.rect.top
                    self.onGround = False
                    self.jgrace = 0
                elif self.vel.y < 0:
                    self.rect.top = ground.rect.bottom
                self.vel.y = -self.jump * ground.bounce
                self.pos.y = self.rect.centery
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
    def __init__(self, pos, size, color, lvl, img=None, move=False):
        super().__init__(Grounds)
        self.pos = pos
        self.size = size
        self.move = move
        if img:
            self.img = pygame.transform.scale(img, self.size)
            self.rect = self.img.get_rect(center = self.pos)
            self.hasImg = True
        else:
            self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size[0], self.size[1])
            self.hasImg = False
        self.color = color
        self.lvl = lvl
    def draw(self):
        if self.hasImg:
            self.rect = self.img.get_rect(center = self.pos)
            screen.blit(self.img, self.rect)
        else:
            self.rect.center = self.pos
            pygame.draw.rect(screen, self.color, self.rect)
    def update(self):
        if self.lvl == player.lvl:
            if self.move:
                self.pos.x += self.move
                if self.pos.x > SCREEN_WIDTH:
                    self.pos.x = -self.size[0]
                elif self.pos.x < -self.size[0]:
                    self.pos.x = SCREEN_WIDTH
            self.draw()

class Cannon(pygame.sprite.Sprite):
    def __init__(self, pos, size, rate, lvl, isFlipped = False):
        super().__init__(Cannons)
        self.pos = pos
        self.size = size
        self.rate = rate
        self.frame = 0
        self.lastTick = 0
        self.flip = isFlipped
        self.images = cannonImgs.copy()
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale_by(self.images[i], self.size)
            self.images[i] = pygame.transform.flip(self.images[i], self.flip, False)
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center = self.pos)
        self.lvl = lvl
    def draw(self):
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center = self.pos)
        screen.blit(self.image, self.rect)
    def update(self):
        if pygame.time.get_ticks() - self.lastTick > self.rate:
            self.lastTick = pygame.time.get_ticks()
            self.frame += 1 
            if self.frame == len(self.images):
                self.frame = 0
                Fireball(V(self.pos.x - 50 if not self.flip else self.pos.x + 50, self.pos.y - 10), 0.36, 100, self.lvl, isFlipped=self.flip)
        if self.lvl == player.lvl:
            self.draw()
class Fireball(pygame.sprite.Sprite):
    def __init__(self, pos, size, rate, lvl, isFlipped = False):
        super().__init__(Fireballs)
        self.pos = pos
        self.size = size
        self.rate = rate
        self.frame = 0
        self.lastTick = 0
        self.flip = isFlipped
        self.images = fireballImgs.copy()
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale_by(self.images[i], self.size)
            self.images[i] = pygame.transform.flip(self.images[i], not self.flip, False)
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center = self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.lvl = lvl
    def draw(self):
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center = self.pos)
        # pygame.draw.rect(screen, "black", self.rect)
        screen.blit(self.image, self.rect)
    def update(self):
        self.pos.x -= 5 if not self.flip else -5
        if pygame.time.get_ticks() - self.lastTick > self.rate:
            self.lastTick = pygame.time.get_ticks()
            self.frame += 1 
            if self.frame == len(self.images): self.frame = 0
        if self.lvl == player.lvl:
            self.draw()

class Comet(pygame.sprite.Sprite):
    def __init__(self, pos, size, rate, lvl):
        super().__init__(Comets)
        self.pos = pos
        self.size = size
        self.rate = rate
        self.frame = 0
        self.lastTick = 0
        self.images = cometImgs.copy()
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale_by(self.images[i], self.size)
            self.images[i] = pygame.transform.rotate(self.images[i], -90)
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center = self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.lvl = lvl
    def draw(self):
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center = self.pos)
        # pygame.draw.rect(screen, "black", self.rect)
        screen.blit(self.image, self.rect)
    def update(self):
        # self.pos.y += 5 
        if pygame.time.get_ticks() - self.lastTick > self.rate:
            self.lastTick = pygame.time.get_ticks()
            self.frame += 1 
            if self.frame == len(self.images): self.frame = 0
        if self.lvl == player.lvl:
            self.draw()


class Trampoline(pygame.sprite.Sprite):
    def __init__(self, pos, size, color, bounce, lvl):
        super().__init__(Trampolines)
        self.pos = pos
        self.size = size
        self.bounce = bounce
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size[0], self.size[1])
        self.color = color
        self.lvl = lvl
    def draw(self): 
        self.rect.center = self.pos
        pygame.draw.ellipse(screen, self.color, self.rect)
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
        self.lvl = level
    def draw(self): 
        self.rect.center = self.pos
        pygame.draw.rect(screen, self.color, self.rect)
    def update(self):
        if self.lvl == player.lvl:
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
Trampolines = pygame.sprite.Group()
Cannons = pygame.sprite.Group()
Fireballs = pygame.sprite.Group()
Comets = pygame.sprite.Group()
brown = (100, 65, 25)
green = (60, 175, 50)

def level(lvl):
    if lvl == 1:
        Ground(V(100, SCREEN_HEIGHT), (200, 100), (60, 175, 50), lvl)
        Ground(V(100, SCREEN_HEIGHT + 20), (200, 85), brown, lvl)
        Ground(V(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 200), (200, 100), (60, 175, 50), lvl)
        Ground(V(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 180), (200, 85), brown, lvl)
        Ground(V(100, SCREEN_HEIGHT - 350), (200, 100), (60, 175, 50), lvl)
        Ground(V(100, SCREEN_HEIGHT - 330), (200, 85), brown, lvl)
        Ground(V(SCREEN_WIDTH // 2 -300, SCREEN_HEIGHT - 500), (200, 100), (60, 175, 50), lvl)
        Ground(V(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 480), (200, 85), brown, lvl)
        Ground(V(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 900), (1800, 400), (99, 94, 90), lvl)
        Ground(V(SCREEN_WIDTH // 2 + 140, SCREEN_HEIGHT+200), (200, 1500), (60, 175, 50), lvl)
        Ground(V(SCREEN_WIDTH // 2 +140, SCREEN_HEIGHT +220), (200, 1485), brown, lvl)
        Teleporter(V(SCREEN_WIDTH // 2 + 600, SCREEN_HEIGHT - 300), (200, 100), (80, 50, 35), lvl)
        Obstacle(V(SCREEN_WIDTH // 2 -300, SCREEN_HEIGHT - 539), (25, 25), 25, (60, 175, 50), 1,lvl)
    elif lvl == 2:
        Ground(V(100, SCREEN_HEIGHT), (200, 100), (60, 175, 50), lvl) #1
        Ground(V(100, SCREEN_HEIGHT +20), (200, 85), brown, lvl)
        Ground(V(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 100), (300, 100), (60, 175, 50), lvl)#2
        Ground(V(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 80), (300, 85), brown, lvl)
        Obstacle(V(SCREEN_WIDTH // 2 -200, SCREEN_HEIGHT -168), (75, 37), 37, (255, 255, 255), 1,lvl)#fix the rest of the obstacles to aroudn these settings.
        Ground(V(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT - 200), (200, 100), (60, 175, 50), lvl)#3
        Ground(V(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT - 180), (200, 85), brown, lvl)
        Ground(V(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 400), (450, 100), (60, 175, 50), lvl)#4
        Ground(V(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 380), (450, 85), brown, lvl)
        Obstacle(V(SCREEN_WIDTH // 2 -100, SCREEN_HEIGHT -469), (75, 37), 37, (255, 255, 255), 1,lvl)
        Obstacle(V(SCREEN_WIDTH // 2 -300, SCREEN_HEIGHT -469), (75, 37), 37, (255, 255, 255), 1,lvl)
        Ground(V(SCREEN_WIDTH // 2 - 720, SCREEN_HEIGHT - 530), (120, 100), (60, 175, 50), lvl)#5
        Ground(V(SCREEN_WIDTH // 2 - 720, SCREEN_HEIGHT - 510), (120, 85), brown, lvl)
        Ground(V(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT - 665), (675, 85), (60, 175, 50), lvl)#6
        Ground(V(SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT - 645), (675, 70), brown, lvl)
        Obstacle(V(SCREEN_WIDTH // 2 -200, SCREEN_HEIGHT -726), (75, 37), 37, (255, 255, 255), 1,lvl)
        Obstacle(V(SCREEN_WIDTH // 2 -50, SCREEN_HEIGHT -850), (75, 37), 37, (255, 255, 255), 0,lvl)
        Obstacle(V(SCREEN_WIDTH // 2 -350, SCREEN_HEIGHT -850), (75, 37), 37, (255, 255, 255), 0,lvl)
        Ground(V(SCREEN_WIDTH // 2 - 500, -50), (1500, 100), (60, 175, 50), lvl)
        Teleporter(V(SCREEN_WIDTH // 2 + 750, SCREEN_HEIGHT - 550), (200, 100), (80, 50, 35),lvl)
    elif lvl == 3:
        Obstacle(V(SCREEN_WIDTH//2 + 8, 20), (1700,50), 50, (255, 255, 255), 0,lvl)
        Ground(V(100, SCREEN_HEIGHT ), (200, 90), (60, 175, 50), lvl) #1
        Ground(V(100, SCREEN_HEIGHT + 20), (200, 75), (100, 65, 25), lvl) #1
        Ground(V(410, SCREEN_HEIGHT - 100), (100, 330), (60, 175, 50), lvl) #1
        Ground(V(410, SCREEN_HEIGHT - 80), (100, 315), (100, 65, 25), lvl) #1
        Trampoline(V(410, SCREEN_HEIGHT - 265), (50, 15), (175, 120, 190), 3, lvl)
        Ground(V(680, SCREEN_HEIGHT-60), (100, 500), (60, 175, 50), lvl) #1
        Ground(V(680, SCREEN_HEIGHT - 40), (100, 485), (100, 65, 25), lvl) #1
        Trampoline(V(680, SCREEN_HEIGHT - 310), (50, 15), (175, 120, 190), 3, lvl)
        Ground(V(900, SCREEN_HEIGHT-100), (70, 600), (60, 175, 50), lvl) #1
        Ground(V(900, SCREEN_HEIGHT - 80), (70, 585), (100, 65, 25), lvl) #1
        Ground(V(1285, SCREEN_HEIGHT+250), (50, 600), (99, 94, 90), lvl) 
        Ground(V(1285, SCREEN_HEIGHT+270), (50, 585), (82, 78, 75), lvl) 
        Ground(V(1335, SCREEN_HEIGHT+265), (50, 600), (128, 116, 108), lvl)
        Ground(V(1335, SCREEN_HEIGHT+285), (50, 585), (99, 91, 85), lvl)
        Obstacle(V(875, SCREEN_HEIGHT - 395.6), (10, 10), 10, (60, 175, 50), 1,lvl)
        Ground(V(1500, SCREEN_HEIGHT - 20), (50, 400),(60, 175, 50), lvl )
        Ground(V(1500, SCREEN_HEIGHT), (50, 385), (100, 65, 25), lvl)
        Trampoline(V(1500, SCREEN_HEIGHT - 215), (50, 15), (175, 120, 190), 1.7, lvl)
        Teleporter(V(SCREEN_WIDTH // 2 + 550, SCREEN_HEIGHT - 750), (200, 100), (80, 50, 35),lvl)
    elif lvl == 4:
        Ground(V(100, SCREEN_HEIGHT), (200, 90), green, lvl) #1
        Ground(V(100, SCREEN_HEIGHT + 20), (200, 75), brown, lvl) #1
        Ground(V(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 125), (200, 50), (100, 65, 25), lvl, img=woodImg) #1
        Cannon(V(SCREEN_WIDTH - 65, SCREEN_HEIGHT - 200), 0.3, 110,  lvl)
        Ground(V(600, SCREEN_HEIGHT - 75), (300, 90), green, lvl) #1
        Ground(V(900, SCREEN_HEIGHT - 90), (350, 120), (60, 175, 50), lvl) #1
        Ground(V(900, SCREEN_HEIGHT - 76), (350, 92), brown, lvl) #1
        Ground(V(450, SCREEN_HEIGHT - 110), (10, 160), (60, 175, 50), lvl) #1
        Obstacle(V(450, SCREEN_HEIGHT - 195), (10, 10), 10, (60, 175, 50), 1,lvl)
        Ground(V(590, SCREEN_HEIGHT - 63), (290, 65), brown, lvl) #1
        Trampoline(V(1050, SCREEN_HEIGHT - 150), (50, 15), (175, 120, 190), 1.7, lvl)
        Ground(V(700, SCREEN_HEIGHT - 650), (120, 90), (60, 175, 50), lvl) #1
        Ground(V(700, SCREEN_HEIGHT - 635), (120, 60), brown, lvl) #1
        Ground(V(1250, SCREEN_HEIGHT - 600), (250, 120), (60, 175, 50), lvl) #1
        Ground(V(1250, SCREEN_HEIGHT - 585), (250, 90), brown, lvl) #1
        Ground(V(75, SCREEN_HEIGHT - 675), (200, 50), (100, 65, 25), lvl, img=woodImg) #1
        Cannon(V(120, SCREEN_HEIGHT - 750), 0.3, 170,  lvl, isFlipped=True)
        Ground(V(200, SCREEN_HEIGHT - 525), (200, 50), (50, 80, 200), lvl) #1
        Teleporter(V(SCREEN_WIDTH // 2 - 700, SCREEN_HEIGHT - 600), (200, 100), (80, 50, 35),lvl)
    elif lvl == 5:
        """this level will have mmoving platforms and you have to get to the top to
        switch the lever while stuff comes from the sky and the boss will explode or 
        something when the lever is touched"""
        Ground(V(100, SCREEN_HEIGHT), (200, 90), green, lvl) #1
        Ground(V(100, SCREEN_HEIGHT + 20), (200, 75), brown, lvl) #1
        Ground(V(900, SCREEN_HEIGHT - 40), (1200, 150), green, lvl) #1
        Ground(V(900, SCREEN_HEIGHT - 20), (1200, 135), brown, lvl) #1
        Ground(V(900, SCREEN_HEIGHT - 250), (200, 50), green, lvl, move=-7) #1
        Ground(V(900, SCREEN_HEIGHT - 390), (200, 50), green, lvl, move=10) #1
        Ground(V(900, SCREEN_HEIGHT - 530), (200, 50), green, lvl, move=-13) #1
        Comet(V(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 0.2, 100, lvl)
        Ground(V(75, SCREEN_HEIGHT - 675), (200, 50), (100, 65, 25), lvl, img=woodImg) #1
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
    Trampolines.update()
    Fireballs.update() 
    Cannons.update()
    Comets.update()
    
    player.update(deltatime)
    if K[Q]:
        game_running = False
    pygame.display.update()

