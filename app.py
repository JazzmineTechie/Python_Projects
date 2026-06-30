import pygame
import sys
import math
import numpy as np

# ==========================================
# 1. INITIALIZATION & SYSTEM CONFIGURATION
# ==========================================
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 680
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Music Matcha")
clock = pygame.time.Clock()

# Color Palettes (RGB Formats)
COLOR_BG = (12, 14, 20)          
COLOR_WHITE_KEY = (245, 245, 250) 
COLOR_BLACK_KEY = (25, 28, 36)
COLOR_DARK_KEY = (38, 42, 53)     
COLOR_CYAN = (0, 255, 221)        
COLOR_MAGENTA = (255, 0, 127)     
COLOR_YELLOW = (255, 213, 0)      
COLOR_GRID_OFF = (40, 46, 62)     
COLOR_TEXT = (180, 190, 210)      
COLOR_PANEL = (22, 26, 38)

# Initialize System Fonts
try:
    font_small = pygame.font.SysFont("Arial", 11, bold=True)
    font_medium = pygame.font.SysFont("Arial", 15, bold=True)
    font_title = pygame.font.SysFont("Arial", 20, bold=True)
except Exception:
    font_small = pygame.font.Font(None, 14)
    font_medium = pygame.font.Font(None, 20)
    font_title = pygame.font.Font(None, 28)

# Global Volume States (0.0 to 1.0)
piano_volume = 0.7
drum_volume = 0.7
bass_volume = 0.6

# Global Visualizer Buffer for Live Waveform Rendering
visualizer_buffer = np.zeros(100)

