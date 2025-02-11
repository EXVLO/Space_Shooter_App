import pygame
import sys

from Shared_Resources import (SCREEN_WIDTH, SCREEN_HEIGHT,)

from Login_Register import show_login_register_window
from Profile import show_profile

from Server import Server
from Client import Client


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main")

server = Server()
server.serv.connect((server.server_host, server.server_port))

client = Client("819", "E.S 2.0")

# Login / Register
show_login_register_window(client, server)

# Send Server Info
server.serv.send(f"$$${client.name}".encode("utf-8"))

# Profile
show_profile(client, server)

