import pygame
import sys
from Shared_Resources import (
        SCREEN_WIDTH, SCREEN_HEIGHT,
        BUTTON_COLOR, BUTTON_HOVER_COLOR,
        font, small_font, TEXT_COLOR_WHITE,
        RANK_COLORS, draw_text
    )

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ranks")

# Return button
return_button = pygame.Rect(int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.9), 80, 30)

# Function to display all ranks in a new window
def show_rank_window():
    rank_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    rank_window.fill((30, 30, 60))
    pygame.display.set_caption("Rank Details")

    draw_text(screen, "Ranks and MMR:", font, TEXT_COLOR_WHITE, int(SCREEN_WIDTH * 0.0125), int(SCREEN_HEIGHT * 0.0167), align="topleft")

    # Rank MMR display
    for i, (rank_name, color) in enumerate(RANK_COLORS.items()):
        rank_mmr = 1000 + i * 500  # MMR for each rank
        draw_text(screen, f"{rank_name} - {rank_mmr} MMR", small_font, color, int(SCREEN_WIDTH * 0.0125), int(SCREEN_HEIGHT * 0.0833 + i * 30), align="topleft")

    pygame.display.flip()

    # Handle rank window events
    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Return Button Handler
        color = BUTTON_HOVER_COLOR if return_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, return_button, border_radius=10)
        draw_text(screen, "Return", small_font, TEXT_COLOR_WHITE, return_button.centerx, return_button.centery, align="center")

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Press Return Button 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    return 

