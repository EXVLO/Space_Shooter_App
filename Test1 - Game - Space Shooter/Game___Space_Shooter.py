import pygame
import sys
import random
import time

pygame.init()
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

score = 0
wave = 1
health = 3

font_size = 36
font = pygame.font.Font(None, font_size)

white_text_color = (255, 255, 255)
black_text_color = (0, 0, 0)

e4 = pygame.image.load("Explosive Animation\\explosive 4.png").convert_alpha()
e3 = pygame.image.load("Explosive Animation\\explosive 3.png").convert_alpha()
e2 = pygame.image.load("Explosive Animation\\explosive 2.png").convert_alpha()
e1 = pygame.image.load("Explosive Animation\\explosive 1.png").convert_alpha()

# "Other Skins\\SpaceShip2.png"
# "Other Skins\\SpaceShip3.png"
spaceship_img = pygame.image.load("SpaceShip1.png").convert_alpha()
lazer_img = pygame.image.load("Lazer.png").convert_alpha()
ufo_img = pygame.image.load("UFO1.png").convert_alpha()
space_img = pygame.image.load("Space1.jpg").convert_alpha()
lost_img = pygame.image.load("Lost_Space.jpg").convert_alpha()
start_img = pygame.image.load("Start_space.jpg").convert_alpha()

class eplosion:
    def __init__(self, x, y):
        self.phase = 4
        self.x = x
        self.y = y

    def draw(self):
        if self.phase == 4:
            screen.blit(e4, (self.x - e4.get_width() / 2, self.y - e4.get_height() / 2))
        elif self.phase == 3:
            screen.blit(e3, (self.x - e3.get_width() / 2, self.y - e3.get_height() / 2))
        elif self.phase == 2:
            screen.blit(e2, (self.x - e2.get_width() / 2, self.y - e2.get_height() / 2))
        elif self.phase == 1:
            screen.blit(e1, (self.x - e1.get_width() / 2, self.y - e1.get_height() / 2))

    def go_phase(self):
        self.phase -= 1

class Background:
    def start(self):
        string_name = f"Space Shooter"
        string_info = f"Press Space To Start"

        text_name = font.render(string_name, True, white_text_color)
        text_info = font.render(string_info, True, white_text_color)

        screen.blit(start_img, (0, 0))
        screen.blit(text_name, (window_width / 2 - text_name.get_width() / 2, window_height * 1 / 5))
        screen.blit(text_info, (20, window_height * 9 / 10))

    def end(self, time):
        string_lost = f"Game Over!"
        string_ships_destroyed = f"Ships Destroyed: {score}"
        string_time_survived = f"Time Survived: {int(time)}"
        string_final_score = f"Final Calculated Score: {(score * time / 2):.2f}"
        string_info = f"Press Space To End"


        text_Lost = font.render(string_lost, True, white_text_color)
        text_final_score = font.render(string_ships_destroyed, True, white_text_color)
        text_time_survived = font.render(string_time_survived, True, white_text_color)
        text_final_points = font.render(string_final_score, True, white_text_color)
        text_info = font.render(string_info, True, white_text_color)

        screen.blit(lost_img, (0, 0))
        screen.blit(text_Lost, (window_width / 2 - text_Lost.get_width() / 2, window_height * 1 / 5))
        screen.blit(text_final_score, (window_width / 2 - text_final_score.get_width() / 2, window_height * 2 / 5))
        screen.blit(text_time_survived, (window_width / 2 - text_time_survived.get_width() / 2, window_height * 3 / 5))
        screen.blit(text_final_points, (window_width / 2 - text_final_points.get_width() / 2, window_height * 4 / 5))
        screen.blit(text_info, (20, window_height * 9 / 10))

    def draw(self, time):
        text_score = font.render(f"Ships Destroyed: {score}", True, black_text_color)
        text_wave = font.render(f"Wave: {wave}", True, white_text_color)
        text_time = font.render(f"Time: {int(time)}", True, white_text_color)
        text_health = font.render(f"Health: {health}", True, black_text_color)

        screen.blit(space_img, (0, 0))
        screen.blit(text_score, (window_width / 50, window_height / 50))
        screen.blit(text_wave, (window_width - window_width / 8, window_height / 50))
        screen.blit(text_time, (window_width - window_width / 8, window_height / 50 + 38))
        screen.blit(text_health, (window_width / 50, window_height / 50 + 38))

