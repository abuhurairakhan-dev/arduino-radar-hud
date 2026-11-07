import math
import time
from typing import List, Tuple, Dict, Optional, Callable
import pygame
from .theme import ThemeColors, FontManager
from .radar_display import TrackedTarget

class HUDButton:
    """A sci-fi interactive button with hover states and active indicators."""
    def __init__(self, rect: pygame.Rect, text: str, action_code: str, shortcut: str = ""):
        self.rect = rect
        self.text = text
        self.action_code = action_code
        self.shortcut = shortcut
        self.is_hovered = False
        self.is_active = False

    def check_hover(self, mouse_pos: Tuple[int, int]) -> bool:
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def render(self, screen: pygame.Surface, theme: ThemeColors, fonts: FontManager):
        border_col = theme.accent if self.is_hovered else (theme.primary if self.is_active else theme.panel_border)
        bg_col = theme.primary_dim if self.is_hovered else theme.panel_bg

        # Button background and border
        pygame.draw.rect(screen, bg_col, self.rect)
        pygame.draw.rect(screen, border_col, self.rect, 1)

        # Tech corner accents
        x, y, w, h = self.rect
        pygame.draw.line(screen, border_col, (x, y), (x + 4, y), 2)
        pygame.draw.line(screen, border_col, (x, y), (x, y + 4), 2)
        pygame.draw.line(screen, border_col, (x + w - 4, y + h), (x + w, y + h), 2)
        pygame.draw.line(screen, border_col, (x + w, y + h - 4), (x + w, y + h), 2)

        # Button text
        label = f"{self.shortcut} {self.text}" if self.shortcut else self.text
        text_col = theme.text_bright if self.is_hovered else theme.text_dim
        txt_surf = fonts.small_font.render(label, True, text_col)
        screen.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))

