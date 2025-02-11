import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (19, 26, 30)

# White Text
TEXT_COLOR_WHITE = (255, 255, 255)
TEXT_COLOR_BLACK = (255, 255, 255)

# Blue Buttons
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)

# Red buttons
BUTTON_COLOR_RED = (139, 0, 0)
BUTTON_HOVER_COLOR_RED = (255, 127, 127)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

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
RANK_NAMES = [
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

# Draw text utility
def draw_text(screen, text, font, color, x, y, align="topleft"):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    setattr(rect, align, (x, y))
    screen.blit(surface, rect)
