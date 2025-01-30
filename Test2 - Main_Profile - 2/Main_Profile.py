import socket

host = "localhost"
port = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))

# Send a test message (optional)
client_socket.send("Hello, server!".encode("utf-8"))

# Receive a response from the server (optional)
response = client_socket.recv(1024).decode("utf-8")
print(f"Server says: {response}")

# Close the connection
client_socket.close()



# import pygame
# import sys
# from Friends_Section import show_friend_window
# from MMR_Rankings import show_rank_window
# from Settings_Section import show_settings_window
# from Space_Shooter import game
# from Login_Register_Screen import show_login_register_window
# from Public_Message_Section import show_public_message_section
# from Shared_Resources import (
#         SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR,
#         BUTTON_COLOR, BUTTON_HOVER_COLOR, buttons,
#         font, small_font, TEXT_COLOR,
#         RANK_COLORS, draw_text,
#         client
#     )

# from Client_Handler import (curr_Client, curr_Client_Idx, client_list)

# show_login_register_window()

# # Initialize Pygame
# pygame.init()

# # Initialize screen
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Main")

# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             mouse_pos = pygame.mouse.get_pos()
#             if buttons[3]["rect"].collidepoint(mouse_pos):  # Ranks button
#                 show_rank_window()
#                 pygame.display.set_caption("Main")
#             elif buttons[4]["rect"].collidepoint(mouse_pos):  # Friend Section button
#                 show_friend_window()
#                 pygame.display.set_caption("Main")
#             elif buttons[1]["rect"].collidepoint(mouse_pos):  # Game button
#                 game()
#                 pygame.display.set_caption("Main")
#             elif buttons[2]["rect"].collidepoint(mouse_pos):  # Settings button 
#                 show_settings_window()
#                 pygame.display.set_caption("Main")
#             elif buttons[0]["rect"].collidepoint(mouse_pos):  # Public Message Section
#                 show_public_message_section()
#                 pygame.display.set_caption("Main")

#     # Clear screen
#     screen.fill(BACKGROUND_COLOR)

#     # MMR and Rank 
#     mmr_txt = f"MMR: {int(curr_Client.mmr)}"
#     draw_text(screen, mmr_txt, font, RANK_COLORS[curr_Client.rank], int(SCREEN_WIDTH * 0.025), int(SCREEN_HEIGHT * 0.22), align="topleft")

#     # Max Score 
#     max_score_txt = f"Max Score: {(curr_Client.max_Score):.2f}"
#     draw_text(screen, max_score_txt, font, RANK_COLORS[curr_Client.rank], int(SCREEN_WIDTH * 0.025), int(SCREEN_HEIGHT * 0.28), align="topleft")

#     # Profile Section
#     rank_txt = f"Rank: {curr_Client.rank}"
#     pygame.draw.rect(screen, (50, 50, 50), (0, 30, SCREEN_WIDTH, 90))
#     draw_text(screen, rank_txt, font, RANK_COLORS[curr_Client.rank], int(SCREEN_WIDTH * 0.025), int(SCREEN_HEIGHT * 0.1333), align="topleft")

#     draw_text(screen, f"Profile: {curr_Client.name}", font, RANK_COLORS[curr_Client.rank], int(SCREEN_WIDTH * 0.025), int(SCREEN_HEIGHT * 0.0667))

#     # Buttons
#     mouse_pos = pygame.mouse.get_pos()
#     for button in buttons:
#         color = BUTTON_HOVER_COLOR if button["rect"].collidepoint(mouse_pos) else BUTTON_COLOR
#         pygame.draw.rect(screen, color, button["rect"], border_radius=10)
#         draw_text(screen, button["label"], small_font, TEXT_COLOR, button["rect"].centerx, button["rect"].centery, align="center")

#     # Update display
#     pygame.display.flip()

# # Quit Pygame
# pygame.quit()
# sys.exit()
