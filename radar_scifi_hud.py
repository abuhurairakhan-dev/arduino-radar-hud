#!/usr/bin/env python3
"""
NEXUS-7 Sci-Fi Ultrasonic Radar System - Real-time HUD Visualizer
Pairing Arduino Uno + SG90 Servo + HC-SR04 Ultrasonic Sensor with Pygame
"""

import sys
import os
import time
import math
import argparse
import pygame

from radar_visualizer.theme import THEMES, FontManager
from radar_visualizer.audio import SoundManager
from radar_visualizer.simulator import RadarSimulator
from radar_visualizer.serial_comm import SerialManager
from radar_visualizer.radar_display import RadarDisplay
from radar_visualizer.hud_panels import HUDPanels

def main():
    parser = argparse.ArgumentParser(description="Sci-Fi Ultrasonic Radar Visualizer")
    parser.add_argument("--port", type=str, default=None, help="Serial COM port (e.g. COM3 or /dev/ttyUSB0)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    parser.add_argument("--sim", action="store_true", help="Force Simulation Mode on startup")
    parser.add_argument("--theme", type=str, default="CYAN", choices=["CYAN", "EMERALD", "AMBER", "RED"], help="Initial color theme")
    parser.add_argument("--alert", type=float, default=30.0, help="Alert distance threshold in cm (default: 30.0)")
    args = parser.parse_args()

    pygame.init()
    pygame.display.set_caption("NEXUS-7 // TACTICAL ULTRASONIC RADAR HUD")

    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.RESIZABLE)
    clock = pygame.time.Clock()

    fonts = FontManager()
    sound_mgr = SoundManager()

    # Find theme
    theme_index = 0
    for idx, th in enumerate(THEMES):
        if th.code == args.theme:
            theme_index = idx
            break

    # Setup display components
    radar_cx = width // 2
    radar_cy = height - 100
    radar_r = 300
    radar = RadarDisplay(radar_cx, radar_cy, radar_r, max_range_cm=50.0)
    hud = HUDPanels(width, height)

    # Serial and Simulation managers
    serial_mgr = SerialManager(baud_rate=args.baud)
    simulator = RadarSimulator(min_angle=15, max_angle=165, step=1, interval_sec=0.035)

    is_sim_mode = args.sim
    if not is_sim_mode:
        connected = serial_mgr.connect(args.port)
        if not connected:
            print("[System] No active serial connection found. Automatically starting in SIMULATION MODE.")
            is_sim_mode = True

    alert_threshold_cm = args.alert
    is_paused = False
    show_scanlines = True
    is_fullscreen = False

    current_angle = 90
    current_dist = -1.0
    is_valid = False
    is_alert = False

    last_time = time.time()
    last_target_count = 0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        now = time.time()

        theme = THEMES[theme_index]

        # Process Pygame Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.RESIZABLE)
                radar_cx = width // 2
                radar_cy = height - 100
                radar_r = min(360, max(220, int(height * 0.44)))
                radar.set_center_and_radius(radar_cx, radar_cy, radar_r)
                hud = HUDPanels(width, height)

            elif event.type == pygame.MOUSEMOTION:
                hud.handle_mouse_motion(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    # Check HUD Buttons
                    action = hud.handle_mouse_click(event.pos)
                    if action:
                        sound_mgr.play_click()
                        if action == "mode":
                            is_sim_mode = not is_sim_mode
                            if not is_sim_mode:
                                serial_mgr.connect(args.port)
                            else:
                                serial_mgr.disconnect()
                        elif action == "theme":
                            theme_index = (theme_index + 1) % len(THEMES)
                        elif action == "audio":
                            sound_mgr.toggle()
                        elif action == "alert":
                            alert_threshold_cm = 20.0 if alert_threshold_cm == 40.0 else (alert_threshold_cm + 10.0)
                            if serial_mgr.is_connected:
                                serial_mgr.send_command(f"ALERT:{int(alert_threshold_cm)}")
                        elif action == "spawn":
                            simulator.spawn_alert_intruder()
                            sound_mgr.play_alarm()
                        elif action == "pause":
                            is_paused = not is_paused
                        elif action == "clear":
                            radar.clear()
                    else:
                        # Click on radar grid: Add custom target in simulation mode!
                        dx = radar.center_x - event.pos[0]
                        dy = radar.center_y - event.pos[1]
                        dist_px = math.hypot(dx, dy)
                        if dist_px <= radar.radius and dy > 0:
                            click_rad = math.atan2(dy, dx)
                            click_deg = math.degrees(click_rad)
                            if 15 <= click_deg <= 165:
                                click_dist = (dist_px / radar.radius) * radar.max_range_cm
                                simulator.add_user_target(click_deg, click_dist)
                                sound_mgr.play_lock()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False

                elif event.key == pygame.K_m:
                    sound_mgr.play_click()
                    is_sim_mode = not is_sim_mode
                    if not is_sim_mode:
                        serial_mgr.connect(args.port)
                    else:
                        serial_mgr.disconnect()

                elif event.key == pygame.K_c:
                    sound_mgr.play_click()
                    theme_index = (theme_index + 1) % len(THEMES)

                elif event.key == pygame.K_s:
                    sound_mgr.toggle()

                elif event.key == pygame.K_a:
                    sound_mgr.play_click()
                    alert_threshold_cm = 20.0 if alert_threshold_cm == 40.0 else (alert_threshold_cm + 10.0)
                    if serial_mgr.is_connected:
                        serial_mgr.send_command(f"ALERT:{int(alert_threshold_cm)}")

                elif event.key == pygame.K_d:
                    simulator.spawn_alert_intruder()
                    sound_mgr.play_alarm()

                elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    sound_mgr.play_click()
                    is_paused = not is_paused

                elif event.key == pygame.K_r:
                    sound_mgr.play_click()
                    radar.clear()

                elif event.key == pygame.K_h:
                    show_scanlines = not show_scanlines

                elif event.key == pygame.K_f or event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        w, h = screen.get_size()
                    else:
                        screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.RESIZABLE)
                        w, h = 1280, 720
                    radar_cx = w // 2
                    radar_cy = h - 100
                    radar_r = min(360, max(220, int(h * 0.44)))
                    radar.set_center_and_radius(radar_cx, radar_cy, radar_r)
                    hud = HUDPanels(w, h)

        # Update telemetry data if not paused
        if not is_paused:
            sample = None
            if is_sim_mode:
                sample = simulator.update()
            else:
                sample = serial_mgr.get_latest_sample()

            if sample:
                ang, dist, valid = sample
                current_angle = ang
                current_dist = dist
                is_valid = valid

                is_alert = (valid and (0.0 < dist <= alert_threshold_cm))
                radar.add_echo(current_angle, current_dist, alert_threshold_cm)
                hud.update_history(current_dist)

                # Sound effects
                if is_alert:
                    sound_mgr.play_alarm()
                elif valid and dist > 0:
                    sound_mgr.play_ping()

            radar.update_particles(dt)

            # Check if new target was locked
            cur_tgt_count = len(radar.tracked_targets)
            if cur_tgt_count > last_target_count:
                sound_mgr.play_lock()
            last_target_count = cur_tgt_count

        # Clear background
        screen.fill(theme.bg)

        # Render Main Radar Display
        radar.render(screen, theme, fonts, alert_threshold_cm)

        # Render Sci-Fi HUD Panels
        conn_str = serial_mgr.connection_status
        hud.render(
            screen=screen,
            theme=theme,
            fonts=fonts,
            current_angle=current_angle,
            current_dist=current_dist,
            is_valid=is_valid,
            is_alert=is_alert,
            alert_threshold_cm=alert_threshold_cm,
            is_sim_mode=is_sim_mode,
            conn_status=conn_str,
            audio_enabled=sound_mgr.enabled,
            is_paused=is_paused,
            fps=clock.get_fps(),
            tracked_targets=radar.tracked_targets,
            show_scanlines=show_scanlines
        )

        pygame.display.flip()

    serial_mgr.disconnect()
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()

