"""
app.py - Standalone Guitar Fretboard Trainer (Treinador de Braço de Guitarra)
Supports Destro (default) & Canhoto (left-handed) orientations,
accidentals (#) enabled by default, perspective explanation banner,
interval study toggle, white background, Nut mapping, and compact badges.
"""

import os
import sys
import time
import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk

from music_theory import FretboardTheory, STRING_NAMES_PT
from fretboard_renderer import FretboardRenderer

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class GuitarTrainerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Guitar Fretboard Trainer • Treinador de Notas na Guitarra (Até 12ª Casa)")
        self.geometry("1280x890")
        self.minsize(1050, 740)

        # Base directories
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.base_dir, "assets")

        # Initialize renderer
        self.renderer = FretboardRenderer(self.assets_dir)

        # App Configuration
        self.hand_orientation = "destro"  # "destro" (default) or "canhoto"
        self.max_fret = 12
        self.start_fret = 1
        self.end_fret = 5
        self.include_open_strings = True
        self.include_accidentals = True   # DEFAULT: Acidentes (#) e Naturais habilitados!
        self.notation = "cifra"
        self.show_interval_notes = False

        # Challenge State
        self.current_challenge = None
        self.valid_positions = set()
        self.found_positions = set()
        self.challenge_start_time = 0.0
        self.target_revealed = False

        # Visual Feedback & Ripple Animation
        self.hover_pos = None
        self.last_clicked_pos = None
        self.last_click_is_correct = None
        self.last_clicked_note_label = ""
        self.hitboxes = {}
        self.canvas_img_tk = None
        self._after_advance_id = None

        self.ripple_pos = None
        self.ripple_progress = 0.0
        self._ripple_anim_id = None

        # Statistics
        self.total_hits = 0
        self.total_errors = 0
        self.reaction_times = []
        self.current_streak = 0
        self.best_streak = 0

        # Build UI
        self._build_ui()

        # Canvas bindings
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<Leave>", self._on_mouse_leave)
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # Start timer tick loop
        self._tick_timer()

        # Start first challenge immediately
        self._next_challenge()

    def _build_ui(self):
        self.configure(fg_color="#0f172a")

        # 1. TOP HEADER BAR
        header_frame = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=0, height=56)
        header_frame.pack(side="top", fill="x", padx=0, pady=0)

        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left", padx=20, pady=8)

        title_lbl = ctk.CTkLabel(
            title_box,
            text="🎸 GUITAR FRETBOARD TRAINER",
            font=ctk.CTkFont(family="Segoe UI", size=19, weight="bold"),
            text_color="#38bdf8"
        )
        title_lbl.pack(side="left")

        self.sub_title_lbl = ctk.CTkLabel(
            title_box,
            text="  |  Perspectiva Real de Quem Toca (Destro • E A D G B E)",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#94a3b8"
        )
        self.sub_title_lbl.pack(side="left")

        top_controls = ctk.CTkFrame(header_frame, fg_color="transparent")
        top_controls.pack(side="right", padx=20, pady=8)

        # Orientation Toggle (Destro / Canhoto)
        self.orientation_btn = ctk.CTkSegmentedButton(
            top_controls,
            values=["🎸 Destro (Padrão)", "🎸 Canhoto"],
            command=self._on_orientation_change,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            selected_color="#0284c7"
        )
        self.orientation_btn.set("🎸 Destro (Padrão)")
        self.orientation_btn.pack(side="left", padx=8)

        # Notation Toggle
        self.notation_btn = ctk.CTkSegmentedButton(
            top_controls,
            values=["Cifra (C, D, E)", "Solfejo (Dó, Ré)"],
            command=self._on_notation_change,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            selected_color="#0284c7"
        )
        self.notation_btn.set("Cifra (C, D, E)")
        self.notation_btn.pack(side="left", padx=8)

        # 2. PERSPECTIVE INFORMATIVE BANNER
        banner_frame = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=8, border_width=1, border_color="#334155")
        banner_frame.pack(side="top", fill="x", padx=20, pady=(8, 4))

        banner_text = (
            "ℹ️ Perspectiva do Instrumentista: A posição das notas equivale exatamente à posição real em que tocamos (visão do instrumento em mãos). "
            "A imagem é uma representação da visão traseira do braço da guitarra, adaptada com transparência para tornar a escala e as cordas visíveis através do braço."
        )
        ctk.CTkLabel(
            banner_frame,
            text=banner_text,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#cbd5e1",
            wraplength=1200,
            justify="left"
        ).pack(side="left", padx=12, pady=6)

        # 3. CHALLENGE HERO CARD
        self.hero_frame = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=12, border_width=1, border_color="#334155")
        self.hero_frame.pack(side="top", fill="x", padx=20, pady=(6, 4))

        hero_left = ctk.CTkFrame(self.hero_frame, fg_color="transparent")
        hero_left.pack(side="left", fill="both", expand=True, padx=22, pady=8)

        self.prompt_label = ctk.CTkLabel(
            hero_left,
            text="ENCONTRE TODAS AS OCORRÊNCIAS DA NOTA:",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#94a3b8"
        )
        self.prompt_label.pack(anchor="w")

        target_container = ctk.CTkFrame(hero_left, fg_color="transparent")
        target_container.pack(anchor="w", pady=(1, 2))

        self.target_note_display = ctk.CTkLabel(
            target_container,
            text="C",
            font=ctk.CTkFont(family="Segoe UI", size=34, weight="bold"),
            text_color="#38bdf8"
        )
        self.target_note_display.pack(side="left")

        self.target_subnote_display = ctk.CTkLabel(
            target_container,
            text="  (Dó)",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="normal"),
            text_color="#94a3b8"
        )
        self.target_subnote_display.pack(side="left", padx=4)

        self.progress_badge = ctk.CTkLabel(
            target_container,
            text="🎯 0 de 2 encontradas",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#f59e0b",
            fg_color="#0f172a",
            corner_radius=8,
            padx=12,
            pady=3
        )
        self.progress_badge.pack(side="left", padx=16)

        self.instruction_subtext = ctk.CTkLabel(
            hero_left,
            text="Clique nas cordas (inclusive no Nut / cordas soltas) que possuem esta nota no intervalo!",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#cbd5e1"
        )
        self.instruction_subtext.pack(anchor="w")

        # Middle: Timer & Streak
        hero_middle = ctk.CTkFrame(self.hero_frame, fg_color="#0f172a", corner_radius=10, width=180)
        hero_middle.pack(side="left", padx=15, pady=8, fill="y")

        ctk.CTkLabel(
            hero_middle,
            text="TEMPO DA NOTA",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#64748b"
        ).pack(pady=(5, 0))

        self.live_timer_lbl = ctk.CTkLabel(
            hero_middle,
            text="0.0s",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#fbbf24"
        )
        self.live_timer_lbl.pack(pady=(0, 2))

        self.streak_badge_lbl = ctk.CTkLabel(
            hero_middle,
            text="🔥 Sequência: 0",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#f97316"
        )
        self.streak_badge_lbl.pack(pady=(0, 5))

        # Right: Action Buttons (Dica / Pular)
        hero_right = ctk.CTkFrame(self.hero_frame, fg_color="transparent")
        hero_right.pack(side="right", padx=20, pady=8)

        self.hint_btn = ctk.CTkButton(
            hero_right,
            text="💡 Revelar Posições",
            width=140,
            command=self._reveal_hint,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.hint_btn.pack(pady=3)

        self.skip_btn = ctk.CTkButton(
            hero_right,
            text="⏭️ Pular Nota",
            width=140,
            command=self._next_challenge,
            fg_color="#1e293b",
            border_width=1,
            border_color="#475569",
            hover_color="#334155",
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.skip_btn.pack(pady=3)

        # 4. INTERACTIVE FRETBOARD CANVAS (WHITE BACKGROUND)
        canvas_wrapper = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=12, border_width=1, border_color="#cbd5e1")
        canvas_wrapper.pack(side="top", fill="both", expand=True, padx=20, pady=6)

        self.canvas = tk.Canvas(
            canvas_wrapper,
            bg="#ffffff",
            highlightthickness=0,
            cursor="hand2"
        )
        self.canvas.pack(fill="both", expand=True, padx=4, pady=4)

        # 5. STATS METRICS BAR
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(side="top", fill="x", padx=20, pady=(4, 6))
        stats_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.card_avg_time = self._create_stat_card(stats_frame, 0, "⏱️ TEMPO MÉDIO", "-- s", "#38bdf8")
        self.card_hits = self._create_stat_card(stats_frame, 1, "✅ ACERTOS", "0", "#10b981")
        self.card_errors = self._create_stat_card(stats_frame, 2, "❌ ERROS", "0", "#ef4444")
        self.card_acc = self._create_stat_card(stats_frame, 3, "🎯 PRECISÃO", "100%", "#a855f7")
        self.card_best_streak = self._create_stat_card(stats_frame, 4, "🏆 RECORDE", "0", "#f59e0b")

        # 6. REGION SELECTION & CONTROL DRAWER
        controls_frame = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=12, border_width=1, border_color="#334155")
        controls_frame.pack(side="bottom", fill="x", padx=20, pady=(0, 10))

        # Row 1: Quick Region Presets & Sliders
        row1 = ctk.CTkFrame(controls_frame, fg_color="transparent")
        row1.pack(fill="x", padx=15, pady=(8, 4))

        ctk.CTkLabel(
            row1,
            text="📍 Região das Casas:",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#f1f5f9"
        ).pack(side="left", padx=(0, 10))

        presets = [
            ("1ª à 5ª", 1, 5),
            ("5ª à 9ª", 5, 9),
            ("7ª à 12ª", 7, 12),
            ("1ª à 12ª", 1, 12),
            ("Braço Inteiro (0-12)", 0, 12),
        ]
        for name, sf, ef in presets:
            btn = ctk.CTkButton(
                row1,
                text=name,
                width=105,
                height=28,
                command=lambda s=sf, e=ef: self._set_region(s, e),
                fg_color="#334155",
                hover_color="#0284c7",
                font=ctk.CTkFont(family="Segoe UI", size=12)
            )
            btn.pack(side="left", padx=4)

        sliders_box = ctk.CTkFrame(row1, fg_color="transparent")
        sliders_box.pack(side="right", padx=5)

        self.lbl_start_fret = ctk.CTkLabel(sliders_box, text=f"De Casa: {self.start_fret}", width=75, text_color="#94a3b8")
        self.lbl_start_fret.pack(side="left", padx=2)

        self.slider_start = ctk.CTkSlider(
            sliders_box,
            from_=0,
            to=11,
            number_of_steps=11,
            width=100,
            command=self._on_start_slider_change
        )
        self.slider_start.set(self.start_fret)
        self.slider_start.pack(side="left", padx=4)

        self.lbl_end_fret = ctk.CTkLabel(sliders_box, text=f"Até Casa: {self.end_fret}", width=75, text_color="#94a3b8")
        self.lbl_end_fret.pack(side="left", padx=2)

        self.slider_end = ctk.CTkSlider(
            sliders_box,
            from_=1,
            to=12,
            number_of_steps=11,
            width=100,
            command=self._on_end_slider_change
        )
        self.slider_end.set(self.end_fret)
        self.slider_end.pack(side="left", padx=4)

        # Row 2: Switches & Study Buttons
        row2 = ctk.CTkFrame(controls_frame, fg_color="transparent")
        row2.pack(fill="x", padx=15, pady=(4, 8))

        # Open strings switch (Nut)
        self.open_strings_switch = ctk.CTkSwitch(
            row2,
            text="Nut / Cordas Soltas (0)",
            command=self._on_open_strings_toggle,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            progress_color="#0284c7"
        )
        self.open_strings_switch.select()
        self.open_strings_switch.pack(side="left", padx=8)

        # Accidentals switch (DEFAULT: CHECKED)
        self.accidental_switch = ctk.CTkSwitch(
            row2,
            text="Incluir Acidentes (#)",
            command=self._on_accidental_toggle,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            progress_color="#0284c7"
        )
        self.accidental_switch.select()  # Checked by default!
        self.accidental_switch.pack(side="left", padx=10)

        # Exibir Todas as Notas do Intervalo
        self.interval_notes_btn = ctk.CTkButton(
            row2,
            text="👁️ Exibir Notas do Intervalo",
            width=190,
            command=self._toggle_interval_notes,
            fg_color="#334155",
            hover_color="#0284c7",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        )
        self.interval_notes_btn.pack(side="left", padx=8)

        # Reset Stats
        self.reset_stats_btn = ctk.CTkButton(
            row2,
            text="🔄 Zerar Métricas",
            width=120,
            command=self._reset_stats,
            fg_color="#1e293b",
            hover_color="#dc2626",
            border_width=1,
            border_color="#475569",
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.reset_stats_btn.pack(side="right", padx=4)

    def _create_stat_card(self, parent, col, title, initial_val, val_color):
        card = ctk.CTkFrame(parent, fg_color="#1e293b", corner_radius=10, border_width=1, border_color="#334155")
        card.grid(row=0, column=col, padx=4, pady=2, sticky="ew")

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#64748b"
        ).pack(pady=(5, 0))

        val_label = ctk.CTkLabel(
            card,
            text=initial_val,
            font=ctk.CTkFont(family="Segoe UI", size=19, weight="bold"),
            text_color=val_color
        )
        val_label.pack(pady=(0, 5))
        return val_label

    def _on_orientation_change(self, val):
        self.hand_orientation = "canhoto" if "Canhoto" in val else "destro"
        orient_txt = "Canhoto" if self.hand_orientation == "canhoto" else "Destro"
        self.sub_title_lbl.configure(text=f"  |  Perspectiva Real de Quem Toca ({orient_txt} • E A D G B E)")
        self._update_challenge_display()
        self._redraw_fretboard()

    def _set_region(self, sf: int, ef: int):
        self.start_fret = sf
        self.end_fret = ef
        self.slider_start.set(sf)
        self.slider_end.set(ef)
        self.lbl_start_fret.configure(text=f"De Casa: {sf}")
        self.lbl_end_fret.configure(text=f"Até Casa: {ef}")
        self._next_challenge()

    def _on_start_slider_change(self, val):
        sf = int(round(val))
        if sf >= self.end_fret:
            sf = max(0, self.end_fret - 1)
            self.slider_start.set(sf)
        self.start_fret = sf
        self.lbl_start_fret.configure(text=f"De Casa: {sf}")
        self._next_challenge()

    def _on_end_slider_change(self, val):
        ef = int(round(val))
        if ef <= self.start_fret:
            ef = min(self.max_fret, self.start_fret + 1)
            self.slider_end.set(ef)
        self.end_fret = ef
        self.lbl_end_fret.configure(text=f"Até Casa: {ef}")
        self._next_challenge()

    def _on_open_strings_toggle(self):
        self.include_open_strings = (self.open_strings_switch.get() == 1)
        self._next_challenge()

    def _on_accidental_toggle(self):
        self.include_accidentals = (self.accidental_switch.get() == 1)
        self._next_challenge()

    def _on_notation_change(self, val):
        self.notation = "solfejo" if "Solfejo" in val else "cifra"
        self._update_challenge_display()
        self._redraw_fretboard()

    def _toggle_interval_notes(self):
        self.show_interval_notes = not self.show_interval_notes
        if self.show_interval_notes:
            self.interval_notes_btn.configure(
                text="👁️ Ocultar Notas do Intervalo",
                fg_color="#0284c7"
            )
        else:
            self.interval_notes_btn.configure(
                text="👁️ Exibir Notas do Intervalo",
                fg_color="#334155"
            )
        self._redraw_fretboard()

    def _update_challenge_display(self):
        if not self.current_challenge:
            return
        c = self.current_challenge
        if self.notation == "solfejo":
            main_text = c["solfejo_sharp"]
            sub_text = f"  ({c['cifra_sharp']})"
        else:
            main_text = c["cifra_sharp"]
            sub_text = f"  ({c['solfejo_sharp']})"

        self.target_note_display.configure(text=main_text)
        self.target_subnote_display.configure(text=sub_text)

        total_needed = len(self.valid_positions)
        found_count = len(self.found_positions)
        self.progress_badge.configure(
            text=f"🎯 {found_count} de {total_needed} encontradas",
            text_color="#10b981" if found_count == total_needed else "#f59e0b"
        )

        reg_str = f"Casas {self.start_fret} à {self.end_fret}"
        if self.include_open_strings:
            reg_str += " + Nut (Soltas)"

        orient_desc = " [Canhoto]" if self.hand_orientation == "canhoto" else ""
        if total_needed > 1:
            self.instruction_subtext.configure(
                text=f"Existem {total_needed} ocorrências de {main_text} em {reg_str}{orient_desc}. Clique em todas para avançar!"
            )
        else:
            self.instruction_subtext.configure(
                text=f"Existe 1 ocorrência de {main_text} em {reg_str}{orient_desc}. Clique nela para avançar!"
            )

    def _next_challenge(self):
        if self._after_advance_id:
            self.after_cancel(self._after_advance_id)
            self._after_advance_id = None
        if self._ripple_anim_id:
            self.after_cancel(self._ripple_anim_id)
            self._ripple_anim_id = None

        self.ripple_pos = None
        self.ripple_progress = 0.0

        prev_semi = self.current_challenge["semitone"] if self.current_challenge else None
        self.current_challenge = FretboardTheory.generate_challenge(
            self.start_fret,
            self.end_fret,
            natural_only=(not self.include_accidentals),
            include_open_strings=self.include_open_strings,
            previous_semitone=prev_semi
        )
        self.valid_positions = set(self.current_challenge["valid_positions"])
        self.found_positions = set()
        self.challenge_start_time = time.perf_counter()
        self.target_revealed = False
        self.last_clicked_pos = None
        self.last_click_is_correct = None
        self.last_clicked_note_label = ""

        self.prompt_label.configure(text="ENCONTRE TODAS AS OCORRÊNCIAS DA NOTA:", text_color="#94a3b8")
        self._update_challenge_display()
        self._redraw_fretboard()

    def _reveal_hint(self):
        if not self.current_challenge:
            return
        self.target_revealed = True
        self.prompt_label.configure(text="DICA: POSIÇÕES DESTACADAS NO BRAÇO:", text_color="#f59e0b")
        self._redraw_fretboard()

    def _on_canvas_resize(self, event):
        self._redraw_fretboard()

    def _animate_ripple(self):
        if self.ripple_progress < 1.0:
            self.ripple_progress += 0.2
            self._redraw_fretboard()
            self._ripple_anim_id = self.after(40, self._animate_ripple)
        else:
            self.ripple_progress = 0.0
            self.ripple_pos = None
            self._redraw_fretboard()

    def _redraw_fretboard(self):
        w = max(400, self.canvas.winfo_width())
        h = max(180, self.canvas.winfo_height())

        targets = None
        if self.target_revealed and self.current_challenge:
            targets = self.valid_positions

        interval_notes_info = None
        if self.show_interval_notes:
            interval_notes_info = {}
            fret_list = list(range(self.start_fret, self.end_fret + 1))
            if self.include_open_strings and 0 not in fret_list:
                fret_list.append(0)

            for s in range(1, 7):
                for f in fret_list:
                    info = FretboardTheory.get_note_info(s, f)
                    if self.include_accidentals or info["is_natural"]:
                        lbl = info["solfejo_sharp"] if self.notation == "solfejo" else info["cifra_sharp"]
                        interval_notes_info[(s, f)] = lbl

        active_label = ""
        if self.current_challenge:
            active_label = self.current_challenge["solfejo_sharp"] if self.notation == "solfejo" else self.current_challenge["cifra_sharp"]

        img, self.hitboxes = self.renderer.render(
            width=w,
            height=h,
            start_fret=self.start_fret,
            end_fret=self.end_fret,
            include_open_strings=self.include_open_strings,
            hand_orientation=self.hand_orientation,
            hover_pos=self.hover_pos,
            target_positions=targets,
            found_positions=self.found_positions,
            last_clicked_pos=self.last_clicked_pos,
            last_click_is_correct=self.last_click_is_correct,
            last_clicked_note_label=active_label if self.last_click_is_correct else self.last_clicked_note_label,
            ripple_progress=self.ripple_progress,
            ripple_pos=self.ripple_pos,
            show_interval_notes=self.show_interval_notes,
            interval_notes_info=interval_notes_info,
            max_fret=self.max_fret
        )

        self.canvas_img_tk = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.canvas_img_tk, anchor="nw")

    def _find_hit_at_coords(self, x: int, y: int) -> tuple[int, int] | None:
        for (s, f), (x1, y1, x2, y2) in self.hitboxes.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                return (s, f)
        return None

    def _on_mouse_move(self, event):
        hit = self._find_hit_at_coords(event.x, event.y)
        if hit != self.hover_pos:
            self.hover_pos = hit
            self._redraw_fretboard()

    def _on_mouse_leave(self, event):
        if self.hover_pos is not None:
            self.hover_pos = None
            self._redraw_fretboard()

    def _on_canvas_click(self, event):
        hit = self._find_hit_at_coords(event.x, event.y)
        if not hit:
            return

        s_num, fret_num = hit
        note_info = FretboardTheory.get_note_info(s_num, fret_num)
        clicked_semi = note_info["semitone"]
        clicked_label = note_info["solfejo_sharp"] if self.notation == "solfejo" else note_info["cifra_sharp"]

        if not self.current_challenge:
            return

        target_semi = self.current_challenge["semitone"]
        target_name = self.current_challenge["solfejo_sharp"] if self.notation == "solfejo" else self.current_challenge["cifra_sharp"]
        elapsed = time.perf_counter() - self.challenge_start_time

        if hit in self.valid_positions:
            if hit in self.found_positions:
                self.prompt_label.configure(
                    text=f"ℹ️ Você já encontrou esta posição de {target_name}! Procure as outras no intervalo.",
                    text_color="#38bdf8"
                )
                return

            # === VALID POSITION FOUND ===
            self.found_positions.add(hit)
            self.total_hits += 1
            self.last_clicked_pos = hit
            self.last_click_is_correct = True
            self.last_clicked_note_label = clicked_label

            self.ripple_pos = hit
            self.ripple_progress = 0.1
            self._animate_ripple()

            total_needed = len(self.valid_positions)
            found_count = len(self.found_positions)
            remaining = total_needed - found_count
            loc_desc = "Nut (Corda Solta)" if fret_num == 0 else f"Casa {fret_num}"

            if remaining == 0:
                self.reaction_times.append(elapsed)
                self.current_streak += 1
                if self.current_streak > self.best_streak:
                    self.best_streak = self.current_streak

                self.prompt_label.configure(
                    text=f"🎉 PERFEITO! Encontrou todas as {total_needed} ocorrências de {target_name} em {elapsed:.2f}s!",
                    text_color="#10b981"
                )
                self._update_stats_display()
                self._update_challenge_display()
                self._redraw_fretboard()

                self._after_advance_id = self.after(750, self._next_challenge)

            else:
                self.prompt_label.configure(
                    text=f"✨ Acertou em {loc_desc}! Resta(m) {remaining} de {target_name} no intervalo.",
                    text_color="#38bdf8"
                )
                self._update_stats_display()
                self._update_challenge_display()
                self._redraw_fretboard()

        else:
            # === INCORRECT HIT ===
            self.total_errors += 1
            self.current_streak = 0
            self.last_clicked_pos = hit
            self.last_click_is_correct = False
            self.last_clicked_note_label = clicked_label

            string_name = STRING_NAMES_PT.get(s_num, f"{s_num}ª corda")
            fret_name = "Nut (Corda Solta)" if fret_num == 0 else f"Casa {fret_num}"
            is_in_active_range = (self.start_fret <= fret_num <= self.end_fret) or (fret_num == 0 and self.include_open_strings)

            if not is_in_active_range and clicked_semi == target_semi:
                msg = f"⚠️ Essa é a nota {target_name}, mas está fora da região ativa! (Estava na {fret_name})"
            else:
                msg = f"❌ Ops! Você clicou em {clicked_label} ({string_name}, {fret_name}). Continue procurando {target_name}!"

            self.prompt_label.configure(text=msg, text_color="#ef4444")
            self._update_stats_display()
            self._redraw_fretboard()

    def _update_stats_display(self):
        self.card_hits.configure(text=str(self.total_hits))
        self.card_errors.configure(text=str(self.total_errors))

        total_attempts = self.total_hits + self.total_errors
        if total_attempts > 0:
            acc = (self.total_hits / total_attempts) * 100.0
            self.card_acc.configure(text=f"{acc:.1f}%")
        else:
            self.card_acc.configure(text="100%")

        if self.reaction_times:
            avg_t = sum(self.reaction_times) / len(self.reaction_times)
            self.card_avg_time.configure(text=f"{avg_t:.2f}s")
        else:
            self.card_avg_time.configure(text="-- s")

        self.card_best_streak.configure(text=str(self.best_streak))
        self.streak_badge_lbl.configure(text=f"🔥 Sequência: {self.current_streak}")

    def _reset_stats(self):
        self.total_hits = 0
        self.total_errors = 0
        self.reaction_times.clear()
        self.current_streak = 0
        self.best_streak = 0
        self._update_stats_display()
        self.prompt_label.configure(text="Métricas zeradas! Pronto para recomeçar.", text_color="#38bdf8")

    def _tick_timer(self):
        if self.challenge_start_time > 0 and len(self.found_positions) < len(self.valid_positions):
            cur_elapsed = time.perf_counter() - self.challenge_start_time
            self.live_timer_lbl.configure(text=f"{cur_elapsed:.1f}s")
        self.after(100, self._tick_timer)

if __name__ == "__main__":
    app = GuitarTrainerApp()
    app.mainloop()
