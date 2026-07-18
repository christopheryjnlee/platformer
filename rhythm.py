import pygame 
import random 

#Initialize Pygame 
pygame.init()

#Screen dimensions 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600 

#Colors
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)

#Game settings 
ARROW_SPEED = 10
ARROW_INTERVAL = 500  # miliseconds 
ARROW_SIZE = 50 

#Arrows 
arrow = pygame.transform.scale(pygame.image.load("arrow.png"), (ARROW_SIZE, ARROW_SIZE))
up = arrow
left = pygame.transform.rotate(arrow, 90)
right = pygame.transform.rotate(arrow, 270)
down = pygame.transform.rotate(arrow, 180)
arrows = {"up": up, "down": down, "left" :left, "right": right}

#Setup screen 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame .display.set_caption("Rhythm Game")

#Clock
clock = pygame.time.Clock()

#Font
font = pygame.font.SysFont(None, 55)

class Arrow:
    def __init__(self, x, y, dir, key):
        self.x = x
        self.y = y
        self.dir = arrows.get(dir)
        self.key = key 
        self.rect = pygame.Rect(x, y, ARROW_SIZE, ARROW_SIZE)

    def update(self):
        self.y += ARROW_SPEED
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.dir, (self.x, self.y))

class Game:
    def __init__(self):
        self.arrows = []
        self.last_arrow_time = pygame.time.get_ticks()
        self.score = 0
        self.ratings = [] # List to score ratings and their display times
        self.keys = {
            pygame.K_UP: "A",
            pygame.K_DOWN: "S",
            pygame.K_LEFT: "D", 
            pygame.K_RIGHT: "F"
        }
        self.columns = {
            "A": SCREEN_WIDTH // 4 - ARROW_SIZE, 
            "S": SCREEN_WIDTH // 4 * 2 - ARROW_SIZE, 
            "D": SCREEN_WIDTH // 4 * 3 - ARROW_SIZE, 
            "F": SCREEN_WIDTH - ARROW_SIZE 
        }

    def spawn_arrow(self):
        arrow_key = random.choice(list(self.columns.keys()))
        arrow_x = self.columns[arrow_key]
        if arrow_key == "A":
            arrow_dir = "up"
        elif arrow_key =="S":
            arrow_dir = "down"
        elif arrow_key == "D":
            arrow_dir = "left"
        else:
            arrow_dir = "right"

        new_arrow = Arrow(arrow_x, 0, arrow_dir, arrow_key)
        self.arrows.append(new_arrow)

    def update_arrows(self):
        for arrow in self.arrows:
            arrow.update()
            if arrow.y > SCREEN_HEIGHT:
                self.arrows.remove(arrow)
                self.ratings.append(("Miss", pygame.time.get_ticks(),arrow.x))

    def check_input(self, key):
        for arrow in self.arrows:
            if arrow.key == self.keys[key] and arrow.rect.colliderect(pygame.Rect(arrow.x, SCREEN_HEIGHT - ARROW_SIZE, ARROW_SIZE, ARROW_SIZE)):
                x = arrow.x 
                self.arrows.remove(arrow)
                if abs(arrow.y - (SCREEN_HEIGHT - ARROW_SIZE)) < ARROW_SIZE: #PERFEC HIT RANGE 
                    self.ratings.append(("Perfect", pygame.time.get_ticks(),x))
                    self.score += 1
                else:
                    self.ratings.append(("Miss", pygame.time.get_ticks(),x))

                break

    def draw_ratings(self, current_time):
        #print(self.ratings)
        for rating, timestamp, x in list(self.ratings):
            if current_time - timestamp < 1000:  #show rating for 1 second 
                rating_text = font.render(rating, True, Green if rating == "Perfect" else Red)
                screen.blit(rating_text, (x - rating_text.get_width() // 2, SCREEN_HEIGHT // 2 - rating_text.get_height() // 2 ))
            else:
                self.ratings.remove((rating,  timestamp,x))

    def run(self):
        running = True
        while running:
            screen.fill(Black)
            current_time = pygame.time.get_ticks()
            if current_time - self.last_arrow_time > ARROW_INTERVAL:
                self. spawn_arrow()
                self.last_arrow_time = current_time

            self.update_arrows()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in self.keys:
                        self.check_input(event.key)

            screen.blit(arrows.get("up"), (self.columns.get("A"),SCREEN_HEIGHT-ARROW_SIZE))

            screen.blit(arrows.get("down"), (self.columns.get("S"),SCREEN_HEIGHT-ARROW_SIZE))

            screen.blit(arrows.get("left"), (self.columns.get("D"),SCREEN_HEIGHT-ARROW_SIZE))

            screen.blit(arrows.get("right"), (self.columns.get("F"),SCREEN_HEIGHT-ARROW_SIZE))
            
            for arrow in self.arrows:
                arrow.draw(screen)

            score_text = font.render(f"Score:{self.score}", True, White)
            screen.blit(score_text, (10, 10))


            #Draw ratings
            self.draw_ratings(current_time)

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()

    