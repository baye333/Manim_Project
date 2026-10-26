"""
Git vs GitHub — capsule verticale 9:16 avec voix off.
Rendu :  python run.py preview | final   (voir README.md)
"""
import os
from contextlib import contextmanager

from manim import *
from manim_voiceover import VoiceoverScene

import script as S
from helpers import *

# ---------- Format vertical 9:16 ----------
PREVIEW = os.environ.get("PREVIEW") == "1"
config.pixel_width = 540 if PREVIEW else 1080
config.pixel_height = 960 if PREVIEW else 1920
config.frame_width = 4.5
config.frame_height = 8
config.frame_rate = 15 if PREVIEW else 30
config.background_color = BG

CHAPTERS = ["Git", "GitHub", "Lien", "Bilan"]


def chunk_text(text, limit=17):
    """Découpe en petits morceaux pour des sous-titres dynamiques."""
    chunks, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > limit:
            chunks.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        chunks.append(cur)
    return chunks


class GitVsGithub(VoiceoverScene):
    # ------------------------------------------------------------
    # Outils de scène
    # ------------------------------------------------------------
    def _subtitle(self, text, duration):
        chunks = chunk_text(text)
        total = sum(len(c) for c in chunks)
        bounds, acc = [], 0
        for c in chunks:
            acc += len(c)
            bounds.append(acc / total)
        state = {"t": 0.0, "i": -1}

        def build(c):
            t = Text(c, font=FONT, font_size=32, weight=BOLD, color=WHITE)
            if t.width > MAX_W - 0.3:
                t.scale_to_fit_width(MAX_W - 0.3)
            bg = RoundedRectangle(
                corner_radius=0.12, width=t.width + 0.3, height=t.height + 0.28,
                fill_color=BLACK, fill_opacity=0.7, stroke_width=0,
            )
            g = VGroup(bg, t).move_to(UP * SUB_Y)
            for m in g.family_members_with_points():
                m.set_z_index(100)
            return g

        pieces = [build(c) for c in chunks]

        def show(k):
            for j, g in enumerate(pieces):
                on = j == k
                g[0].set_fill(BLACK, opacity=0.7 if on else 0)
                g[1].set_opacity(1 if on else 0)

        def upd(m, dt):
            state["t"] += dt
            frac = min(state["t"] / max(duration, 0.01), 1.0)
            idx = next((k for k, b in enumerate(bounds) if frac <= b), len(bounds) - 1)
            if idx != state["i"]:
                state["i"] = idx
                show(idx)

        holder = VGroup(*pieces)
        holder.add_updater(upd)
        self.add(holder)
        return holder

    @contextmanager
    def say(self, text):
        """Voix + sous-titres synchronisés. Les animations du bloc `with` durent
        au plus tracker.duration."""
        with self.voiceover(text=text) as tracker:
            sub = self._subtitle(text, tracker.duration)
            yield tracker
        sub.clear_updaters()
        self.remove(sub)

    def make_chips(self):
        chips = VGroup()
        for name in CHAPTERS:
            t = txt(name, size=18, color=MUTED, bold=True)
            r = RoundedRectangle(
                corner_radius=0.14, height=0.36, width=t.width + 0.35,
                stroke_color=MUTED, stroke_width=2, fill_opacity=0,
            )
            t.move_to(r)
            chips.add(VGroup(r, t))
        chips.arrange(RIGHT, buff=0.1).move_to(UP * TOP_Y)
        if chips.width > MAX_W:
            chips.scale_to_fit_width(MAX_W)
        return chips

    def set_chapter(self, i):
        anims = []
        for k, chip in enumerate(self.chips):
            r, t = chip
            if k == i:
                anims += [r.animate.set_fill(YELLOW, 1).set_stroke(YELLOW), t.animate.set_color(BLACK)]
            else:
                anims += [r.animate.set_fill(opacity=0).set_stroke(MUTED), t.animate.set_color(MUTED)]
        self.play(*anims, run_time=0.35)

    def clear_stage(self):
        objs = [m for m in self.mobjects if m is not self.chips]
        if objs:
            self.play(*[FadeOut(o) for o in objs], run_time=0.5)

    # ------------------------------------------------------------
    def construct(self):
        self.set_speech_service(get_voice_service())
        self.chips = self.make_chips()
        self.add(self.chips)

        self.intro()
        self.part_git()
        self.part_github()
        self.part_link()
        self.part_recap()
        self.outro()

    # ------------------------------------------------------------
    # 1. Accroche
    # ------------------------------------------------------------
    def intro(self):
        git = Pill("Git", GIT_C, size=40, filled=True).move_to(UP * 1.9)
        hub = Pill("GitHub", HUB_C, size=40, filled=True).move_to(DOWN * 0.3)
        eq = txt("=  ?", size=64, color=YELLOW, bold=True).move_to(UP * 0.8)
        neq = txt("≠", size=80, color=RED, bold=True).move_to(UP * 0.8)

        with self.say(S.INTRO) as tr:
            d = tr.duration
            self.play(FadeIn(git, shift=DOWN * 0.3), FadeIn(hub, shift=UP * 0.3),
                      Write(eq), run_time=d * 0.35)
            self.play(Indicate(eq, color=YELLOW, scale_factor=1.25), run_time=d * 0.25)
            self.play(ReplacementTransform(eq, neq), run_time=d * 0.2)
            self.play(Indicate(neq, color=RED, scale_factor=1.3), run_time=d * 0.15)
        self.clear_stage()

    # ------------------------------------------------------------
    # 2. Git
    # ------------------------------------------------------------
    def part_git(self):
        self.set_chapter(0)

        # --- GIT_1 : outil local
        laptop = Laptop(GIT_C).move_to(UP * 1.2)
        cmd1 = txt("$ git init", size=20, color=GREEN, mono=True).move_to(laptop.screen.get_center() + UP * 0.2)
        cmd2 = txt("$ git commit", size=20, color=GIT_C, mono=True).next_to(cmd1, DOWN, buff=0.15, aligned_edge=LEFT)
        local = Pill("100 % local", GIT_C).next_to(laptop, DOWN, buff=0.45)
        with self.say(S.GIT_1) as tr:
            d = tr.duration
            self.play(FadeIn(laptop, shift=UP * 0.3, scale=0.9), run_time=d * 0.2)
            self.play(Write(cmd1), run_time=d * 0.2)
            self.play(Write(cmd2), run_time=d * 0.2)
            self.play(FadeIn(local, shift=UP * 0.2), run_time=d * 0.2)

        # --- GIT_2 : commits
        small = VGroup(laptop, cmd1, cmd2)
        nodes = VGroup(*[Node(f"v{i}", YELLOW) for i in (1, 2, 3)]).arrange(RIGHT, buff=0.9).move_to(UP * 0.3)
        lines = VGroup(*[link(nodes[i], nodes[i + 1]) for i in range(2)])
        back = CurvedArrow(nodes[2].get_top() + UP * 0.05, nodes[1].get_top() + UP * 0.05,
                           angle=TAU / 4, color=GREEN, stroke_width=5)
        back_label = Pill("retour", GREEN, size=18).next_to(back, UP, buff=0.12)
        with self.say(S.GIT_2) as tr:
            d = tr.duration
            self.play(FadeOut(local), small.animate.scale(0.55).move_to(UP * 2.55), run_time=d * 0.15)
            self.play(LaggedStart(
                FadeIn(nodes[0], scale=0.5), Create(lines[0]), FadeIn(nodes[1], scale=0.5),
                Create(lines[1]), FadeIn(nodes[2], scale=0.5), lag_ratio=0.35), run_time=d * 0.4)
            self.play(Create(back), FadeIn(back_label), run_time=d * 0.2)
            self.play(Indicate(nodes[1], color=GREEN, scale_factor=1.3), run_time=d * 0.2)

        # --- GIT_3 : branches
        branch_node = Node("f1", GREEN).move_to(nodes[1].get_center() + DOWN * 1.2 + RIGHT * 0.75)
        branch_line = Line(nodes[1].get_bottom(), branch_node.get_left(), color=GREEN, stroke_width=4)
        main_tag = Pill("main", YELLOW, size=18).next_to(nodes[0], DOWN, buff=0.3).shift(LEFT * 0.1)
        feat_tag = Pill("feature", GREEN, size=18).next_to(branch_node, DOWN, buff=0.2)
        with self.say(S.GIT_3) as tr:
            d = tr.duration
            self.play(FadeOut(back), FadeOut(back_label), FadeIn(main_tag), run_time=d * 0.2)
            self.play(Create(branch_line), FadeIn(branch_node, scale=0.5), run_time=d * 0.35)
            self.play(FadeIn(feat_tag, shift=UP * 0.2), run_time=d * 0.2)
        self.clear_stage()

    # ------------------------------------------------------------
    # 3. GitHub
    # ------------------------------------------------------------
    def part_github(self):
        self.set_chapter(1)

        cloud = Cloud(HUB_C, "GitHub").scale(0.85).move_to(UP * 1.9)
        online = Pill("En ligne", HUB_C, size=20).next_to(cloud, UP, buff=-0.05).shift(RIGHT * 1.1)
        repos = VGroup()
        for name in ("projet-1", "projet-2", "projet-3"):
            card = RoundedRectangle(corner_radius=0.1, width=1.25, height=0.7,
                                    stroke_color=HUB_C, stroke_width=3, fill_color=PANEL, fill_opacity=1)
            lab = txt(name, size=16, color=HUB_C, bold=True).move_to(card)
            repos.add(VGroup(card, lab))
        repos.arrange(RIGHT, buff=0.15).move_to(UP * 0.25)
        stems = VGroup(*[Line(cloud.get_bottom() + DOWN * 0.02, r.get_top(), color=MUTED, stroke_width=2) for r in repos])

        with self.say(S.HUB_1) as tr:
            d = tr.duration
            self.play(FadeIn(cloud, scale=0.7), run_time=d * 0.25)
            self.play(FadeIn(online, shift=DOWN * 0.2), run_time=d * 0.15)
            self.play(LaggedStart(*[AnimationGroup(Create(s), FadeIn(r, shift=UP * 0.2)) for s, r in zip(stems, repos)],
                                  lag_ratio=0.3), run_time=d * 0.4)

        feats = VGroup(
            Pill("Pull requests", GREEN, size=24),
            Pill("Issues", YELLOW, size=24),
            Pill("Revue de code", HUB_C, size=24),
        ).arrange(DOWN, buff=0.22).move_to(DOWN * 0.15)
        with self.say(S.HUB_2) as tr:
            d = tr.duration
            self.play(FadeOut(repos), FadeOut(stems), FadeOut(online), run_time=d * 0.2)
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.25) for f in feats], lag_ratio=0.35), run_time=d * 0.6)
        self.clear_stage()

    # ------------------------------------------------------------
    # 4. Le lien : push / pull
    # ------------------------------------------------------------
    def part_link(self):
        self.set_chapter(2)

        cloud = Cloud(HUB_C, "GitHub", 28).scale(0.75).move_to(UP * 2.2)
        laptop = Laptop(GIT_C, 1.8, 1.15).move_to(DOWN * 0.7)
        git_lab = txt("Git", size=30, color=GIT_C, bold=True).move_to(laptop.screen)
        push = Arrow(laptop.get_top() + LEFT * 0.5 + UP * 0.1, cloud.get_bottom() + LEFT * 0.5 + DOWN * 0.15,
                     buff=0, color=GREEN, stroke_width=7)
        pull = Arrow(cloud.get_bottom() + RIGHT * 0.5 + DOWN * 0.15, laptop.get_top() + RIGHT * 0.5 + UP * 0.1,
                     buff=0, color=YELLOW, stroke_width=7)
        push_l = txt("git push", size=19, color=GREEN, bold=True, mono=True).next_to(push, LEFT, buff=0.12)
        pull_l = txt("git pull", size=19, color=YELLOW, bold=True, mono=True).next_to(pull, RIGHT, buff=0.12)

        with self.say(S.LINK_1) as tr:
            d = tr.duration
            self.play(FadeIn(cloud, shift=DOWN * 0.3), FadeIn(laptop, shift=UP * 0.3), FadeIn(git_lab), run_time=d * 0.3)
            self.play(GrowArrow(push), Write(push_l), run_time=d * 0.25)
            self.play(GrowArrow(pull), Write(pull_l), run_time=d * 0.25)

        up_dot = Dot(radius=0.13, color=GREEN).move_to(push.get_start())
        down_dot = Dot(radius=0.13, color=YELLOW).move_to(pull.get_start())
        with self.say(S.LINK_2) as tr:
            d = tr.duration
            self.add(up_dot)
            self.play(up_dot.animate.move_to(push.get_end()), run_time=d * 0.3, rate_func=smooth)
            self.play(Indicate(cloud, color=GREEN, scale_factor=1.08), FadeOut(up_dot), run_time=d * 0.2)
            self.add(down_dot)
            self.play(down_dot.animate.move_to(pull.get_end()), run_time=d * 0.3, rate_func=smooth)
            self.play(Indicate(laptop, color=YELLOW, scale_factor=1.08), FadeOut(down_dot), run_time=d * 0.2)

        # --- Git fonctionne sans GitHub
        self.play(*[FadeOut(m) for m in (cloud, push, pull, push_l, pull_l)], run_time=0.4)
        group = VGroup(laptop, git_lab)
        others = VGroup(
            Pill("GitHub", HUB_C, size=24),
            Pill("GitLab", GITLAB_C, size=24),
            Pill("Bitbucket", BITB_C, size=24),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 0.45)
        intro_t = txt("Git fonctionne aussi avec :", size=22, color=MUTED).move_to(UP * 1.0)
        with self.say(S.LINK_3) as tr:
            d = tr.duration
            self.play(group.animate.scale(0.7).move_to(UP * 2.4), run_time=d * 0.2)
            self.play(FadeIn(intro_t), run_time=d * 0.15)
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in others], lag_ratio=0.35), run_time=d * 0.55)
        self.clear_stage()

    # ------------------------------------------------------------
    # 5. Bilan
    # ------------------------------------------------------------
    def part_recap(self):
        self.set_chapter(3)

        def card(title, sub, color, icon):
            box = RoundedRectangle(corner_radius=0.2, width=1.95, height=2.6,
                                   stroke_color=color, stroke_width=4, fill_color=PANEL, fill_opacity=1)
            icon.move_to(box.get_top() + DOWN * 0.8)
            t = txt(title, size=30, color=color, bold=True).move_to(box.get_center() + DOWN * 0.2)
            s = txt(sub, size=20, color=TEXT_C).next_to(t, DOWN, buff=0.2)
            if s.width > 1.7:
                s.scale_to_fit_width(1.7)
            return VGroup(box, icon, t, s)

        c1 = card("Git", "L'outil", GIT_C, Laptop(GIT_C, 0.9, 0.6))
        c2 = card("GitHub", "La plateforme", HUB_C, Cloud(HUB_C, "", 10).scale(0.45))
        cards = VGroup(c1, c2).arrange(RIGHT, buff=0.2).move_to(UP * 0.5)

        with self.say(S.RECAP) as tr:
            d = tr.duration
            self.play(FadeIn(c1, shift=RIGHT * 0.3), run_time=d * 0.3)
            self.play(FadeIn(c2, shift=LEFT * 0.3), run_time=d * 0.3)
            self.play(Indicate(c1, color=GIT_C), Indicate(c2, color=HUB_C), run_time=d * 0.3)
        self.clear_stage()

    # ------------------------------------------------------------
    # 6. Conclusion
    # ------------------------------------------------------------
    def outro(self):
        self.play(FadeOut(self.chips), run_time=0.3)
        name = txt("Dev_Web", size=64, color=YELLOW, bold=True).move_to(UP * 1.3)
        handle = txt("@devops_web", size=36, color=TEXT_C).next_to(name, DOWN, buff=0.25)
        cta = Pill("Abonne-toi", GIT_C, size=30, filled=True).next_to(handle, DOWN, buff=0.5)
        with self.say(S.OUTRO) as tr:
            d = tr.duration
            self.play(FadeIn(name, shift=UP * 0.3), FadeIn(handle, shift=UP * 0.2), run_time=d * 0.4)
            self.play(GrowFromCenter(cta), run_time=d * 0.25)
            self.play(Indicate(cta, scale_factor=1.15), run_time=d * 0.25)
        self.wait(1)