# ==========================================
# 2. AUDIO SYNTHESIS & SOUND GENERATOR
# ==========================================
def generate_synth_wave(frequency, duration=0.5, wave_type="sine", volume_multiplier=1.0):
    global visualizer_buffer
    sample_rate = 44100
    total_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, total_samples, False)
    
    if wave_type == "sine":
        wave_data = np.sin(2 * np.pi * frequency * t)
    elif wave_type == "triangle":
        wave_data = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
    elif wave_type == "square":
        wave_data = np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave_type == "noise":
        wave_data = np.random.uniform(-1, 1, total_samples)
        envelope = np.exp(-18 * t)
        wave_data = wave_data * envelope
    elif wave_type == "kick":
        freqs = frequency * np.exp(-35 * t)
        wave_data = np.sin(2 * np.pi * freqs * t)
        envelope = np.exp(-10 * t)
        wave_data = wave_data * envelope
    else:
        wave_data = np.sin(2 * np.pi * frequency * t)

    fade_len = int(sample_rate * 0.05)
    if total_samples > fade_len:
        fade_out = np.linspace(1.0, 0.0, fade_len)
        wave_data[-fade_len:] *= fade_out

    step = max(1, len(wave_data) // 100)
    snapshot = wave_data[::step][:100]
    if len(snapshot) == 100:
        visualizer_buffer = np.clip(visualizer_buffer + snapshot * 1.5, -1.0, 1.0)

    audio_signal = int(32767 * 0.4 * volume_multiplier) * wave_data
    audio_signal = audio_signal.astype(np.int16)
    stereo_signal = np.column_stack((audio_signal, audio_signal))
    return pygame.sndarray.make_sound(stereo_signal)

WHITE_FREQS = {"C": 261.63, "D": 293.66, "E": 329.63, "F": 349.23, "G": 392.00, "A": 440.00, "B": 493.88}
BLACK_FREQS = {"C#": 277.18, "D#": 311.13, "F#": 369.99, "G#": 415.30, "A#": 466.16}
BASS_FREQS =  {"C": 65.41,  "D": 73.42,  "E": 82.41,  "F": 87.31,  "G": 98.00,  "A": 110.00, "B": 123.47}

PIANO_WHITE_SOUNDS = {n: generate_synth_wave(f, 0.5, "sine", piano_volume) for n, f in WHITE_FREQS.items()}
PIANO_BLACK_SOUNDS = {n: generate_synth_wave(f, 0.5, "square", piano_volume) for n, f in BLACK_FREQS.items()}
BASS_SOUNDS = {n: generate_synth_wave(f, 0.6, "triangle", bass_volume) for n, f in BASS_FREQS.items()}

drum_kits = {
    "Acoustic Studio": [generate_synth_wave(150, 0.2, "kick", drum_volume), generate_synth_wave(0, 0.12, "noise", drum_volume)],
    "Electronic 808": [generate_synth_wave(80, 0.4, "kick", drum_volume * 1.2), generate_synth_wave(0, 0.08, "noise", drum_volume * 0.8)]
}
current_kit_name = "Acoustic Studio"

KEY_MAP = {
    pygame.K_a: "C", pygame.K_s: "D", pygame.K_d: "E", pygame.K_f: "F",
    pygame.K_g: "G", pygame.K_h: "A", pygame.K_j: "B"
}

CHORD_DICTIONARY = {
    "C": "C Major (Happy - C, E, G)", "D": "D Minor (Sad - D, F, A)", "E": "E Minor (Mystical - E, G, B)",
    "F": "F Major (Grand - F, A, C)", "G": "G Major (Triumphant - G, B, D)", "A": "A Minor (Melancholic - A, C, E)",
    "B": "B Diminished (Tense - B, D, F)"
}

# ==========================================
# 3. INTERACTIVE VISUAL ANIMATION ENGINE
# ==========================================
class ParticleAnimation:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color # This is an RGB tuple (e.g., (0, 255, 221))
        self.radius = 5
        self.alpha = 255
        self.active = True

    def update(self):
        self.radius += 5
        self.alpha -= 12
        if self.alpha <= 0:
            self.active = False

    def draw(self, surface):
        if self.active:
            target_radius = int(self.radius)
            anim_surface = pygame.Surface((target_radius * 2, target_radius * 2), pygame.SRCALPHA)
            
            # FIXED: Correctly unpacking the color tuple to inject alpha channel safely
            color_with_alpha = (self.color[0], self.color[1], self.color[2], int(self.alpha))
            
            pygame.draw.circle(anim_surface, color_with_alpha, (target_radius, target_radius), target_radius, 2)
            surface.blit(anim_surface, (self.x - target_radius, self.y - target_radius))

active_animations = []

# ==========================================
# 4. OBJECT-ORIENTED INTERFACE COMPONENTS
# ==========================================
class PianoKey:
    def __init__(self, x, y, w, h, note_name, is_black, key_hint=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.note_name = note_name
        self.is_black = is_black
        self.key_hint = key_hint
        self.is_pressed = False

    def draw(self, surface):
        if self.is_pressed:
            color = COLOR_CYAN
        else:
            color = COLOR_BLACK_KEY if self.is_black else COLOR_WHITE_KEY
            
        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        pygame.draw.rect(surface, COLOR_DARK_KEY, self.rect, 2, border_radius=4)
        
        if not self.is_black:
            text = font_medium.render(self.note_name, True, COLOR_DARK_KEY)
            surface.blit(text, (self.rect.x + self.rect.width//2 - 6, self.rect.y + self.rect.height - 38))
            if self.key_hint:
                hint = font_small.render(f"[{self.key_hint}]", True, (130, 140, 150))
                surface.blit(hint, (self.rect.x + self.rect.width//2 - 10, self.rect.y + self.rect.height - 20))

    def trigger(self):
        global current_detected_chord
        self.is_pressed = True
        if self.is_black:
            PIANO_BLACK_SOUNDS[self.note_name].play()
        else:
            PIANO_WHITE_SOUNDS[self.note_name].play()
            current_detected_chord = CHORD_DICTIONARY.get(self.note_name, "")
        active_animations.append(ParticleAnimation(self.rect.centerx, self.rect.centery, COLOR_CYAN))

class DrumPad:
    def __init__(self, x, y, w, h, instrument_type):
        self.rect = pygame.Rect(x, y, w, h)
        self.instrument_type = instrument_type # 0 = Kick, 1 = Snare
        self.is_active = False

    def draw(self, surface, highlight=False):
        if highlight:
            color = (255, 120, 190)
        else:
            color = COLOR_MAGENTA if self.is_active else COLOR_GRID_OFF
        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        pygame.draw.rect(surface, COLOR_DARK_KEY, self.rect, 1, border_radius=4)

class BassString:
    def __init__(self, x, y, w, h, note_name):
        self.rect = pygame.Rect(x, y, w, h)
        self.note_name = note_name
        self.is_playing = False
        self.flash_timer = 0

    def draw(self, surface):
        if self.is_playing and self.flash_timer > 0:
            color = (65, 60, 35)
            self.flash_timer -= 1
            if self.flash_timer <= 0:
                self.is_playing = False
        else:
            color = COLOR_GRID_OFF

        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        pygame.draw.rect(surface, COLOR_DARK_KEY, self.rect, 1, border_radius=4)
        pygame.draw.line(surface, COLOR_YELLOW, (self.rect.x, self.rect.centery), (self.rect.x + self.rect.width, self.rect.centery), 2)
        
        text = font_small.render(f"Bass {self.note_name}", True, COLOR_TEXT)
        surface.blit(text, (self.rect.x - 75, self.rect.y + 6))

    def trigger(self, trigger_x):
        self.is_playing = True
        self.flash_timer = 12
        BASS_SOUNDS[self.note_name].play()
        active_animations.append(ParticleAnimation(trigger_x, self.rect.centery, COLOR_YELLOW))

class ControlSlider:
    def __init__(self, x, y, w, h, label, min_val, max_val, default_val, accent_color):
        self.track_rect = pygame.Rect(x, y, w, h)
        self.handle_rect = pygame.Rect(x + w//2 - 6, y - 4, 12, h + 8)
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = default_val
        self.accent_color = accent_color
        self.is_dragging = False
        
        ratio = (default_val - min_val) / (max_val - min_val)
        self.handle_rect.x = int(x + (ratio * w) - 6)

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_GRID_OFF, self.track_rect, border_radius=2)
        pygame.draw.rect(surface, self.accent_color, self.handle_rect, border_radius=4)
        lbl = font_small.render(f"{self.label}: {int(self.current_val)}", True, COLOR_TEXT)
        surface.blit(lbl, (self.track_rect.x, self.track_rect.y - 16))

    def update(self, mouse_pos_tuple):
        if self.is_dragging:
                    # Extract raw integer X position directly inside the function wrapper
            mouse_x = mouse_pos_tuple[0]
        new_x = max(self.track_rect.x, min(mouse_x, self.track_rect.x + self.track_rect.width))
        self.handle_rect.x = new_x - self.handle_rect.width // 2
        ratio = (new_x - self.track_rect.x) / self.track_rect.width
        self.current_val = self.min_val + (ratio * (self.max_val - self.min_val))

# ==========================================
# 5. INITIAL SYSTEM LAYOUT INSTANTIATIONS
# ==========================================
piano_white_keys = []
piano_black_keys = []
X_START = 150
key_letters = ["A", "S", "D", "F", "G", "H", "J"]

for i, note in enumerate(WHITE_FREQS.keys()):
    piano_white_keys.append(PianoKey(X_START + (i * 65), 470, 60, 150, note, False, key_letters[i] if i < len(key_letters) else ""))

black_offsets = [0, 1, 3, 4, 5]
black_notes = list(BLACK_FREQS.keys())
for i, offset_idx in enumerate(black_offsets):
    w_key_x = piano_white_keys[offset_idx].rect.x
    piano_black_keys.append(PianoKey(w_key_x + 42, 470, 36, 90, black_notes[i], True))

drum_matrix = [[], []]
for row in range(2):
    for step in range(16):
        drum_matrix[row].append(DrumPad(X_START + (step * 50), 110 + (row * 42), 45, 36, row))

bass_notes = ["C", "E", "G", "B"]
bass_strings = []
for i, note in enumerate(bass_notes):
    bass_strings.append(BassString(X_START, 215 + (i * 36), 795, 30, note))

bpm_slider = ControlSlider(745, 30, 200, 6, "BPM Speed Control", 60, 240, 120, COLOR_CYAN)
vol_slider = ControlSlider(745, 68, 200, 6, "Main Synth Output Vol", 0, 100, 70, COLOR_YELLOW)

kit_btn_rect = pygame.Rect(560, 28, 150, 42)

sequencer_clock = 0
current_step = 0
current_detected_chord = "Play piano options [A to J keyboard hotkeys enabled]"
is_playing = False  # Start paused so users can click notes first!

# ==========================================
# 6. RUNTIME APPLICATION ENVIRONMENT LOOP
# ==========================================
running = True
while running:
    
    frames_per_beat = max(2, int((60 * 15) / bpm_slider.current_val))
    visualizer_buffer *= 0.86

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard Interceptions
                # --- Inside your event loop, under if event.type == pygame.KEYDOWN: ---
        if event.type == pygame.KEYDOWN:
            # Toggle play/pause state when user presses the spacebar
            if event.key == pygame.K_SPACE:
                is_playing = not is_playing
                # Update the display subtitle banner to guide the user
                if is_playing:
                    current_detected_chord = "Sequencer Started! Press [SPACE] to Pause."
                else:
                    current_detected_chord = "Sequencer Paused. Press [SPACE] to Play."

            if event.key in KEY_MAP:
                t_note = KEY_MAP[event.key]
                for w_key in piano_white_keys:
                    if w_key.note_name == t_note:
                        w_key.trigger()


        if event.type == pygame.KEYUP:
            if event.key in KEY_MAP:
                t_note = KEY_MAP[event.key]
                for w_key in piano_white_keys:
                    if w_key.note_name == t_note:
                        w_key.is_pressed = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            if bpm_slider.handle_rect.collidepoint(mouse_pos):
                bpm_slider.is_dragging = True
            if vol_slider.handle_rect.collidepoint(mouse_pos):
                vol_slider.is_dragging = True
            if kit_btn_rect.collidepoint(mouse_pos):
                current_kit_name = "Electronic 808" if current_kit_name == "Acoustic Studio" else "Acoustic Studio"

            for b_key in piano_black_keys:
                if b_key.rect.collidepoint(mouse_pos):
                    b_key.trigger()
            for w_key in piano_white_keys:
                if w_key.rect.collidepoint(mouse_pos):
                    w_key.trigger()

            for row in drum_matrix:
                for pad in row:
                    if pad.rect.collidepoint(mouse_pos):
                        pad.is_active = not pad.is_active

            for b_str in bass_strings:
                if b_str.rect.collidepoint(mouse_pos):
                    b_str.trigger(mouse_pos[0])

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            bpm_slider.is_dragging = False
            vol_slider.is_dragging = False
            for w_key in piano_white_keys:
                w_key.is_pressed = False
            for b_key in piano_black_keys:
                b_key.is_pressed = False

    if bpm_slider.is_dragging:
        bpm_slider.update(pygame.mouse.get_pos())
    if vol_slider.is_dragging:
        vol_slider.update(pygame.mouse.get_pos())

    # Sequence Loop Automation Tracker
    sequencer_clock += 1
        # --- Replace your previous Sequence Loop Automation Tracker block with this ---
    if is_playing:
        sequencer_clock += 1
        if sequencer_clock >= frames_per_beat:
            sequencer_clock = 0
            current_step = (current_step + 1) % 16
            
            active_kit = drum_kits[current_kit_name]
            
            if drum_matrix[0][current_step].is_active:
                active_kit[0].play() 
                active_animations.append(ParticleAnimation(drum_matrix[0][current_step].rect.centerx, drum_matrix[0][current_step].rect.centery, COLOR_MAGENTA))
                
            if drum_matrix[1][current_step].is_active:
                active_kit[1].play() 
                active_animations.append(ParticleAnimation(drum_matrix[1][current_step].rect.centerx, drum_matrix[1][current_step].rect.centery, COLOR_MAGENTA))

            if current_step % 4 == 0:
                t_idx = (current_step // 4) % len(bass_strings)
                bass_strings[t_idx].trigger(drum_matrix[0][current_step].rect.centerx)

    # --- Render Stack ---
    screen.fill(COLOR_BG)

    # Labels Panels Text Graphics
    text_main_title = font_title.render("Matcha Studio", True, COLOR_CYAN)
    screen.blit(text_main_title, (25, 22))
    
    pygame.draw.rect(screen, COLOR_DARK_KEY if current_kit_name == "Acoustic Studio" else COLOR_PANEL, kit_btn_rect, border_radius=6)
    pygame.draw.rect(screen, COLOR_MAGENTA, kit_btn_rect, 1, border_radius=6)
    kit_txt = font_medium.render(f"KIT: {current_kit_name}", True, COLOR_WHITE_KEY)
    screen.blit(kit_txt, (kit_btn_rect.x + 20, kit_btn_rect.y + 12))

    # Render Oscilloscope View Window
    pygame.draw.rect(screen, COLOR_PANEL, (25, 62, 100, 32), border_radius=4)
    for idx, dynamic_amplitude in enumerate(visualizer_buffer):
        v_x = 25 + idx
        v_h = int(dynamic_amplitude * 14)
        pygame.draw.line(screen, COLOR_CYAN, (v_x, 78 - v_h), (v_x, 78 + v_h), 1)

    text_drum_lbl = font_medium.render("Percussion Grid System (Kick / Snare Tracks)", True, COLOR_MAGENTA)
    screen.blit(text_drum_lbl, (150, 88))
    
    text_bass_lbl = font_medium.render("Bass Guitar Polyphonic Strings Tracker", True, COLOR_YELLOW)
    screen.blit(text_bass_lbl, (150, 362))

    text_piano_lbl = font_medium.render("Chromatic Grand Piano Synthesizer Console", True, COLOR_WHITE_KEY)
    screen.blit(text_piano_lbl, (150, 445))

    pygame.draw.rect(screen, COLOR_PANEL, (150, 405, 795, 26), border_radius=4)
    theory_txt = font_small.render(f"LAB INSIGHTS: {current_detected_chord}", True, COLOR_CYAN)
    screen.blit(theory_txt, (162, 412))

    # Track Background Panel
    pygame.draw.rect(screen, COLOR_PANEL, (135, 102, 825, 92), border_radius=6)

    # Process Array Elements Draw Calls
    bpm_slider.draw(screen)
    vol_slider.draw(screen)

    for row_idx, row in enumerate(drum_matrix):
        lbl_str = "Kick" if row_idx == 0 else "Snare"
        lbl_obj = font_small.render(lbl_str, True, COLOR_TEXT)
        screen.blit(lbl_obj, (55, 120 + (row_idx * 42)))
        for step_idx, pad in enumerate(row):
            pad.draw(screen, highlight=(step_idx == current_step))

    for b_str in bass_strings:
        b_str.draw(screen)
    
    # Draw Timeline Playhead Guide Bar Sync Line
    p_x = drum_matrix[0][current_step].rect.centerx
    pygame.draw.line(screen, (255, 255, 255), (p_x, 102), (p_x, 345), 2)

    for w_key in piano_white_keys:
        w_key.draw(screen)
    for b_key in piano_black_keys:
        b_key.draw(screen)

    # Visual Updates
    for anim in active_animations[:]:
        anim.update()
        if not anim.active:
            active_animations.remove(anim)
        else:
            anim.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.mixer.quit()
pygame.quit()
sys.exit()