class Spaceship:
    def __init__(self):
        self.x = window_width // 2 - spaceship_img.get_width() // 2
        self.y = window_height - spaceship_img.get_height()
        self.velocity = 10

    def draw(self):
        screen.blit(spaceship_img, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x = max(0, self.x - self.velocity)
        if keys[pygame.K_RIGHT]:
            self.x = min(window_width - spaceship_img.get_width(), self.x + self.velocity)

class Lazer:
    def __init__(self, x):
        self.x = x
        self.y = spaceship.y

    def draw(self):
        screen.blit(lazer_img, (self.x, self.y))

    def move(self):
        self.y -= 10  

class UFO:
    def __init__(self):
        self.x = random.randint(0, window_width - ufo_img.get_width())
        self.y = -ufo_img.get_height()  # Spawn UFOs at the top
        self.speed = 2  # Adjust UFO speed here

    def draw(self):
        screen.blit(ufo_img, (self.x, self.y))

    def move(self):
        self.y += self.speed

background = Background()
spaceship = Spaceship()
lazers = []
ufos = []
explosives = []

# Shooting delay variables
last_shot_time = 0
shoot_delay = 250  # milliseconds
space_pressed = False

start_time = time.time()
running = True

background.start()
pygame.display.update()

starting = True
while starting:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        starting = False
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        starting = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time_now = time.time() - start_time
    wave = 1 + int(time_now) // 30

    # Handle shooting with delay
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and not space_pressed and current_time - last_shot_time > shoot_delay:
        lazers.append(Lazer(spaceship.x + spaceship_img.get_width() // 2 - lazer_img.get_width() // 2))
        last_shot_time = current_time
        space_pressed = True  # Mark space as pressed

    if not keys[pygame.K_SPACE]:  
        space_pressed = False 


    # Move and draw objects
    background.draw(time_now)
    spaceship.draw()
    spaceship.move()

    for lazer in lazers:
        lazer.draw()
        lazer.move()

    # Remove lasers that go off-screen
    lazers = [lazer for lazer in lazers if lazer.y > 0]

    # Spawn UFOs (adjust frequency as needed)
    if random.randint(0, 100) < wave * 2:
        ufos.append(UFO())

    # Handle UFO movement and collision
    new_ufos = []
    for ufo in ufos:
        ufo_rect = pygame.Rect(ufo.x, ufo.y, ufo_img.get_width(), ufo_img.get_height())
        ufo.draw()
        ufo.move()
        for lazer in lazers:
            lazer_rect = pygame.Rect(lazer.x, lazer.y, lazer_img.get_width(), lazer_img.get_height())
            if lazer_rect.colliderect(ufo_rect):
                # Remove the UFO if hit
                explosives.append(eplosion(lazer.x, lazer.y))
                score += 1
                break
        else:
            new_ufos.append(ufo)  # Keep the UFO if not hit by any laser
    ufos = new_ufos

    # Remove UFOs that go off-screen
    passed_ufos = []
    for ufo in ufos:
        if ufo.y < window_height:
            passed_ufos.append(ufo)
        else:
            health -= 1
            if health == 0:
                running = False
                break

    ufos = passed_ufos

    passed_explos = []
    for exp in explosives:
        exp.draw()
        exp.go_phase()
        if exp.phase != 0:
            passed_explos.append(exp)

    explosives = passed_explos

    pygame.display.update()
    clock.tick(60)

background.end(time_now)
pygame.display.update()

ending = True
while ending:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        ending = False
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        ending = False

player_score = score * time_now / 2
print(player_score)

pygame.quit()
sys.exit() 
