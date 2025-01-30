import pygame
import sys
from Friend_List import show_friend_window
from MMR_Rankings import show_rank_window
from Settings import show_settings_window
from Space_Shooter_Game import game
from Public_Chat_Section import show_public_message_section
from Shared_Resources import (
        SCREEN_WIDTH, SCREEN_HEIGHT, 
        BACKGROUND_COLOR,
        BUTTON_COLOR, BUTTON_HOVER_COLOR,
        font, small_font, TEXT_COLOR_WHITE, TEXT_COLOR_BLACK,
        RANK_COLORS, draw_text 
    )

# Buttons for Profile
buttons = [
    {"label": "Message Section", "rect": pygame.Rect(int(SCREEN_WIDTH * 1 / 21), int(SCREEN_HEIGHT * 0.9), 150, 40)},
    {"label": "Game Section", "rect": pygame.Rect(int(SCREEN_WIDTH * 6 / 21), int(SCREEN_HEIGHT * 0.9), 150, 40)},
    {"label": "Settings Section", "rect": pygame.Rect(int(SCREEN_WIDTH * 11 / 21), int(SCREEN_HEIGHT * 0.9), 150, 40)},
    {"label": "View Ranks", "rect": pygame.Rect(int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.1), 120, 30)},
    {"label": "Friend Section", "rect": pygame.Rect(int(SCREEN_WIDTH  * 16 / 21), int(SCREEN_HEIGHT * 0.9), 150, 40)},  
    {"label": "Statistics", "rect": pygame.Rect(int(SCREEN_WIDTH  * 0.6), int(SCREEN_HEIGHT * 0.1), 120, 30)},  
]

# Initialize Pygame
pygame.init()

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Profile")

def show_profile(curr_client, server):
    # Profile loop
    running = True
    while running:

        # Handle Buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if buttons[0]["rect"].collidepoint(mouse_pos):  # Public Message Section 
                    show_public_message_section(curr_client, server)
                    pygame.display.set_caption("Main")
                elif buttons[1]["rect"].collidepoint(mouse_pos):  # Game button 
                    game(curr_client, server)
                    pygame.display.set_caption("Main")
                elif buttons[2]["rect"].collidepoint(mouse_pos):  # Settings button 
                    show_settings_window(curr_client, server)
                    pygame.display.set_caption("Main")
                elif buttons[3]["rect"].collidepoint(mouse_pos):  # Ranks button
                    show_rank_window()
                    pygame.display.set_caption("Main")
                elif buttons[4]["rect"].collidepoint(mouse_pos):  # Friend Section button
                    show_friend_window(curr_client)
                    pygame.display.set_caption("Main")
                elif buttons[5]["rect"].collidepoint(mouse_pos):  # Statistics
                    pass
                    pygame.display.set_caption("Main")
           
        # Screen Background
        screen.fill(BACKGROUND_COLOR)

        # MMR and Rank 
        mmr_txt = f"MMR: {int(curr_client.mmr)}"
        draw_text(screen, mmr_txt, font, RANK_COLORS[curr_client.rank], int(SCREEN_WIDTH * 0.025), int(SCREEN_HEIGHT * 0.22), align="topleft")

        # Max Score 
        max_score_txt = f"Max Score: {(curr_client.max_Score):.2f}"
        draw_text(screen, max_score_txt, font, RANK_COLORS[curr_client.rank], int(SCREEN_WIDTH * 0.025), int(SCREEN_HEIGHT * 0.28), align="topleft")

        # Profile Section
        rank_txt = f"Rank: {curr_client.rank}"
        pygame.draw.rect(screen, (50, 50, 50), (0, 30, SCREEN_WIDTH, 90))
        draw_text(screen, rank_txt, font, RANK_COLORS[curr_client.rank], int(SCREEN_WIDTH * 0.025), int(SCREEN_HEIGHT * 0.1333), align="topleft")

        draw_text(screen, f"Profile: {curr_client.name}", font, RANK_COLORS[curr_client.rank], int(SCREEN_WIDTH * 0.025), int(SCREEN_HEIGHT * 0.0667))

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            color = BUTTON_HOVER_COLOR if button["rect"].collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, button["rect"], border_radius=10)
            draw_text(screen, button["label"], small_font, TEXT_COLOR_WHITE, button["rect"].centerx, button["rect"].centery, align="center")

        # Update display
        pygame.display.flip()

