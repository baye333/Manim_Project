"""Palette, composants visuels et service de voix."""
import os
import subprocess

from manim import *

# ---------- Réglages ----------
FONT = os.environ.get("FONT", "Sans")        # ex: FONT="Poppins"
MONO = os.environ.get("MONO", "Monospace")

BG = "#060b14"
PANEL = "#0d1624"
TEXT_C = "#e6edf3"
MUTED = "#8b949e"
GIT_C = "#f05033"      # orange Git
HUB_C = "#58a6ff"      # bleu GitHub
GREEN = "#3fb950"
YELLOW = "#ffc83d"
RED = "#ff6b6b"
GITLAB_C = "#fc6d26"
BITB_C = "#2684ff"

# Zones sûres pour TikTok (cadre : 4.5 x 8 unités)
TOP_Y = 3.55           # puces de chapitre
SUB_Y = -2.35          # sous-titres
MAX_W = 4.1            # largeur max du contenu


# ---------- Texte ----------
def txt(s, size=36, color=TEXT_C, bold=False, mono=False, **kw):
    t = Text(s, font=MONO if mono else FONT, font_size=size, color=color,
             weight=BOLD if bold else NORMAL, **kw)
    if t.width > MAX_W:
        t.scale_to_fit_width(MAX_W)
    return t


class Pill(VGroup):
    """Étiquette arrondie : Pill("En ligne", HUB_C)."""
    def __init__(self, label, color=YELLOW, size=22, filled=False):
        t = txt(label, size=size, color=BLACK if filled else color, bold=True)
        box = RoundedRectangle(
            corner_radius=0.22, height=0.44, width=t.width + 0.45,
            stroke_color=color, stroke_width=3,
            fill_color=color, fill_opacity=1 if filled else 0.14,
        )
        t.move_to(box)
        super().__init__(box, t)
        self.box, self.label = box, t


class Laptop(VGroup):
    def __init__(self, color=GIT_C, width=2.0, height=1.3):
        screen = RoundedRectangle(
            corner_radius=0.12, width=width, height=height,
            stroke_color=color, stroke_width=4,
            fill_color=PANEL, fill_opacity=1,
        )
        base = RoundedRectangle(
            corner_radius=0.07, width=width * 1.25, height=0.14,
            stroke_width=0, fill_color=color, fill_opacity=1,
        ).next_to(screen, DOWN, buff=0.06)
        super().__init__(screen, base)
        self.screen, self.base = screen, base


class Cloud(VGroup):
    def __init__(self, color=HUB_C, label="GitHub", label_size=30):
        parts = VGroup(
            Circle(radius=0.55).move_to([-0.60, -0.05, 0]),
            Circle(radius=0.80).move_to([0.05, 0.22, 0]),
            Circle(radius=0.52).move_to([0.75, -0.05, 0]),
            RoundedRectangle(corner_radius=0.3, width=2.2, height=0.62).move_to([0.05, -0.27, 0]),
        )
        parts.set_fill(color, 1).set_stroke(width=0)
        parts.move_to(ORIGIN)
        t = txt(label, size=label_size, color=BLACK, bold=True).move_to(parts.get_center() + DOWN * 0.1)
        super().__init__(parts, t)
        self.body, self.label = parts, t


class Node(VGroup):
    """Un commit : rond avec une étiquette."""
    def __init__(self, label, color=YELLOW, r=0.27):
        c = Circle(radius=r, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.25)
        t = txt(label, size=18, color=color, bold=True).move_to(c)
        super().__init__(c, t)
        self.circle = c


def link(a, b, color=MUTED, w=4):
    """Trait entre deux mobjects (bord à bord)."""
    d = b.get_center() - a.get_center()
    d = d / np.linalg.norm(d)
    r = a.circle.width / 2 if hasattr(a, "circle") else 0
    return Line(a.get_center() + d * r, b.get_center() - d * r, color=color, stroke_width=w)


# ---------- Voix ----------
def get_voice_service():
    """VOICE=rec (ta voix, défaut) | gtts (voix de synthèse) | silent (test sans voix)."""
    mode = os.environ.get("VOICE", "rec").lower()
    if mode == "gtts":
        from manim_voiceover.services.gtts import GTTSService
        return GTTSService(lang="fr")
    if mode == "silent":
        return SilentService()
    from manim_voiceover.services.recorder import RecorderService
    return RecorderService()


from manim_voiceover.services.base import SpeechService


class SilentService(SpeechService):
    """Génère un silence proportionnel au texte : sert à tester l'animation sans micro."""

    def generate_from_text(self, text, cache_dir=None, path=None, **kwargs):
        cache_dir = cache_dir or self.cache_dir
        input_data = {"input_text": text, "service": "silent"}
        cached = self.get_cached_result(input_data, cache_dir)
        if cached is not None:
            return cached
        audio_path = (self.get_audio_basename(input_data) + ".mp3") if path is None else str(path)
        dur = max(1.5, len(text.split()) * 0.42)
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
             "anullsrc=r=44100:cl=mono", "-t", f"{dur:.2f}", "-q:a", "9",
             "-acodec", "libmp3lame", os.path.join(str(cache_dir), audio_path)],
            check=True,
        )
        return {"input_text": text, "input_data": input_data, "original_audio": audio_path}
