import pygame
import sys
import socket
from Shared_Resources import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR,
    small_font, font, draw_text,
    server_host, server_port, serv
)

from Client_Handler import curr_Client, curr_Client_Idx, client_list

# Rectangles for the input boxes and buttons
input_box_username = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 40)
input_box_password = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10, 300, 40)
enter_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)

login_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150, 200, 50)  # Login button
register_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 80, 200, 50)  # Register button

def show_login_register_window():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Login/Register")

    choice = None
    username_text = ""
    password_text = ""
    input_active_username = False
    input_active_password = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BACKGROUND_COLOR)

        draw_text(
            screen, "Login or Register", font, TEXT_COLOR,
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 - 19 - 8, align="center"
        )

        if choice is None:
            # Login button
            color = BUTTON_HOVER_COLOR if login_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, login_button, border_radius=10)
            draw_text(screen, "Login", small_font, TEXT_COLOR, login_button.centerx, login_button.centery, align="center")

            # Register button
            color = BUTTON_HOVER_COLOR if register_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, register_button, border_radius=10)
            draw_text(screen, "Register", small_font, TEXT_COLOR, register_button.centerx, register_button.centery, align="center")

        else:
            # Username input box
            color_username = (40, 40, 80) if input_active_username else (30, 30, 60)
            pygame.draw.rect(screen, color_username, input_box_username, border_radius=8)
            draw_text(screen, username_text, small_font, TEXT_COLOR, input_box_username.x + 10, input_box_username.centery, align="midleft")

            # Password input box
            color_password = (40, 40, 80) if input_active_password else (30, 30, 60)
            pygame.draw.rect(screen, color_password, input_box_password, border_radius=8)
            draw_text(screen, "*" * len(password_text), small_font, TEXT_COLOR, input_box_password.x + 10, input_box_password.centery, align="midleft")

            # Enter button
            color = BUTTON_HOVER_COLOR if enter_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, enter_button, border_radius=10)
            draw_text(screen, "Enter", small_font, TEXT_COLOR, enter_button.centerx, enter_button.centery, align="center")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if choice is None:
                    if login_button.collidepoint(event.pos):
                        choice = 0  # Login
                    elif register_button.collidepoint(event.pos):
                        choice = 1  # Register
                elif choice is not None:
                    if input_box_username.collidepoint(event.pos):
                        input_active_username = True
                        input_active_password = False
                    elif input_box_password.collidepoint(event.pos):
                        input_active_username = False
                        input_active_password = True
                    else:
                        input_active_username = False
                        input_active_password = False

                    if enter_button.collidepoint(event.pos):
                        curr_Client.change_Name(username_text)
                        curr_Client.change_Pass(password_text)

                        try:
                            if choice == 0:  # Login
                                serv.send(f"$$${curr_Client.name}".encode("utf-8"))
                                #serv.send(f"LOGIN {curr_Client.name} {curr_Client.password}".encode("utf-8"))
                            elif choice == 1:  # Register
                                #serv.send(f"REGISTER {curr_Client.name} {curr_Client.password}".encode("utf-8"))
                                serv.send(f"$$${curr_Client.name}".encode("utf-8"))

                            print(f"{'Login' if choice == 0 else 'Register'} with Username: {username_text} and Password: {password_text}")
                            return

                        except socket.error as e:
                            print(f"Socket error: {e}")
                            return

            elif event.type == pygame.KEYDOWN:
                if choice is not None:
                    if input_active_username:
                        if event.key == pygame.K_BACKSPACE:
                            username_text = username_text[:-1]
                        elif len(username_text) < 20:
                            username_text += event.unicode

                    elif input_active_password:
                        if event.key == pygame.K_BACKSPACE:
                            password_text = password_text[:-1]
                        elif len(password_text) < 20:
                            password_text += event.unicode
