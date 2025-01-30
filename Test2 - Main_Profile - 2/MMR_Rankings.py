import pygame
import sys
from Shared_Resources import (
        SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR,
        BUTTON_COLOR, BUTTON_HOVER_COLOR, buttons,
        font, small_font, TEXT_COLOR,
        RANK_COLORS, draw_text
    )

from Client_Handler import (curr_Client, curr_Client_Idx, client_list)

window_width = SCREEN_WIDTH
window_height = SCREEN_HEIGHT

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("MMR Ranks")

# Function to display all ranks in a new window
def show_rank_window():
    rank_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Keep same size as the main window
    rank_window.fill((30, 30, 30))
    pygame.display.set_caption("Rank Details")

    draw_text(screen, "Ranks and MMR:", font, TEXT_COLOR, int(SCREEN_WIDTH * 0.0125), int(SCREEN_HEIGHT * 0.0167), align="topleft")

    # Adjust the rank MMR display
    for i, (rank_name, color) in enumerate(RANK_COLORS.items()):
        rank_mmr = 1000 + i * 500  # Example MMR for each rank
        draw_text(screen, f"{rank_name} - {rank_mmr} MMR", small_font, color, int(SCREEN_WIDTH * 0.0125), int(SCREEN_HEIGHT * 0.0833 + i * 30), align="topleft")

    # Return button at the bottom left
    return_button = pygame.Rect(int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.9), 80, 30)

    pygame.display.flip()

    # Handle rank window events
    while True:
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER_COLOR if return_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, return_button, border_radius=10)
        draw_text(screen, "Return", small_font, TEXT_COLOR, return_button.centerx, return_button.centery, align="center")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    return # Close the Game window and return to the main window
