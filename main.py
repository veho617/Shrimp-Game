import pygame as py
import random
import time

py.init()

#Variables
screen_width = 1600
screen_height = 1000
screen_size = (screen_width, screen_height)
screen = py.display.set_mode(screen_size)
py.display.set_caption("Veho Shrimp Game")
clock = py.time.Clock()
fps = 60
bowl_x = 500
bowl_y = 700
bowl_velocity = 20
score = 0
highscore = 0
start_time = time.time()
game_over = False
font = py.font.Font(None, 74)
shrimp_width =100
shrimp_height = 100

#Images
bg = py.image.load("bg.png")
bowl = py.image.load("bowl.png")
bowl = py.transform.scale(bowl, (175, 175)) #gotta transform beacue i drew it too big on gimp

#Sprite, idk sprite groups yet
class Shrimp(py.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = py.image.load("shrimp.png")
        self.image = py.transform.scale(self.image, (shrimp_width, shrimp_height)) 
       
        self.rect = self.image.get_rect()
        
        self.rect.topleft = (x, y)
        
        self.velocity = random.randint(6, 10)

    def update(self):
        self.rect.y += self.velocity
        if self.rect.top > screen_height:
            self.rect.y = -100
            self.rect.x = random.randint(0, screen_width - self.rect.width)


shrimp_group = py.sprite.Group()


for i in range(5):
    shrimp = Shrimp(random.randint(0, screen_width - 100), random.randint(-300, -100))
    shrimp_group.add(shrimp)


def display_score_and_timer():
    global highscore
    remaining_time = max(0, 15 - int(time.time() - start_time))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    timer_text = font.render(f"Time: {remaining_time}s", True, (0, 0, 0))
    highscore_text = font.render(f"Highscore: {highscore}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (10, 90))
    screen.blit(highscore_text, (10, 170))


def game_over_screen():
    global highscore
    if score > highscore:
        highscore = score

    #making the text
    screen.fill((0, 0, 0))
    game_over_text = font.render("Time's Up!", True, (255, 0, 0))
    final_score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
    try_again_text = font.render("Press R to Try Again", True, (255, 255, 255))
    highscore_text = font.render(f"Highscore: {highscore}", True, (255, 255, 0))

    #putting it on screen
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, 300)) #width is in the middle, the middle of the text width is in the middle of the screen. same with the rest
    screen.blit(final_score_text, (screen_width // 2 - final_score_text.get_width() // 2, 400))
    screen.blit(try_again_text, (screen_width // 2 - try_again_text.get_width() // 2, 500))
    screen.blit(highscore_text, (screen_width // 2 - highscore_text.get_width() // 2, 600))

    py.display.flip()

#Game Loop
run = True
while run:

    # Interrupt handling
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

        if game_over and event.type == py.KEYDOWN and event.key == py.K_r:
            score = 0
            start_time = time.time() #time keeper for start
            game_over = False

    if not game_over:
        #movement handling
        keys = py.key.get_pressed()
        if keys[py.K_LEFT] and bowl_x > 0:
            bowl_x -= bowl_velocity
        if keys[py.K_RIGHT] and bowl_x < screen_width - bowl.get_width():
            bowl_x += bowl_velocity

        # Collisions
        for shrimp in shrimp_group:
            if shrimp.rect.colliderect(py.Rect(bowl_x, bowl_y, bowl.get_width(), bowl.get_height())):
                score += 1
                shrimp.rect.y = -100
                shrimp.rect.x = random.randint(0, screen_width - shrimp.rect.width)

        
        if time.time() - start_time >= 15: #current time elapsed exceeds 15s
            game_over = True

        clock.tick(fps)
        screen.blit(bg, (0, 0))

        
        screen.blit(bowl, (bowl_x, bowl_y))
        shrimp_group.update()
        shrimp_group.draw(screen)

        
        display_score_and_timer()

        py.display.flip()
    else:
        game_over_screen()

py.quit()