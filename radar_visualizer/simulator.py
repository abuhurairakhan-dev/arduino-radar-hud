import math
import time
import random
from typing import Tuple, List, Optional

class SimulatedTarget:
    """A target object in polar coordinates with autonomous motion."""
    def __init__(self, name: str, angle: float, distance: float, speed_dist: float = 0.0, speed_angle: float = 0.0, span: float = 6.0):
        self.name = name
        self.angle = angle
        self.distance = distance
        self.speed_dist = speed_dist
        self.speed_angle = speed_angle
        self.span = span # angular width in degrees
        self.base_distance = distance
        self.min_dist = 12.0
        self.max_dist = 48.0

    def update(self, dt: float):
        self.angle += self.speed_angle * dt
        # Bounce angle within scan field
        if self.angle > 155:
            self.angle = 155
            self.speed_angle *= -1
        elif self.angle < 25:
            self.angle = 25
            self.speed_angle *= -1

        self.distance += self.speed_dist * dt
        if self.distance < self.min_dist:
            self.distance = self.min_dist
            self.speed_dist *= -1
        elif self.distance > self.max_dist:
            self.distance = self.max_dist
            self.speed_dist *= -1

class RadarSimulator:
    """Simulates the Arduino Uno + SG90 Servo + HC-SR04 ultrasonic sensor."""
    def __init__(self, min_angle: int = 15, max_angle: int = 165, step: int = 1, interval_sec: float = 0.04):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.step = step
        self.interval_sec = interval_sec
        self.current_angle = float(min_angle)
        self.direction = 1
        self.last_step_time = time.time()
        self.last_update_time = time.time()

        # Initialize realistic targets
        self.targets: List[SimulatedTarget] = [
            # Intruder drone: moves back and forth and closes in, triggering alerts
            SimulatedTarget("INTRUDER-ALPHA", angle=75.0, distance=36.0, speed_dist=-6.0, speed_angle=8.0, span=8.0),
            # Stationary barrier / wall
            SimulatedTarget("BARRIER-01", angle=135.0, distance=41.0, speed_dist=0.0, speed_angle=0.0, span=12.0),
            # Small scout drone
            SimulatedTarget("PROBE-BETA", angle=35.0, distance=26.0, speed_dist=4.0, speed_angle=-10.0, span=5.0),
        ]

    def add_user_target(self, angle: float, distance: float):
        """Allows user to click on radar grid to place a custom target."""
        self.targets.append(
            SimulatedTarget(f"TGT-MK{len(self.targets)+1}", angle=angle, distance=distance, speed_dist=0.0, speed_angle=0.0, span=7.0)
        )
        if len(self.targets) > 6:
            self.targets.pop(0)

    def spawn_alert_intruder(self):
        """Spawns an aggressive high-speed intruder breaching the perimeter."""
        self.targets.append(
            SimulatedTarget("FAST-HOSTILE", angle=90.0, distance=45.0, speed_dist=-18.0, speed_angle=random.uniform(-15.0, 15.0), span=7.0)
        )

    def update(self) -> Optional[Tuple[int, float, bool]]:
        """
        Updates simulation. Returns (angle, distance_cm, is_valid) if a new scan sample is ready,
        else None.
        """
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now

        for t in self.targets:
            t.update(dt)

        if now - self.last_step_time < self.interval_sec:
            return None

        self.last_step_time = now

        # Advance servo angle
        self.current_angle += self.direction * self.step
        if self.current_angle >= self.max_angle:
            self.current_angle = float(self.max_angle)
            self.direction = -1
        elif self.current_angle <= self.min_angle:
            self.current_angle = float(self.min_angle)
            self.direction = 1

        # Check ray intersection with targets
        best_dist = 999.0
        cur_ang = self.current_angle

        for t in self.targets:
            half_span = t.span / 2.0
            if (t.angle - half_span) <= cur_ang <= (t.angle + half_span):
                # Add slight ultrasonic jitter / sensor noise (±0.3cm)
                measured = t.distance + random.uniform(-0.35, 0.35)
                if measured < best_dist:
                    best_dist = measured

        if best_dist <= 55.0:
            return int(cur_ang), round(best_dist, 1), True
        else:
            return int(cur_ang), -1.0, False

