import pygame
import sys
from Shared_Resources import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_HOVER_COLOR_RED, BUTTON_COLOR_RED,
    font, small_font,
    TEXT_COLOR_WHITE, draw_text,
)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Friend Section")


return_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 60, 100, 40)
input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 110, 300, 40)
add_button = pygame.Rect(SCREEN_WIDTH // 2 + 160, SCREEN_HEIGHT - 110, 120, 40)


# Function to display the friends list in a new window
def show_friend_window(curr_client):

    screen.fill(BACKGROUND_COLOR)

    # Draw a gradient background
    for i in range(SCREEN_HEIGHT):
        pygame.draw.line(screen, (30 + i // 20, 30 + i // 20, 70 + i // 10), (0, i), (SCREEN_WIDTH, i))

    # Draw the "Friends List" title
    draw_text(screen, "Friends List", font, TEXT_COLOR_WHITE, SCREEN_WIDTH // 2, 40, align="center")

    # Function to render the friends list
    def render_friends():
        screen.fill(BACKGROUND_COLOR)
        for i in range(SCREEN_HEIGHT):
            pygame.draw.line(screen, (30 + i // 20, 30 + i // 20, 70 + i // 10), (0, i), (SCREEN_WIDTH, i))
        draw_text(screen, "Friends List", font, TEXT_COLOR_WHITE, SCREEN_WIDTH // 2, 40, align="center")

        # Redraw the friends list
        friend_card_width = int(SCREEN_WIDTH * 0.7)
        friend_card_height = 40
        card_x = int(SCREEN_WIDTH * 0.1)

        for i, friend in enumerate(curr_client.friends):
            card_y = 80 + i * (friend_card_height + 10)
            friend_card = pygame.Rect(card_x, card_y, friend_card_width, friend_card_height)
            pygame.draw.rect(screen, (50, 50, 80), friend_card, border_radius=8)
            draw_text(screen, friend, small_font, TEXT_COLOR_WHITE, friend_card.x + 10, friend_card.centery, align="midleft")

            # Remove button
            remove_button = pygame.Rect(card_x + friend_card_width + 10, card_y, 100, friend_card_height)
            mouse_pos = pygame.mouse.get_pos()
            color = BUTTON_HOVER_COLOR_RED if remove_button.collidepoint(mouse_pos) else BUTTON_COLOR_RED
            pygame.draw.rect(screen, color, remove_button, border_radius=8)
            draw_text(screen, "Remove", small_font, TEXT_COLOR_WHITE, remove_button.centerx, remove_button.centery, align="center")
            buttons.append((remove_button, i))  # Store the button rect and friend index


    buttons = []  # List of (button_rect, friend_index)
    input_text = ""  # Text input by the user
    render_friends()

    # Handle friend window events
    color1 = (30, 30, 60)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()

        # Return
        color = BUTTON_HOVER_COLOR if return_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, return_button, border_radius=10)
        draw_text(screen, "Return", small_font, TEXT_COLOR_WHITE, return_button.centerx, return_button.centery, align="center")
        buttons.append((return_button, -1)) 

        # Add Friend
        color = BUTTON_HOVER_COLOR if add_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, add_button, border_radius=10)
        draw_text(screen, "Add Friend", small_font, TEXT_COLOR_WHITE, add_button.centerx, add_button.centery, align="center")

        # Draw the input box and "Add Friend" button
        pygame.draw.rect(screen, color1, input_box, border_radius=8)
        draw_text(screen, input_text, small_font, TEXT_COLOR_WHITE, input_box.x + 10, input_box.centery, align="midleft")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                    color1 = (40, 40, 80) 
                else:
                    color1 = (30, 30, 60) 
                    input_active = False

                for button, index in buttons:
                    if button.collidepoint(event.pos):
                        if index == -1:
                            return  # Close the Friends window and return to the main window
                        else:
                            curr_client.remove_Friend(curr_client.friends[index]) # Remove the friend from the list
                            buttons = []  # Clear buttons list for re-rendering
                            render_friends()  # Re-render the updated friends list

                if add_button.collidepoint(event.pos):
                    if input_text.strip():  # Add the friend if text is not empty
                        curr_client.add_Friend(input_text.strip())
                        input_text = ""  # Clear the input box
                        buttons = []  # Clear buttons list for re-rendering
                        render_friends()  # Re-render the updated friends list

            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove the last character
                elif event.key == pygame.K_TAB:
                    if len(input_text) + 4 <= 20:  # Ensure Tab (4 spaces) won't exceed the input limit
                        input_text += "    "  # Add four spaces
                elif len(input_text) < 20:  # Limit input to 20 characters
                    input_text += event.unicode

                # Re-render the screen after updating the input text
                buttons = []  # Clear the buttons list
                render_friends()
