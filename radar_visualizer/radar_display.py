import math
import time
import random
from typing import List, Tuple, Dict, Optional
import pygame
from .theme import ThemeColors, FontManager

class RadarEcho:
    """Represents a single echo detection on the radar grid."""
    def __init__(self, angle_deg: int, distance_cm: float, timestamp: float, is_alert: bool):
        self.angle_deg = angle_deg
        self.distance_cm = distance_cm
        self.timestamp = timestamp
        self.is_alert = is_alert
        self.initial_age = 0.0

class TrackedTarget:
    """Clustered target object with bounding box and HUD tracking reticle."""
    def __init__(self, target_id: str, x: float, y: float, distance_cm: float, angle_deg: float, is_alert: bool):
        self.target_id = target_id
        self.x = x
        self.y = y
        self.distance_cm = distance_cm
        self.angle_deg = angle_deg
        self.is_alert = is_alert
        self.last_seen = time.time()
        self.lock_level = 1.0 # 0.0 to 1.0

class RadarDisplay:
    """Renders the sci-fi polar ultrasonic radar screen with phosphor trail and HUD reticles."""
    def __init__(self, center_x: int, center_y: int, radius: int, max_range_cm: float = 50.0):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.max_range_cm = max_range_cm
        self.current_angle = 90.0
        self.sweep_direction = 1

        self.echoes: List[RadarEcho] = []
        self.tracked_targets: List[TrackedTarget] = []
        self.particles: List[Dict] = []
        self.persistence_sec = 3.5

        # Pre-allocated surfaces for high-performance alpha blending
        self.surf_trail = pygame.Surface((self.radius * 2 + 100, self.radius * 2 + 100), pygame.SRCALPHA)
        self.surf_blips = pygame.Surface((self.radius * 2 + 100, self.radius * 2 + 100), pygame.SRCALPHA)

    def set_center_and_radius(self, cx: int, cy: int, r: int):
        self.center_x = cx
        self.center_y = cy
        self.radius = r
        self.surf_trail = pygame.Surface((self.radius * 2 + 100, self.radius * 2 + 100), pygame.SRCALPHA)
        self.surf_blips = pygame.Surface((self.radius * 2 + 100, self.radius * 2 + 100), pygame.SRCALPHA)

    def add_echo(self, angle_deg: int, distance_cm: float, alert_threshold_cm: float):
        """Adds or updates an echo measurement from ultrasonic sensor."""
        now = time.time()
        self.current_angle = float(angle_deg)

        if distance_cm > 0.0 and distance_cm <= self.max_range_cm:
            is_alert = (distance_cm <= alert_threshold_cm)
            # Replace existing echo at this angle or add new
            self.echoes = [e for e in self.echoes if abs(e.angle_deg - angle_deg) > 1 or (now - e.timestamp) > 0.2]
            self.echoes.append(RadarEcho(angle_deg, distance_cm, now, is_alert))

            # Emit ionizing radar particles at detection point
            rad = math.radians(angle_deg)
            dist_px = (distance_cm / self.max_range_cm) * self.radius
            px = self.center_x - math.cos(rad) * dist_px
            py = self.center_y - math.sin(rad) * dist_px
            for _ in range(3):
                self.particles.append({
                    "x": px,
                    "y": py,
                    "vx": random.uniform(-15, 15),
                    "vy": random.uniform(-15, 15),
                    "life": 0.6,
                    "max_life": 0.6,
                    "is_alert": is_alert
                })

        # Remove echoes older than persistence window
        self.echoes = [e for e in self.echoes if (now - e.timestamp) < self.persistence_sec]
        self._cluster_targets(alert_threshold_cm)

    def clear(self):
        self.echoes.clear()
        self.tracked_targets.clear()
        self.particles.clear()

    def _cluster_targets(self, alert_threshold_cm: float):
        """Groups nearby echo points into distinct tracked targets."""
        now = time.time()
        if not self.echoes:
            self.tracked_targets.clear()
            return

        sorted_echoes = sorted(self.echoes, key=lambda e: e.angle_deg)
        clusters: List[List[RadarEcho]] = []
        current_cluster: List[RadarEcho] = [sorted_echoes[0]]

        for i in range(1, len(sorted_echoes)):
            prev = current_cluster[-1]
            curr = sorted_echoes[i]
            # If within 7 degrees and 5 cm, group together
            if abs(curr.angle_deg - prev.angle_deg) <= 7 and abs(curr.distance_cm - prev.distance_cm) <= 6.0:
                current_cluster.append(curr)
            else:
                clusters.append(current_cluster)
                current_cluster = [curr]
        if current_cluster:
            clusters.append(current_cluster)

        new_targets: List[TrackedTarget] = []
        for idx, cluster in enumerate(clusters):
            avg_ang = sum(e.angle_deg for e in cluster) / len(cluster)
            avg_dist = sum(e.distance_cm for e in cluster) / len(cluster)
            is_alert = any(e.distance_cm <= alert_threshold_cm for e in cluster)

            rad = math.radians(avg_ang)
            dist_px = (avg_dist / self.max_range_cm) * self.radius
            tx = self.center_x - math.cos(rad) * dist_px
            ty = self.center_y - math.sin(rad) * dist_px

            target_id = f"TGT-{chr(65 + (idx % 26))}{idx + 1:02d}"
            new_targets.append(TrackedTarget(target_id, tx, ty, avg_dist, avg_ang, is_alert))

        self.tracked_targets = new_targets

    def update_particles(self, dt: float):
        for p in self.particles:
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["life"] -= dt
        self.particles = [p for p in self.particles if p["life"] > 0]

    def render(self, screen: pygame.Surface, theme: ThemeColors, fonts: FontManager, alert_dist_cm: float):
        """Main render method for the polar radar grid, sweep beam, and targets."""
        cx = self.center_x
        cy = self.center_y
        r = self.radius

        # 1. Draw Polar Grid Background & Range Rings
        self._render_grid(screen, theme, fonts, alert_dist_cm)

        # 2. Draw Phosphor Persistence Fan / Trail
        self._render_sweep_trail(screen, theme)

        # 3. Draw Range Blips and Target Signatures
        self._render_blips(screen, theme, fonts, alert_dist_cm)

        # 4. Draw Sci-Fi Tracking Reticles & Locks
        self._render_reticles(screen, theme, fonts)

        # 5. Draw Sweeping Beam & Ion Particles
        self._render_beam(screen, theme)

    def _render_grid(self, screen: pygame.Surface, theme: ThemeColors, fonts: FontManager, alert_dist_cm: float):
        cx, cy, r = self.center_x, self.center_y, self.radius

        # Outer bounding semicircle frame (15° to 165°)
        # Draw concentric range circles (every 10 cm up to 50 cm)
        num_rings = 5
        for i in range(1, num_rings + 1):
            ring_cm = (self.max_range_cm / num_rings) * i
            ring_r = int((i / num_rings) * r)
            rect = pygame.Rect(cx - ring_r, cy - ring_r, ring_r * 2, ring_r * 2)

            # Check if this ring is near the alert perimeter
            is_alert_zone = abs(ring_cm - alert_dist_cm) < 1.0

            if is_alert_zone:
                # Pulsing alert boundary
                pulse = (math.sin(time.time() * 6.0) + 1.0) * 0.5
                ring_color = [
                    int(theme.alert_ring[0] * (0.6 + 0.4 * pulse)),
                    int(theme.alert_ring[1] * (0.6 + 0.4 * pulse)),
                    int(theme.alert_ring[2] * (0.6 + 0.4 * pulse))
                ]
                pygame.draw.arc(screen, ring_color, rect, math.radians(15), math.radians(165), 2)

                # Alert perimeter tag
                lbl = fonts.micro_font.render(f"PERIMETER {int(ring_cm)}cm [ALERT]", True, theme.text_alert)
                screen.blit(lbl, (cx - 70, cy - ring_r - 12))
            else:
                # Standard range arc
                pygame.draw.arc(screen, theme.grid, rect, math.radians(15), math.radians(165), 1)
                lbl = fonts.micro_font.render(f"{int(ring_cm)}cm", True, theme.text_dim)
                screen.blit(lbl, (cx + 6, cy - ring_r + 2))

        # Radial angle spokes (every 15° from 15° to 165°)
        for deg in range(15, 166, 15):
            rad = math.radians(deg)
            x_end = cx - math.cos(rad) * r
            y_end = cy - math.sin(rad) * r

            # Key cardinal axes are drawn brighter
            is_cardinal = (deg in (30, 60, 90, 120, 150))
            color = theme.primary_dim if is_cardinal else theme.grid
            width = 1

            pygame.draw.line(screen, color, (cx, cy), (x_end, y_end), width)

            # Degree labels along circumference
            lbl_x = cx - math.cos(rad) * (r + 18)
            lbl_y = cy - math.sin(rad) * (r + 18)
            lbl_text = fonts.small_font.render(f"{deg}°", True, theme.primary if is_cardinal else theme.text_dim)
            screen.blit(lbl_text, lbl_text.get_rect(center=(lbl_x, lbl_y)))

        # Baseline horizontal limiter (15° to 165° outer boundary arc)
        outer_rect = pygame.Rect(cx - r, cy - r, r * 2, r * 2)
        pygame.draw.arc(screen, theme.primary, outer_rect, math.radians(15), math.radians(165), 2)

        # Center origin hub
        pygame.draw.circle(screen, theme.primary, (cx, cy), 6)
        pygame.draw.circle(screen, theme.bg, (cx, cy), 3)

    def _render_sweep_trail(self, screen: pygame.Surface, theme: ThemeColors):
        """Draws trailing phosphor persistence cone behind sweeping needle."""
        cx, cy, r = self.center_x, self.center_y, self.radius
        self.surf_trail.fill((0, 0, 0, 0))

        trail_span_deg = 20.0
        steps = 14
        step_deg = trail_span_deg / steps
        cur_ang = self.current_angle

        # Re-center coords for surf_trail
        scx = r + 50
        scy = r + 50

        for i in range(steps):
            # Sweep backwards based on current direction
            alpha = int(90 * (1.0 - (i / steps) ** 1.3))
            if alpha <= 0:
                continue

            ang1 = cur_ang - (i * step_deg * self.sweep_direction)
            ang2 = cur_ang - ((i + 1) * step_deg * self.sweep_direction)

            # Clamp angles to radar bounds
            if not (14 <= ang1 <= 166 and 14 <= ang2 <= 166):
                continue

            r1 = math.radians(ang1)
            r2 = math.radians(ang2)

            p0 = (scx, scy)
            p1 = (scx - math.cos(r1) * r, scy - math.sin(r1) * r)
            p2 = (scx - math.cos(r2) * r, scy - math.sin(r2) * r)

            poly_color = (*theme.primary_glow[:3], alpha)
            pygame.draw.polygon(self.surf_trail, poly_color, [p0, p1, p2])

        screen.blit(self.surf_trail, (cx - scx, cy - scy))

    def _render_blips(self, screen: pygame.Surface, theme: ThemeColors, fonts: FontManager, alert_dist_cm: float):
        """Renders glowing echoes with decay."""
        cx, cy, r = self.center_x, self.center_y, self.radius
        now = time.time()

        for echo in self.echoes:
            age = now - echo.timestamp
            fade = max(0.0, 1.0 - (age / self.persistence_sec))
            if fade <= 0.01:
                continue

            rad = math.radians(echo.angle_deg)
            dist_px = (echo.distance_cm / self.max_range_cm) * r
            bx = cx - math.cos(rad) * dist_px
            by = cy - math.sin(rad) * dist_px

            color_base = theme.target_alert if echo.is_alert else theme.target_normal

            # Concentric expanding acoustic pulse ripple
            ripple_radius = 4 + int((1.0 - fade) * 16)
            ripple_alpha = int(fade * 140)
            ripple_surf = pygame.Surface((ripple_radius * 2 + 4, ripple_radius * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(
                ripple_surf,
                (*color_base, ripple_alpha),
                (ripple_radius + 2, ripple_radius + 2),
                ripple_radius,
                1
            )
            screen.blit(ripple_surf, (bx - ripple_radius - 2, by - ripple_radius - 2))

            # Core blip pip
            core_color = [int(c * fade) for c in color_base]
            pygame.draw.circle(screen, core_color, (int(bx), int(by)), 4)
            pygame.draw.circle(screen, (255, 255, 255), (int(bx), int(by)), 2)

    def _render_reticles(self, screen: pygame.Surface, theme: ThemeColors, fonts: FontManager):
        """Renders sci-fi corner brackets and tracking telemetry over clustered targets."""
        for target in self.tracked_targets:
            tx = int(target.x)
            ty = int(target.y)
            box_sz = 14

            col = theme.target_alert if target.is_alert else theme.primary
            pulse = math.sin(time.time() * 8.0) * 2.0 if target.is_alert else 0.0
            bs = int(box_sz + pulse)

            # Draw sci-fi corner tracking brackets [ ]
            # Top-Left
            pygame.draw.lines(screen, col, False, [(tx - bs, ty - bs + 6), (tx - bs, ty - bs), (tx - bs + 6, ty - bs)], 2)
            # Top-Right
            pygame.draw.lines(screen, col, False, [(tx + bs - 6, ty - bs), (tx + bs, ty - bs), (tx + bs, ty - bs + 6)], 2)
            # Bottom-Left
            pygame.draw.lines(screen, col, False, [(tx - bs, ty + bs - 6), (tx - bs, ty + bs), (tx - bs + 6, ty + bs)], 2)
            # Bottom-Right
            pygame.draw.lines(screen, col, False, [(tx + bs - 6, ty + bs), (tx + bs, ty + bs), (tx + bs, ty + bs - 6)], 2)

            # If alert target, draw pulsing warning vector line from center
            if target.is_alert:
                pygame.draw.line(screen, theme.target_alert, (self.center_x, self.center_y), (tx, ty), 1)

            # Target telemetry pill
            tag_text = f"{target.target_id} {target.distance_cm:.1f}cm {int(target.angle_deg)}°"
            lbl = fonts.micro_font.render(tag_text, True, theme.text_alert if target.is_alert else theme.text_bright)
            screen.blit(lbl, (tx + bs + 4, ty - 6))

    def _render_beam(self, screen: pygame.Surface, theme: ThemeColors):
        """Renders active radar sweep needle and particle spray."""
        cx, cy, r = self.center_x, self.center_y, self.radius
        rad = math.radians(self.current_angle)

        bx = cx - math.cos(rad) * r
        by = cy - math.sin(rad) * r

        # Main laser / sonar needle
        pygame.draw.line(screen, (255, 255, 255), (cx, cy), (bx, by), 2)
        pygame.draw.line(screen, theme.primary, (cx, cy), (bx, by), 1)

        # Tip flare
        pygame.draw.circle(screen, (255, 255, 255), (int(bx), int(by)), 4)
        pygame.draw.circle(screen, theme.primary, (int(bx), int(by)), 8, 1)

        # Ion particles
        for p in self.particles:
            alpha = int((p["life"] / p["max_life"]) * 220)
            col = theme.target_alert if p["is_alert"] else theme.primary
            p_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*col, alpha), (2, 2), 2)
            screen.blit(p_surf, (int(p["x"]) - 2, int(p["y"]) - 2))

