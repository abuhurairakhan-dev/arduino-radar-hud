import pygame
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class ThemeColors:
    name: str
    code: str
    bg: Tuple[int, int, int]
    panel_bg: Tuple[int, int, int]
    panel_border: Tuple[int, int, int]
    primary: Tuple[int, int, int]
    primary_dim: Tuple[int, int, int]
    primary_glow: Tuple[int, int, int]
    secondary: Tuple[int, int, int]
    accent: Tuple[int, int, int]
    target_normal: Tuple[int, int, int]
    target_alert: Tuple[int, int, int]
    target_glow: Tuple[int, int, int]
    grid: Tuple[int, int, int]
    alert_ring: Tuple[int, int, int]
    text_bright: Tuple[int, int, int]
    text_dim: Tuple[int, int, int]
    text_alert: Tuple[int, int, int]
    scanline: Tuple[int, int, int, int]

THEMES: List[ThemeColors] = [
    ThemeColors(
        name="CYAN ASTRAL (TRON / JARVIS)",
        code="CYAN",
        bg=(6, 12, 22),
        panel_bg=(10, 20, 35),
        panel_border=(0, 180, 240),
        primary=(0, 240, 255),
        primary_dim=(0, 85, 110),
        primary_glow=(0, 150, 255),
        secondary=(0, 160, 255),
        accent=(0, 255, 170),
        target_normal=(0, 255, 200),
        target_alert=(255, 45, 85),
        target_glow=(255, 90, 120),
        grid=(0, 150, 200),
        alert_ring=(255, 50, 90),
        text_bright=(220, 245, 255),
        text_dim=(80, 140, 170),
        text_alert=(255, 70, 100),
        scanline=(0, 240, 255, 12)
    ),
    ThemeColors(
        name="TACTICAL EMERALD (PREDATOR / WAR ROOM)",
        code="EMERALD",
        bg=(4, 18, 10),
        panel_bg=(8, 30, 18),
        panel_border=(0, 200, 90),
        primary=(0, 255, 110),
        primary_dim=(0, 85, 40),
        primary_glow=(20, 180, 70),
        secondary=(50, 210, 90),
        accent=(160, 255, 60),
        target_normal=(120, 255, 70),
        target_alert=(255, 50, 50),
        target_glow=(255, 100, 80),
        grid=(0, 160, 80),
        alert_ring=(255, 70, 70),
        text_bright=(210, 255, 220),
        text_dim=(70, 150, 100),
        text_alert=(255, 80, 80),
        scanline=(0, 255, 100, 12)
    ),
    ThemeColors(
        name="SOLARIS AMBER (WEYLAND-YUTANI / CRT)",
        code="AMBER",
        bg=(20, 12, 4),
        panel_bg=(32, 20, 8),
        panel_border=(255, 160, 20),
        primary=(255, 175, 0),
        primary_dim=(100, 68, 0),
        primary_glow=(220, 130, 0),
        secondary=(255, 205, 60),
        accent=(255, 230, 110),
        target_normal=(255, 210, 70),
        target_alert=(255, 40, 40),
        target_glow=(255, 110, 60),
        grid=(180, 120, 15),
        alert_ring=(255, 60, 40),
        text_bright=(255, 235, 190),
        text_dim=(160, 120, 70),
        text_alert=(255, 80, 60),
        scanline=(255, 180, 0, 12)
    ),
    ThemeColors(
        name="CRIMSON RED ALERT (DEFCON 1)",
        code="RED",
        bg=(22, 6, 8),
        panel_bg=(36, 10, 14),
        panel_border=(255, 50, 70),
        primary=(255, 55, 75),
        primary_dim=(110, 20, 30),
        primary_glow=(220, 30, 50),
        secondary=(255, 110, 130),
        accent=(255, 200, 90),
        target_normal=(255, 190, 80),
        target_alert=(255, 255, 255),
        target_glow=(255, 140, 150),
        grid=(180, 35, 50),
        alert_ring=(255, 255, 255),
        text_bright=(255, 215, 220),
        text_dim=(160, 80, 90),
        text_alert=(255, 240, 100),
        scanline=(255, 60, 80, 12)
    ),
]

class FontManager:
    """Manages tech / futuristic fonts with graceful fallbacks."""
    def __init__(self):
        pygame.font.init()
        # Candidate fonts that look high-tech / monospace / military HUD
        candidates = ["consolas", "lucidaconsole", "dejavusansmono", "couriernew", "courier", "arial"]
        found_font = None
        for cand in candidates:
            if cand in pygame.font.get_fonts():
                found_font = cand
                break
        
        self.font_family = found_font
        self.title_font = pygame.font.SysFont(found_font, 20, bold=True)
        self.subtitle_font = pygame.font.SysFont(found_font, 14, bold=True)
        self.hud_large = pygame.font.SysFont(found_font, 28, bold=True)
        self.hud_giant = pygame.font.SysFont(found_font, 40, bold=True)
        self.normal_font = pygame.font.SysFont(found_font, 13, bold=False)
        self.small_font = pygame.font.SysFont(found_font, 11, bold=False)
        self.micro_font = pygame.font.SysFont(found_font, 9, bold=False)

