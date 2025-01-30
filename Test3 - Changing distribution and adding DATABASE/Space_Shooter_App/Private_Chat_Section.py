import pygame
import sys
import threading
from threading import Lock
from Shared_Resources import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR,
    BUTTON_COLOR, BUTTON_HOVER_COLOR, TEXT_COLOR_WHITE,
    small_font, font, draw_text,
)

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
message_lock = Lock()  # Lock for thread-safe access to `received_messages`

def receive_messages(curr_client, server):
    while True:
        try:
            message = server.serv.recv(1024).decode("utf-8")
            if message:
                with message_lock:  # Lock to safely modify the list
                    received_messages.append(message)
                    if len(received_messages) > 50:  # Keep the last 50 messages
                        received_messages.pop(0)
        except:
            print("[INFO] Disconnected from server.")
            break

def message_section(curr_client, receiver_name, server):
    global input_text, active_input

    pygame.display.set_caption(f"Chat with {receiver_name}")

    threading.Thread(target=receive_messages, args=(curr_client, server), daemon=True).start()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(WHITE)

        # Display chat header
        header_text = font.render(f"Chat with {receiver_name}", True, BLACK)
        screen.blit(header_text, (50, 50))

        # Display received messages
        y_offset = 100
        with message_lock:  # Lock to safely access the list
            for msg in received_messages[-10:]:  # Display the last 10 messages
                msg_surface = small_font.render(msg, True, BLACK)
                screen.blit(msg_surface, (50, y_offset))
                y_offset += 20

        # Input box
        pygame.draw.rect(screen, GRAY if active_input else WHITE, input_box, border_radius=5)
        pygame.draw.rect(screen, BLACK, input_box, 2, border_radius=5)
        input_surface = small_font.render(input_text, True, BLACK)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        # Return and Send Buttons
        for button, label in [(return_button, "Return"), (send_button, "Send")]:
            color = BUTTON_HOVER_COLOR if button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, button, border_radius=10)
            draw_text(screen, label, small_font, TEXT_COLOR_WHITE, button.centerx, button.centery, align="center")

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
                
                if send_button.collidepoint(event.pos):
                    if input_text.strip():
                        # Format the message to send to the server
                        message = f"{curr_client.name}, {receiver_name}, {input_text.strip()}"
                        server.serv.send(message.encode("utf-8"))

                        # Add the sent message to the local display
                        message2 = f"You: {input_text.strip()}"
                        with message_lock:  # Lock to safely modify the list
                            received_messages.append(message2)
                            if len(received_messages) > 50:  # Keep the last 50 messages
                                received_messages.pop(0)

                        # Clear input box after sending
                        input_text = ""

                if return_button.collidepoint(event.pos):
                    return

            elif event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        message = f"{curr_client.name}, {receiver_name}, {input_text.strip()}"
                        server.serv.send(message.encode("utf-8"))

                        # Add the sent message to the local display
                        message2 = f"You: {input_text.strip()}\n"
                        with message_lock:
                            received_messages.append(message2)
                            if len(received_messages) > 50:
                                received_messages.pop(0)

                        input_text = ""  # Clear input after sending
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        pygame.display.flip()
        clock.tick(30)
