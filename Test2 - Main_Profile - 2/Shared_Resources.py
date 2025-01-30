# shared_resources.py
import pygame
import socket
from datetime import datetime

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = '127.0.0.1'
server_port=12345

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)

# White Text
TEXT_COLOR = (255, 255, 255)

# Blue Buttons
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)

# Red buttons
BUTTON_COLOR_RED = (139, 0, 0)
BUTTON_HOVER_COLOR_RED = (255, 127, 127)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

font_size = 36
font = pygame.font.Font(None, font_size)

white_text_color = (255, 255, 255)
black_text_color = (0, 0, 0)

# Rank Colors
RANK_COLORS = {
    "Thruster Scout III": (200, 200, 200),
    "Thruster Scout II": (180, 180, 180),
    "Thruster Scout I": (160, 160, 160),
    "Galactic Navigator III": (150, 200, 255),
    "Galactic Navigator II": (130, 180, 240),
    "Galactic Navigator I": (110, 160, 220),
    "Cosmic Sharpshooter III": (255, 200, 150),
    "Cosmic Sharpshooter II": (240, 180, 130),
    "Cosmic Sharpshooter I": (220, 160, 110),
    "Void Veteran": (200, 100, 255),
    "Alien Slayer": (180, 90, 240),
    "Supernova General": (255, 50, 50),
    "Black Hole Conqueror": (100, 50, 150),
    "Quantum Warlord": (50, 255, 50),
    "Universe Breaker": (255, 215, 0),
}

# Rank Names
RANK_MMRS = [
    "Thruster Scout III",
    "Thruster Scout II",
    "Thruster Scout I",
    "Galactic Navigator III",
    "Galactic Navigator II",
    "Galactic Navigator I",
    "Cosmic Sharpshooter III",
    "Cosmic Sharpshooter II",
    "Cosmic Sharpshooter I",
    "Void Veteran",
    "Alien Slayer",
    "Supernova General",
    "Black Hole Conqueror",
    "Quantum Warlord",
    "Universe Breaker",
]

# Buttons for Main
buttons = [
    {"label": "Message Section", "rect": pygame.Rect(int(SCREEN_WIDTH * 1 / 21), int(SCREEN_HEIGHT * 0.9), 150, 40)},
    {"label": "Game Section", "rect": pygame.Rect(int(SCREEN_WIDTH * 6 / 21), int(SCREEN_HEIGHT * 0.9), 150, 40)},
    {"label": "Settings Section", "rect": pygame.Rect(int(SCREEN_WIDTH * 11 / 21), int(SCREEN_HEIGHT * 0.9), 150, 40)},
    {"label": "View Ranks", "rect": pygame.Rect(int(SCREEN_WIDTH * 0.8), int(SCREEN_HEIGHT * 0.1), 120, 30)},
    {"label": "Friend Section", "rect": pygame.Rect(int(SCREEN_WIDTH  * 16 / 21), int(SCREEN_HEIGHT * 0.9), 150, 40)},  
]

class client:
    def __init__(self, name, password):
        now = datetime.now()
        self.name = name
        self.password = password
        self.account_created =  now.strftime("%m/%d/%Y, %H:%M:%S")
        self.mmr = 800
        rnk = (self.mmr - 1000) // 500 if (self.mmr - 1000) // 500 >= 0 else 0
        self.rank = RANK_MMRS[rnk]
        self.max_Score = 0.0
        self.friends = []

    def change_Name(self, newName):
        self.name = newName

    def change_Pass(self, newpass):
        self.password = newpass

    # Friend Section
    def search_Friend(self, friend_client):
        for friend in range (self.friends):
            if (friend_client.name == friend.name):
                return True
        return False

    def add_Friend(self, friend_client):
        self.friends.append(friend_client)
        # if self.search_Friend(friend_client):
        #     return # Friend Already in List
        # self.friends.append(friend_client)

    def remove_Friend(self, friend_client):
        self.friends.remove(friend_client)
        # for friend in range (self.friends):
        #     if (friend_client.name == friend.name):
        #         self.friends.remove(friend_client)

    def update_max_score(self, new_max_score):
        self.max_Score = max(new_max_score, self.max_Score)
        self.mmr = new_max_score * 0.001819
        rnk = (self.mmr - 1000) // 500 if (self.mmr - 1000) // 500 >= 0 else 0
        self.rank = RANK_MMRS[rnk]


# Draw text utility
def draw_text(screen, text, font, color, x, y, align="topleft"):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    setattr(rect, align, (x, y))
    screen.blit(surface, rect)