class HUDPanels:
    """Renders the comprehensive sci-fi movie HUD: Telemetry, Oscilloscope, Threat Matrix, and Controls."""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.distance_history: List[float] = [0.0] * 60
        self.buttons: List[HUDButton] = []
        self._init_buttons()

        # Pre-rendered scanline surface for CRT movie effect
        self.scanlines = pygame.Surface((width, height), pygame.SRCALPHA)
        for y in range(0, height, 4):
            pygame.draw.line(self.scanlines, (0, 0, 0, 45), (0, y), (width, y), 1)

    def _init_buttons(self):
        btn_y = self.height - 48
        btn_w = 135
        btn_h = 32
        gap = 10
        start_x = 20

        specs = [
            ("MODE", "mode", "[M]"),
            ("THEME", "theme", "[C]"),
            ("AUDIO", "audio", "[S]"),
            ("ALERT 30cm", "alert", "[A]"),
            ("SPAWN TGT", "spawn", "[D]"),
            ("FREEZE", "pause", "[P]"),
            ("CLEAR", "clear", "[R]"),
        ]

        self.buttons = []
        for i, (text, code, key) in enumerate(specs):
            rect = pygame.Rect(start_x + i * (btn_w + gap), btn_y, btn_w, btn_h)
            self.buttons.append(HUDButton(rect, text, code, key))

    def update_history(self, distance_cm: float):
        if distance_cm > 0.0:
            self.distance_history.append(min(50.0, distance_cm))
        else:
            self.distance_history.append(50.0)
        if len(self.distance_history) > 60:
            self.distance_history.pop(0)

    def handle_mouse_click(self, pos: Tuple[int, int]) -> Optional[str]:
        for btn in self.buttons:
            if btn.rect.collidepoint(pos):
                return btn.action_code
        return None

    def handle_mouse_motion(self, pos: Tuple[int, int]):
        for btn in self.buttons:
            btn.check_hover(pos)

    def render(
        self,
        screen: pygame.Surface,
        theme: ThemeColors,
        fonts: FontManager,
        current_angle: int,
        current_dist: float,
        is_valid: bool,
        is_alert: bool,
        alert_threshold_cm: float,
        is_sim_mode: bool,
        conn_status: str,
        audio_enabled: bool,
        is_paused: bool,
        fps: float,
        tracked_targets: List[TrackedTarget],
        show_scanlines: bool = True
    ):
        # 1. Header Bar
        self._render_header(screen, theme, fonts, is_sim_mode, conn_status, audio_enabled, is_paused, fps)

        # 2. Left Panel: Telemetry & Threat Matrix
        self._render_left_panel(screen, theme, fonts, current_angle, current_dist, is_valid, is_alert, alert_threshold_cm, tracked_targets)

        # 3. Right Panel: Oscilloscope & Waterfall History
        self._render_right_panel(screen, theme, fonts, current_dist, alert_threshold_cm)

        # 4. Bottom Control Dock
        self._render_dock(screen, theme, fonts, audio_enabled, is_paused, alert_threshold_cm)

        # 5. Full-screen CRT scanline overlay
        if show_scanlines:
            screen.blit(self.scanlines, (0, 0))

    def _render_panel_box(self, screen: pygame.Surface, rect: pygame.Rect, theme: ThemeColors, title: str, fonts: FontManager):
        """Draws a sci-fi panel box with chamfered style and glowing header."""
        pygame.draw.rect(screen, theme.panel_bg, rect)
        pygame.draw.rect(screen, theme.panel_border, rect, 1)

        # Glowing corner tick marks
        x, y, w, h = rect
        pygame.draw.line(screen, theme.primary, (x, y), (x + 8, y), 2)
        pygame.draw.line(screen, theme.primary, (x, y), (x, y + 8), 2)
        pygame.draw.line(screen, theme.primary, (x + w - 8, y), (x + w, y), 2)
        pygame.draw.line(screen, theme.primary, (x + w, y), (x + w, y + 8), 2)

        # Title bar banner
        if title:
            pygame.draw.rect(screen, theme.primary_dim, (x, y, w, 20))
            t_surf = fonts.subtitle_font.render(f"// {title}", True, theme.text_bright)
            screen.blit(t_surf, (x + 8, y + 3))

    def _render_header(self, screen: pygame.Surface, theme: ThemeColors, fonts: FontManager, is_sim_mode: bool, conn_status: str, audio: bool, paused: bool, fps: float):
        rect = pygame.Rect(10, 10, self.width - 20, 42)
        self._render_panel_box(screen, rect, theme, "", fonts)

        # Main Title
        title_surf = fonts.title_font.render("NEXUS-7 ULTRASONIC TACTICAL RADAR", True, theme.primary)
        screen.blit(title_surf, (24, 18))

        sub_surf = fonts.micro_font.render("SYSTEM VERSION 2.0 // HC-SR04 ACOUSTIC SENSOR // 40kHz PULSE", True, theme.text_dim)
        screen.blit(sub_surf, (24, 38))

        # Status Badges on Top Right
        now_str = time.strftime("%H:%M:%S") + f".{int(time.time()*10)%10}"
        badge_x = self.width - 480

        # Mode Badge
        mode_txt = "SIMULATION" if is_sim_mode else f"LIVE: {conn_status}"
        mode_col = theme.accent if is_sim_mode else (theme.target_normal if "CONNECTED" in conn_status else theme.target_alert)
        m_surf = fonts.small_font.render(f"[{mode_txt}]", True, mode_col)
        screen.blit(m_surf, (badge_x, 22))

        # Audio Badge
        sfx_txt = "SFX: ON" if audio else "SFX: MUTED"
        sfx_col = theme.text_bright if audio else theme.text_dim
        a_surf = fonts.small_font.render(f"[{sfx_txt}]", True, sfx_col)
        screen.blit(a_surf, (badge_x + 160, 22))

        # Pause Badge
        if paused:
            p_surf = fonts.small_font.render("[FROZEN]", True, theme.text_alert)
            screen.blit(p_surf, (badge_x + 250, 22))

        # Clock & FPS
        clk_surf = fonts.small_font.render(f"UTC {now_str} | {fps:.0f} FPS", True, theme.text_bright)
        screen.blit(clk_surf, (badge_x + 325, 22))

    def _render_left_panel(self, screen: pygame.Surface, theme: ThemeColors, fonts: FontManager, angle: int, dist: float, is_valid: bool, is_alert: bool, alert_dist: float, targets: List[TrackedTarget]):
        p_rect = pygame.Rect(10, 60, 280, self.height - 118)
        self._render_panel_box(screen, p_rect, theme, "TELEMETRY & THREAT MATRIX", fonts)

        # 1. Bearing Compass Dial
        cx = 75
        cy = 135
        cr = 40
        pygame.draw.circle(screen, theme.panel_bg, (cx, cy), cr)
        pygame.draw.circle(screen, theme.grid, (cx, cy), cr, 1)

        # Compass tick marks
        for a in range(0, 360, 45):
            rad = math.radians(a)
            x1 = cx + math.cos(rad) * (cr - 4)
            y1 = cy - math.sin(rad) * (cr - 4)
            x2 = cx + math.cos(rad) * cr
            y2 = cy - math.sin(rad) * cr
            pygame.draw.line(screen, theme.grid, (x1, y1), (x2, y2), 1)

        # Active angle needle
        rad_curr = math.radians(angle)
        nx = cx - math.cos(rad_curr) * (cr - 6)
        ny = cy - math.sin(rad_curr) * (cr - 6)
        pygame.draw.line(screen, theme.primary, (cx, cy), (nx, ny), 2)
        pygame.draw.circle(screen, theme.primary, (cx, cy), 3)

        # Bearing readout
        screen.blit(fonts.subtitle_font.render("BEARING", True, theme.text_dim), (135, 105))
        screen.blit(fonts.hud_large.render(f"{angle:03d}°", True, theme.primary), (135, 122))
        screen.blit(fonts.micro_font.render(f"SERVO SECTOR: 15°-165°", True, theme.text_dim), (135, 155))

        # 2. Distance Readout Display
        dist_box = pygame.Rect(20, 190, 260, 75)
        pygame.draw.rect(screen, (0, 0, 0, 70), dist_box)
        pygame.draw.rect(screen, theme.panel_border, dist_box, 1)

        screen.blit(fonts.small_font.render("CURRENT SENSOR RANGE", True, theme.text_dim), (28, 196))
        if is_valid and dist > 0:
            dist_str = f"{dist:.1f} CM"
            inch_str = f"({dist * 0.3937:.1f} IN)"
            screen.blit(fonts.hud_giant.render(dist_str, True, theme.target_alert if is_alert else theme.text_bright), (28, 214))
            screen.blit(fonts.small_font.render(inch_str, True, theme.text_dim), (180, 230))
        else:
            screen.blit(fonts.hud_giant.render("--.- CM", True, theme.text_dim), (28, 214))
            screen.blit(fonts.small_font.render("NO ECHO DETECTED", True, theme.text_dim), (28, 252))

        # 3. Threat Assessment Box
        threat_y = 278
        screen.blit(fonts.subtitle_font.render("DEFCON THREAT LEVEL", True, theme.text_bright), (20, threat_y))

        # DEFCON Gauge Bar
        num_bars = 4
        bar_w = 58
        bar_h = 16
        threat_level = 3 if is_alert else (2 if (is_valid and dist < alert_dist + 10.0) else (1 if is_valid else 0))

        for b in range(num_bars):
            bx = 20 + b * (bar_w + 8)
            rect_b = pygame.Rect(bx, threat_y + 22, bar_w, bar_h)
            if b <= threat_level:
                col = theme.target_alert if b >= 3 else (theme.accent if b == 2 else theme.primary)
                pygame.draw.rect(screen, col, rect_b)
            else:
                pygame.draw.rect(screen, theme.grid, rect_b, 1)

        threat_names = ["DEFCON 4: CLEAR", "DEFCON 3: TRACKING", "DEFCON 2: ELEVATED", "DEFCON 1: INTRUSION"]
        screen.blit(fonts.small_font.render(threat_names[threat_level], True, theme.target_alert if is_alert else theme.text_bright), (20, threat_y + 44))

        # 4. Proximity Alert Banner (Flashing when alert is active)
        if is_alert:
            pulse = math.sin(time.time() * 10.0) > 0.0
            alert_bg = theme.target_alert if pulse else (80, 10, 20)
            alert_box = pygame.Rect(20, 350, 260, 48)
            pygame.draw.rect(screen, alert_bg, alert_box)
            pygame.draw.rect(screen, (255, 255, 255), alert_box, 2)
            al1 = fonts.subtitle_font.render(">> PROXIMITY ALERT <<", True, (255, 255, 255))
            al2 = fonts.micro_font.render(f"BREACH AT {dist:.1f}cm (LIMIT {alert_dist:.0f}cm)", True, (255, 240, 240))
            screen.blit(al1, al1.get_rect(center=(alert_box.centerx, alert_box.y + 16)))
            screen.blit(al2, al2.get_rect(center=(alert_box.centerx, alert_box.y + 34)))
        else:
            alert_box = pygame.Rect(20, 350, 260, 48)
            pygame.draw.rect(screen, (10, 25, 20), alert_box)
            pygame.draw.rect(screen, theme.grid, alert_box, 1)
            screen.blit(fonts.small_font.render("PERIMETER SECURE", True, theme.text_dim), (alert_box.x + 14, alert_box.y + 14))

        # 5. Tracked Targets Table
        tbl_y = 412
        screen.blit(fonts.subtitle_font.render(f"LOCKED TARGETS ({len(targets)})", True, theme.text_bright), (20, tbl_y))

        header_str = "ID       RANGE    BEARING  STATUS"
        screen.blit(fonts.micro_font.render(header_str, True, theme.text_dim), (20, tbl_y + 20))
        pygame.draw.line(screen, theme.grid, (20, tbl_y + 32), (280, tbl_y + 32), 1)

        row_y = tbl_y + 38
        if targets:
            for tgt in targets[:5]:
                col = theme.target_alert if tgt.is_alert else theme.text_bright
                status = "HOSTILE" if tgt.is_alert else "TRACKED"
                row_str = f"{tgt.target_id:<7} {tgt.distance_cm:4.1f}cm   {int(tgt.angle_deg):03d}°    {status}"
                screen.blit(fonts.micro_font.render(row_str, True, col), (20, row_y))
                row_y += 16
        else:
            screen.blit(fonts.micro_font.render("NO TARGET SIGNATURES DETECTED", True, theme.text_dim), (20, row_y))

    def _render_right_panel(self, screen: pygame.Surface, theme: ThemeColors, fonts: FontManager, current_dist: float, alert_dist: float):
        p_rect = pygame.Rect(self.width - 290, 60, 280, self.height - 118)
        self._render_panel_box(screen, p_rect, theme, "SIGNAL & OSCILLOSCOPE", fonts)

        # 1. Live Ultrasonic Waveform Oscilloscope
        rx = self.width - 280
        ry = 95
        rw = 260
        rh = 100

        pygame.draw.rect(screen, (0, 0, 0, 90), (rx, ry, rw, rh))
        pygame.draw.rect(screen, theme.panel_border, (rx, ry, rw, rh), 1)
        screen.blit(fonts.micro_font.render("ACOUSTIC CHIRP & ECHO ENVELOPE (40 kHz)", True, theme.text_dim), (rx + 6, ry + 5))

        # Center zero line
        mid_y = ry + rh // 2
        pygame.draw.line(screen, theme.grid, (rx, mid_y), (rx + rw, mid_y), 1)

        # Synthesize oscilloscope waveform showing trigger burst and return echo
        pts = []
        now = time.time()
        echo_x = int(rx + min(rw - 20, max(25, (current_dist / 50.0) * rw)))

        for i in range(rw):
            x = rx + i
            # Initial transmit pulse at x near rx
            if i < 25:
                amp = math.sin((i * 1.5) + now * 25.0) * (20 * math.exp(-i / 8.0))
            # Echo return burst around echo_x
            elif abs(i - echo_x) < 20 and current_dist > 0:
                dist_from_echo = abs(i - echo_x)
                amp = math.sin((i * 1.8) + now * 30.0) * (26 * math.exp(-dist_from_echo / 6.0))
            else:
                # Ambient acoustic noise floor
                amp = math.sin(i * 0.4 + now * 10.0) * 2.0

            y = mid_y + int(amp)
            pts.append((x, y))

        if len(pts) > 1:
            pygame.draw.lines(screen, theme.primary, False, pts, 1)

        # 2. Distance Waterfall History Graph
        gy = 215
        gh = 110
        pygame.draw.rect(screen, (0, 0, 0, 90), (rx, gy, rw, gh))
        pygame.draw.rect(screen, theme.panel_border, (rx, gy, rw, gh), 1)
        screen.blit(fonts.micro_font.render("RANGE TIME-SERIES (LAST 60 SWEEPS)", True, theme.text_dim), (rx + 6, gy + 5))

        # Draw alert threshold line on graph
        alert_y = gy + gh - int((alert_dist / 50.0) * gh)
        pygame.draw.line(screen, theme.alert_ring, (rx, alert_y), (rx + rw, alert_y), 1)
        screen.blit(fonts.micro_font.render(f"ALERT {int(alert_dist)}cm", True, theme.text_alert), (rx + rw - 65, alert_y - 12))

        # Plot historical points
        hist_pts = []
        step_x = rw / max(1, len(self.distance_history) - 1)
        for idx, val in enumerate(self.distance_history):
            px = int(rx + idx * step_x)
            py = int(gy + gh - (val / 50.0) * (gh - 14) - 7)
            hist_pts.append((px, py))

        if len(hist_pts) > 1:
            pygame.draw.lines(screen, theme.accent, False, hist_pts, 2)

        # 3. Hardware & Environmental Specs Card
        sy = 345
        screen.blit(fonts.subtitle_font.render("TACTICAL SPECIFICATIONS", True, theme.text_bright), (rx, sy))

        specs_info = [
            ("SENSOR", "HC-SR04 ULTRASONIC"),
            ("SONIC VELOCITY", "343.2 M/S (@ 20°C)"),
            ("SOUND FREQUENCY", "40.0 kHz BURST"),
            ("DETECTION CONE", "~15 DEGREES"),
            ("SERVO ACTUATOR", "SG90 MICRO SERVO"),
            ("SWEEP STEP", "1 DEGREE / 70ms"),
            ("MAX RADAR RANGE", "50.0 CENTIMETERS"),
            ("ALERT BOUNDARY", f"{alert_dist:.1f} CENTIMETERS"),
        ]

        card_y = sy + 22
        for title, val in specs_info:
            screen.blit(fonts.micro_font.render(title, True, theme.text_dim), (rx, card_y))
            screen.blit(fonts.micro_font.render(val, True, theme.text_bright), (rx + 115, card_y))
            card_y += 18

    def _render_dock(self, screen: pygame.Surface, theme: ThemeColors, fonts: FontManager, audio: bool, paused: bool, alert_dist: float):
        # Update button text/active status dynamically
        for btn in self.buttons:
            if btn.action_code == "audio":
                btn.text = "SFX: ON" if audio else "SFX: OFF"
                btn.is_active = audio
            elif btn.action_code == "pause":
                btn.text = "RESUME" if paused else "FREEZE"
                btn.is_active = paused
            elif btn.action_code == "alert":
                btn.text = f"ALERT {int(alert_dist)}cm"
                btn.is_active = True

            btn.render(screen, theme, fonts)

