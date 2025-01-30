import pygame
import sys
import json
from Shared_Resources import (
        SCREEN_WIDTH, SCREEN_HEIGHT, 
        BACKGROUND_COLOR,
        BUTTON_COLOR, BUTTON_HOVER_COLOR,
        font, small_font, TEXT_COLOR_WHITE, TEXT_COLOR_BLACK,
        RANK_COLORS, draw_text 
    )

from Client import Client

red_color = (248, 19, 19)

# Rectangles for the input boxes and buttons
input_box_username = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 40) # Username Button
input_box_password = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10, 300, 40) # Password
enter_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50) # Enter Button

login_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150, 200, 50)  # Login button
register_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 80, 200, 50)  # Register button

# Return button
return_button = pygame.Rect(int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.9), 80, 30)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Login/Register")

def show_login_register_window(curr_client, server):
    choice = None
    username_text = ""
    password_text = ""
    input_active_username = False
    input_active_password = False
    error_id = 0

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BACKGROUND_COLOR)

        draw_text(screen, "Login or Register", font, TEXT_COLOR_WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 - 19 - 8, align="center")

        if choice is None:
            # Login button
            color = BUTTON_HOVER_COLOR if login_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, login_button, border_radius=10)
            draw_text(screen, "Login", small_font, TEXT_COLOR_WHITE, login_button.centerx, login_button.centery, align="center")

            # Register button
            color = BUTTON_HOVER_COLOR if register_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, register_button, border_radius=10)
            draw_text(screen, "Register", small_font, TEXT_COLOR_WHITE, register_button.centerx, register_button.centery, align="center")

        else:
            if error_id == -1:
                txt_error1 = "Username not found"
                draw_text(screen, txt_error1, small_font, red_color, input_box_username.x + 70, input_box_username.centery - 40, align="midleft")
            elif error_id == -2:
                txt_error2 = "Password is incorrect"
                draw_text(screen, txt_error2, small_font, red_color,  input_box_username.x + 70, input_box_username.centery - 40, align="midleft")
            elif error_id == -3:
                txt_error3 = "Username already exists"
                draw_text(screen, txt_error3, small_font, red_color,  input_box_username.x + 52, input_box_username.centery - 40, align="midleft")

            # Username input box
            color_username = (40, 40, 80) if input_active_username else (30, 30, 60)
            pygame.draw.rect(screen, color_username, input_box_username, border_radius=8)
            draw_text(screen, username_text, small_font, TEXT_COLOR_WHITE, input_box_username.x + 10, input_box_username.centery, align="midleft")

            # Password input box
            color_password = (40, 40, 80) if input_active_password else (30, 30, 60)
            pygame.draw.rect(screen, color_password, input_box_password, border_radius=8)
            draw_text(screen, "*" * len(password_text), small_font, TEXT_COLOR_WHITE, input_box_password.x + 10, input_box_password.centery, align="midleft")

            # Enter button
            color = BUTTON_HOVER_COLOR if enter_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, enter_button, border_radius=10)
            draw_text(screen, "Enter", small_font, TEXT_COLOR_WHITE, enter_button.centerx, enter_button.centery, align="center")

            # Return Button Handler
            color = BUTTON_HOVER_COLOR if return_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, return_button, border_radius=10)
            draw_text(screen, "Return", small_font, TEXT_COLOR_WHITE, return_button.centerx, return_button.centery, align="center")

        pygame.display.flip()

        # Handle Buttons
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
                    if return_button.collidepoint(event.pos):
                        choice = None
                        input_active_username = False
                        input_active_password = False
                        username_text = ""
                        password_text = ""
                        error_id = 0
                        continue
                    elif input_box_username.collidepoint(event.pos): # Username
                        input_active_username = True
                        input_active_password = False
                    elif input_box_password.collidepoint(event.pos): # Password
                        input_active_username = False
                        input_active_password = True
                    else: # Screen
                        input_active_username = False
                        input_active_password = False
                    
                    # Enter Button
                    if enter_button.collidepoint(event.pos):
                        if choice == 0:  # Login
                            # Prepare the login message to send to the server
                            server_message = f"%%%LOGIN{username_text}, {password_text}"
                            server.serv.send(server_message.encode("utf-8"))

                            # Wait for the server's response
                            received_message = server.serv.recv(1024).decode("utf-8")

                            # Handle the server's response
                            if received_message == "-1":
                                error_id = -1
                                print("Username not found")
                            elif received_message == "-2":
                                error_id = -2
                                print("Password is incorrect")
                            else:
                                try:
                                    # Parse the JSON response
                                    response = json.loads(received_message)

                                    # Update the client's data
                                    curr_client.change_Name(response["name"])
                                    curr_client.change_Pass(response["password"])
                                    curr_client.account_created = response["acc_created"]
                                    curr_client.update_max_score(float(response["max_score"]))
                                    curr_client.friends = response["friend_list"]

                                    print(f"Welcome back {response['name']}!")
                                    print(f"Your friends: {curr_client.friends}")
                                except json.JSONDecodeError as e:
                                    print(f"Error decoding server response: {e}")
                                except KeyError as e:
                                    print(f"Missing key in server response: {e}")
                                return
                        else:  # Register
                            server_message = f"%%%REGISTER{username_text}, {password_text}"
                            server.serv.send(server_message.encode("utf-8"))

                            recieved_message = server.serv.recv(1024).decode("utf-8")
                            if recieved_message == "-1":
                                error_id = -3
                                print("Username already exists")
                            else:  # Registration success
                                curr_client.change_Name(username_text)
                                curr_client.change_Pass(password_text)
                                print(f"Welcome {username_text}, Good Luck!")
                                return
            
            # Keyboard Inputs
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
