import pygame
import sys
import random
import time
from Shared_Resources import (
        SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR,
        BUTTON_COLOR, BUTTON_HOVER_COLOR,
        font, small_font, TEXT_COLOR_WHITE, TEXT_COLOR_BLACK,
        RANK_COLORS, draw_text,
    )

window_width = SCREEN_WIDTH
window_height = SCREEN_HEIGHT

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

e4 = pygame.image.load("Explosive Animation\\explosive 4.png").convert_alpha()
e3 = pygame.image.load("Explosive Animation\\explosive 3.png").convert_alpha()
e2 = pygame.image.load("Explosive Animation\\explosive 2.png").convert_alpha()
e1 = pygame.image.load("Explosive Animation\\explosive 1.png").convert_alpha()

# "Other Skins\\SpaceShip2.png"
# "Other Skins\\SpaceShip3.png"
spaceship_img = pygame.image.load("Main Skins\\SpaceShip1.png").convert_alpha()
lazer_img = pygame.image.load("Main Skins\\Lazer.png").convert_alpha()
ufo_img = pygame.image.load("Main Skins\\UFO1.png").convert_alpha()
space_img = pygame.image.load("Main Skins\\Space1.jpg").convert_alpha()
lost_img = pygame.image.load("Main Skins\\Lost_Space.jpg").convert_alpha()
start_img = pygame.image.load("Main Skins\\Start_space.jpg").convert_alpha()

class explosion:
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

        text_name = font.render(string_name, True, TEXT_COLOR_WHITE)

        screen.blit(start_img, (0, 0))
        screen.blit(text_name, (window_width / 2 - text_name.get_width() / 2, window_height * 1 / 5))

    def end(self, time):
        string_lost = f"Game Over!"
        string_ships_destroyed = f"Ships Destroyed: {score}"
        string_time_survived = f"Time Survived: {int(time)}"
        string_final_score = f"Final Calculated Score: {(score * time / 2):.2f}"


        text_Lost = font.render(string_lost, True, TEXT_COLOR_WHITE)
        text_final_score = font.render(string_ships_destroyed, True, TEXT_COLOR_WHITE)
        text_time_survived = font.render(string_time_survived, True, TEXT_COLOR_WHITE)
        text_final_points = font.render(string_final_score, True, TEXT_COLOR_WHITE)

        screen.blit(lost_img, (0, 0))
        screen.blit(text_Lost, (window_width / 2 - text_Lost.get_width() / 2, window_height * 1 / 5))
        screen.blit(text_final_score, (window_width / 2 - text_final_score.get_width() / 2, window_height * 2 / 5))
        screen.blit(text_time_survived, (window_width / 2 - text_time_survived.get_width() / 2, window_height * 3 / 5))
        screen.blit(text_final_points, (window_width / 2 - text_final_points.get_width() / 2, window_height * 4 / 5))

    def draw(self, time):
        text_score = font.render(f"Ships Destroyed: {score}", True, TEXT_COLOR_BLACK)
        text_wave = font.render(f"Wave: {wave}", True, TEXT_COLOR_WHITE)
        text_time = font.render(f"Time: {int(time)}", True, TEXT_COLOR_WHITE)
        text_health = font.render(f"Health: {health}", True, TEXT_COLOR_BLACK)

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

# Return button at the bottom left
start_button = pygame.Rect(int(SCREEN_WIDTH * 0.5 - 70), int(SCREEN_HEIGHT * 0.3), 140, 50)
# Return button at the bottom left
return_button = pygame.Rect(int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.9), 80, 30)

def game(curr_client, server):
    pygame.display.set_caption("Space Shooter")
    global score, health, wave, lazers, ufos, explosives, space_pressed  

    # Reset game variables
    score = 0
    wave = 1
    health = 3
    lazers = []
    ufos = []
    explosives = []

    # Display starting screen
    starting = True
    background.start()
    pygame.display.update()

    # Handle Game window events
    while starting:
        mouse_pos = pygame.mouse.get_pos()

        # Start
        color1 = BUTTON_HOVER_COLOR if start_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color1, start_button, border_radius=10)
        draw_text(screen, "Start", font, TEXT_COLOR_WHITE, start_button.centerx, start_button.centery, align="center")

        # Return
        color2 = BUTTON_HOVER_COLOR if return_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color2, return_button, border_radius=10)
        draw_text(screen, "Return", small_font, TEXT_COLOR_WHITE, return_button.centerx, return_button.centery, align="center")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Start
                if start_button.collidepoint(event.pos):
                    starting = False # Start the Game window and Start to the main window
                # Return
                elif return_button.collidepoint(event.pos):
                    return

    # Initialize game variables
    start_time = time.time()
    score = 0
    wave = 1
    health = 3
    lazers.clear()
    ufos.clear()
    explosives.clear()
    last_shot_time = 0

    # Game Loop
    start_time = time.time()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Calculate elapsed time and wave
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
            space_pressed = False  # Reset when SPACE is released

        # Drawing and updating objects
        background.draw(time_now)
        spaceship.draw()
        spaceship.move()

        # Lazers
        for lazer in lazers:
            lazer.draw()
            lazer.move()
        lazers = [lazer for lazer in lazers if lazer.y > 0]

        # UFOs
        if random.randint(0, 100) < wave * 2:  # spawn chance
            ufos.append(UFO())
        new_ufos = []
        for ufo in ufos:
            ufo_rect = pygame.Rect(ufo.x, ufo.y, ufo_img.get_width(), ufo_img.get_height())
            ufo.draw()
            ufo.move()
            for lazer in lazers:
                lazer_rect = pygame.Rect(lazer.x, lazer.y, lazer_img.get_width(), lazer_img.get_height())
                if lazer_rect.colliderect(ufo_rect):
                    explosives.append(explosion(ufo.x + ufo_img.get_width() // 2, ufo.y + ufo_img.get_height() // 2))
                    score += 1
                    break
            else:
                new_ufos.append(ufo)
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

        # Explosions
        new_explosions = []
        for exp in explosives:
            exp.draw()
            exp.go_phase()
            if exp.phase > 0:
                new_explosions.append(exp)
        explosives = new_explosions

        # Update screen
        pygame.display.update()
        clock.tick(60)

        # Check game over condition
        if health <= 0:
            running = False

    # Game over screen
    time_now = time.time() - start_time
    background.end(time_now)
    if (score * time_now / 2 > curr_client.max_Score):
        server_message = f"%%%NEWREC{round(score * time_now / 2, 2)}, {curr_client.name}"
        server.serv.send(server_message.encode("utf-8"))
        curr_client.update_max_score(score * time_now / 2)
    pygame.display.update()

    # Handle Game window events
    while True:
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER_COLOR if return_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, return_button, border_radius=10)
        draw_text(screen, "Return", small_font, TEXT_COLOR_WHITE, return_button.centerx, return_button.centery, align="center")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    return # Close the Game window and return to the main window


