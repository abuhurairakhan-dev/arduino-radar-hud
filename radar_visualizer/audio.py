import time
import numpy as np
import pygame

class SoundManager:
    """Procedural audio synthesizer for sci-fi radar sound effects."""
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.enabled = True
        self.mixer_initialized = False
        self.last_ping_time = 0.0
        self.last_alarm_time = 0.0
        self.last_lock_time = 0.0

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=2, buffer=512)
            self.mixer_initialized = True
            self._generate_sounds()
        except Exception as e:
            print(f"[Audio] Note: Audio initialization skipped ({e}). Visualizer will run silently.")
            self.enabled = False

    def _generate_sounds(self):
        sr = self.sample_rate

        # 1. Sonar Ping (Sci-fi resonance sweep ping)
        dur_ping = 0.12
        t = np.linspace(0, dur_ping, int(sr * dur_ping), False)
        # 1150 Hz main tone + 2300 Hz subtle overtone with exponential decay
        decay = np.exp(-t * 28.0)
        ping_wave = (0.75 * np.sin(2 * np.pi * 1150 * t) + 0.25 * np.sin(2 * np.pi * 2300 * t)) * decay
        arr_ping = (ping_wave * 14000).astype(np.int16)
        stereo_ping = np.column_stack((arr_ping, arr_ping))
        self.sound_ping = pygame.sndarray.make_sound(stereo_ping)
        self.sound_ping.set_volume(0.28)

        # 2. Alert Klaxon (Urgent sci-fi proximity warble)
        dur_alarm = 0.18
        t_alarm = np.linspace(0, dur_alarm, int(sr * dur_alarm), False)
        # Frequency modulated alert tone from 650Hz to 950Hz
        fm = 800.0 + 200.0 * np.sin(2 * np.pi * 25.0 * t_alarm)
        phase = 2 * np.pi * np.cumsum(fm) / sr
        decay_alarm = np.minimum(1.0, 1.2 - t_alarm / dur_alarm)
        alarm_wave = np.sin(phase) * decay_alarm
        arr_alarm = (alarm_wave * 16000).astype(np.int16)
        stereo_alarm = np.column_stack((arr_alarm, arr_alarm))
        self.sound_alarm = pygame.sndarray.make_sound(stereo_alarm)
        self.sound_alarm.set_volume(0.35)

        # 3. Lock-On Chirp (High-tech reticle target acquisition)
        dur_lock = 0.09
        t_lock = np.linspace(0, dur_lock, int(sr * dur_lock), False)
        # Rapid upward chirp 1600Hz -> 2800Hz
        freq_sweep = np.linspace(1600, 2800, len(t_lock))
        phase_lock = 2 * np.pi * np.cumsum(freq_sweep) / sr
        lock_wave = np.sin(phase_lock) * np.exp(-t_lock * 18.0)
        arr_lock = (lock_wave * 12000).astype(np.int16)
        stereo_lock = np.column_stack((arr_lock, arr_lock))
        self.sound_lock = pygame.sndarray.make_sound(stereo_lock)
        self.sound_lock.set_volume(0.22)

        # 4. Interface Click (Crisp tactical key tap)
        dur_click = 0.03
        t_click = np.linspace(0, dur_click, int(sr * dur_click), False)
        click_wave = np.sin(2 * np.pi * 2200 * t_click) * np.exp(-t_click * 120.0)
        arr_click = (click_wave * 12000).astype(np.int16)
        stereo_click = np.column_stack((arr_click, arr_click))
        self.sound_click = pygame.sndarray.make_sound(stereo_click)
        self.sound_click.set_volume(0.25)

    def toggle(self):
        """Toggle audio mute state."""
        self.enabled = not self.enabled
        return self.enabled

    def play_ping(self):
        now = time.time()
        if self.enabled and self.mixer_initialized and (now - self.last_ping_time > 0.08):
            self.last_ping_time = now
            try:
                self.sound_ping.play()
            except Exception:
                pass

    def play_alarm(self):
        now = time.time()
        if self.enabled and self.mixer_initialized and (now - self.last_alarm_time > 0.22):
            self.last_alarm_time = now
            try:
                self.sound_alarm.play()
            except Exception:
                pass

    def play_lock(self):
        now = time.time()
        if self.enabled and self.mixer_initialized and (now - self.last_lock_time > 0.35):
            self.last_lock_time = now
            try:
                self.sound_lock.play()
            except Exception:
                pass

    def play_click(self):
        if self.enabled and self.mixer_initialized:
            try:
                self.sound_click.play()
            except Exception:
                pass

