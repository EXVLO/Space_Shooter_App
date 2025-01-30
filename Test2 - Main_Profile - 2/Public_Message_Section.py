import pygame
import sys
from Shared_Resources import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR,
    small_font, font, draw_text
)

from Client_Handler import (curr_Client, curr_Client_Idx, client_list)
from Personal_Chat_Section import message_section

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Message Friends")

# Colors
WHITE = (60, 60, 120)
BLACK = (0, 0, 0)
LIGHT_GRAY = (190, 190, 190)
DARK_GRAY = (50, 50, 50)

# Button dimensions
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40

# Create buttons for each friend
def create_buttons():
    buttons = []
    y_offset = 100
    for friend in curr_Client.friends:
        button_rect = pygame.Rect(500, y_offset, BUTTON_WIDTH, BUTTON_HEIGHT)
        buttons.append((friend, button_rect))
        y_offset += 60
    return buttons

def draw_buttons(buttons):
    for friend, rect in buttons:
        pygame.draw.rect(screen, LIGHT_GRAY, rect)
        text = font.render("Message", True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def draw_friend_list():
    y_offset = 100
    for friend in curr_Client.friends:
        text = font.render(friend, True, BLACK)
        screen.blit(text, (100, y_offset))
        y_offset += 60

# Return button at the bottom left
return_button = pygame.Rect(int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.9), 80, 30)

def show_public_message_section():
    clock = pygame.time.Clock()
    buttons = create_buttons()

    while True:
        screen.fill(WHITE)
        
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER_COLOR if return_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, return_button, border_radius=10)
        draw_text(screen, "Return", small_font, TEXT_COLOR, return_button.centerx, return_button.centery, align="center")
        # Draw friend list and buttons
        draw_friend_list()
        draw_buttons(buttons)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if return_button.collidepoint(event.pos):
                    return 
                for friend, rect in buttons:
                    if rect.collidepoint(mouse_pos):
                        message_section(friend)  # Switch to message section

        pygame.display.flip()
        clock.tick(30)
