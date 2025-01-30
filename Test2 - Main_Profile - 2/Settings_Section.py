import pygame
import sys
from Shared_Resources import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR, BUTTON_COLOR_RED, BUTTON_HOVER_COLOR_RED,
    font, small_font, draw_text,
)

from Client_Handler import (curr_Client, curr_Client_Idx, client_list)

# Function to display the Settings Section
def show_settings_window():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Settings Section")

    # UI elements
    return_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
    delete_account_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 170, 200, 50)

    # Main loop for the Settings Section
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BACKGROUND_COLOR)

        # Draw "Settings Section" title
        draw_text(screen, "Settings Section", font, TEXT_COLOR, SCREEN_WIDTH // 2, 40, align="center")

        # Display username, password, and account creation date
        draw_text(screen, f"Username: {curr_Client.name}", small_font, TEXT_COLOR, 100, 100, align="topleft")
        draw_text(screen, f"Password: {curr_Client.password}", small_font, TEXT_COLOR, 100, 150, align="topleft")
        draw_text(screen, f"Account Created: {curr_Client.account_created}", small_font, TEXT_COLOR, 100, 200, align="topleft")

        # Delete Account Button
        color = BUTTON_HOVER_COLOR_RED if delete_account_button.collidepoint(mouse_pos) else BUTTON_COLOR_RED
        pygame.draw.rect(screen, color, delete_account_button, border_radius=10)
        draw_text(screen, "Delete Account", small_font, TEXT_COLOR, delete_account_button.centerx, delete_account_button.centery, align="center")

        # Return Button
        color = BUTTON_HOVER_COLOR if return_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, return_button, border_radius=10)
        draw_text(screen, "Return", small_font, TEXT_COLOR, return_button.centerx, return_button.centery, align="center")

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    return  # Return to the previous screen
                elif delete_account_button.collidepoint(event.pos):
                    confirm_delete = show_confirmation_popup(screen)
                    if confirm_delete:
                        # Handle account deletion logic here
                        print("Account Deleted!")  # Replace with actual account deletion logic
                        pygame.quit()
                        sys.exit()

# Function to display a confirmation popup for account deletion
def show_confirmation_popup(screen):
    popup_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    confirm_button = pygame.Rect(popup_rect.centerx - 100, popup_rect.centery + 30, 80, 40)
    cancel_button = pygame.Rect(popup_rect.centerx + 20, popup_rect.centery + 30, 80, 40)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (40, 40, 40), popup_rect, border_radius=10)
        draw_text(screen, "Are you sure you want to delete your account?", small_font, TEXT_COLOR, popup_rect.centerx, popup_rect.y + 40, align="center")

        # Yes Button
        color = BUTTON_HOVER_COLOR_RED if confirm_button.collidepoint(mouse_pos) else BUTTON_COLOR_RED
        pygame.draw.rect(screen, color, confirm_button, border_radius=10)
        draw_text(screen, "Yes", small_font, TEXT_COLOR, confirm_button.centerx, confirm_button.centery, align="center")

        # No
        color = BUTTON_HOVER_COLOR if cancel_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, cancel_button, border_radius=10)
        draw_text(screen, "Return", small_font, TEXT_COLOR, cancel_button.centerx, cancel_button.centery, align="center")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if confirm_button.collidepoint(event.pos):
                    return True  # Confirm deletion
                elif cancel_button.collidepoint(event.pos):
                    return False  # Cancel deletion

