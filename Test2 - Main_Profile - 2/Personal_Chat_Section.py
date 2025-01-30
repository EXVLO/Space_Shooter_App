import pygame
import sys
import socket
import threading
from Shared_Resources import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR,
    small_font, font, draw_text,
    server_host, server_port, serv
)

from Client_Handler import (curr_Client, curr_Client_Idx, client_list)

serv.connect((server_host, server_port))
serv.send(f"$$${curr_Client.name}".encode("utf-8"))
# Sender's name
sender_name = curr_Client.name

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Buttons
return_button = pygame.Rect(int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.9), 80, 30)
send_button = pygame.Rect(int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.9), 80, 30)

# Text input box
input_box = pygame.Rect(50, int(SCREEN_HEIGHT * 0.8), SCREEN_WIDTH - 100, 30)
active_input = False
input_text = ""

# Messages to display
received_messages = []

def receive_messages():
    while True:
        try:
            message = serv.recv(1024).decode("utf-8")
            if message:
                received_messages.append(message)
        except:
            print("[INFO] Disconnected from server.")
            serv.close()
            break

threading.Thread(target=receive_messages, daemon=True).start()


def message_section(receiver_name):
    global input_text, active_input

    pygame.display.set_caption(f"Chat with {receiver_name}")

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(WHITE)

        # Display chat header
        header_text = font.render(f"Chat with {receiver_name}", True, BLACK)
        screen.blit(header_text, (50, 50))

        # Display received messages
        y_offset = 100
        for msg in received_messages[-10:]:  # Display the last 10 messages
            msg_surface = small_font.render(msg, True, BLACK)
            screen.blit(msg_surface, (50, y_offset))
            y_offset += 20

        # Input box
        pygame.draw.rect(screen, GRAY if active_input else WHITE, input_box, border_radius=5)
        pygame.draw.rect(screen, BLACK, input_box, 2, border_radius=5)
        input_surface = small_font.render(input_text, True, BLACK)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        # Return Button
        color = BUTTON_HOVER_COLOR if return_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, return_button, border_radius=10)
        draw_text(screen, "Return", small_font, TEXT_COLOR, return_button.centerx, return_button.centery, align="center")

        # Send Button
        color = BUTTON_HOVER_COLOR if send_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, send_button, border_radius=10)
        draw_text(screen, "Send", small_font, TEXT_COLOR, send_button.centerx, send_button.centery, align="center")

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active_input = True
                else:
                    active_input = False
                
                # Send Message
                if send_button.collidepoint(event.pos):
                    if input_text.strip():
                        message = f"{curr_Client.name}, {receiver_name}, {input_text.strip()}"
                        serv.send(message.encode("utf-8"))
                        input_text = "" 

                if return_button.collidepoint(event.pos):
                    return

                pygame.display.update()

            elif event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        message = f"{sender_name}, {receiver_name}, {input_text.strip()}"
                        input_text = ""  # Clear input after sending
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        pygame.display.flip()
        clock.tick(30)