"""
fretboard_renderer.py - Fretboard renderer with transparency wash on unselected regions,
no blue boundary lines, study mode to show all notes in the active interval,
compact note badges, and pure white background.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

class FretboardRenderer:
    def __init__(self, assets_dir: str):
        self.assets_dir = assets_dir
        self.white_bg_neck_path = os.path.join(assets_dir, "guitar_neck_white_bg.jpg")
        
        # Crop parameters in original image (1024 x 764):
        self.orig_crop_box = (15, 285, 785, 465)
        self.crop_w = self.orig_crop_box[2] - self.orig_crop_box[0]  # 770
        self.crop_h = self.orig_crop_box[3] - self.orig_crop_box[1]  # 180

        # Exact Fret wire X coordinates:
        self.raw_frets = {
            0: 292,   # Nut boundary into fret 1
            1: 341,
            2: 395,
            3: 442,
            4: 487,
            5: 530,
            6: 570,
            7: 608,
            8: 644,
            9: 676,
            10: 708,
            11: 740,
            12: 771   # 12th fret
        }

        self.nut_raw_x_start = 220
        self.nut_raw_x_end = 292

        # String Y positions (Top to bottom: 6=Low E, 5=A, 4=D, 3=G, 2=B, 1=High E)
        self.string_y_endpoints = {
            6: (353, 351),  # E (thickest wound, top)
            5: (364, 363),  # A
            4: (375, 376),  # D
            3: (386, 388),  # G
            2: (398, 401),  # B
            1: (410, 414),  # E (thinnest, bottom)
        }

        self.neck_y_bounds = (345, 420)

        self._base_cropped_image = None
        if os.path.exists(self.white_bg_neck_path):
            try:
                raw_img = Image.open(self.white_bg_neck_path).convert("RGBA")
                self._base_cropped_image = raw_img.crop(self.orig_crop_box)
            except Exception:
                self._base_cropped_image = None

    def get_string_y(self, s_num: int, x_raw: float) -> float:
        x0 = 289.0
        x1 = 771.0
        y0, y1 = self.string_y_endpoints[s_num]
        t = (x_raw - x0) / (x1 - x0)
        return y0 + t * (y1 - y0)

    def render(
        self,
        width: int,
        height: int,
        start_fret: int = 1,
        end_fret: int = 5,
        include_open_strings: bool = True,
        zoom_mode: bool = False,
        hover_pos: tuple[int, int] | None = None,           # (string, fret)
        target_positions: set[tuple[int, int]] | None = None,
        found_positions: set[tuple[int, int]] | None = None,
        last_clicked_pos: tuple[int, int] | None = None,
        last_click_is_correct: bool | None = None,
        last_clicked_note_label: str = "",
        ripple_progress: float = 0.0,
        ripple_pos: tuple[int, int] | None = None,
        show_interval_notes: bool = False,
        interval_notes_info: dict | None = None,           # maps (s, f) -> note label
        max_fret: int = 12
    ) -> tuple[Image.Image, dict[tuple[int, int], tuple[int, int, int, int]]]:
        """
        Renders fretboard with soft transparency on unselected areas (no blue lines),
        optional interval note study view, and compact badges.
        """
        img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)

        if not self._base_cropped_image:
            draw.text((width // 2, height // 2), "Imagem da guitarra não encontrada", fill=(0, 0, 0), anchor="mm")
            return img, {}

        # Determine horizontal cropping and zoom range
        if zoom_mode and (start_fret > 0 or end_fret < max_fret):
            f_min = max(0, start_fret)
            f_max = min(max_fret, end_fret)
            if f_max <= f_min:
                f_max = min(max_fret, f_min + 1)
            
            prev_f = max(0, f_min - 1) if f_min > 0 else 0
            x_left_raw = (self.nut_raw_x_start - 10) if f_min == 0 else (self.raw_frets[prev_f] - 10)
            x_right_raw = self.raw_frets[f_max] + 15
            
            sub_x1 = max(0, int(x_left_raw - self.orig_crop_box[0]))
            sub_x2 = min(self.crop_w, int(x_right_raw - self.orig_crop_box[0]))
            sub_img = self._base_cropped_image.crop((sub_x1, 0, sub_x2, self.crop_h))
            
            cur_crop_w = sub_x2 - sub_x1
            cur_offset_x = x_left_raw
            visible_frets = [f for f in range(max(0, f_min - 1), f_max + 1) if f in self.raw_frets]
        else:
            sub_img = self._base_cropped_image
            cur_crop_w = self.crop_w
            cur_offset_x = float(self.orig_crop_box[0])
            visible_frets = list(range(0, max_fret + 1))

        target_h = int(height * 0.74)
        scale = target_h / float(self.crop_h)
        target_w = int(cur_crop_w * scale)

        pad_x = max(10, (width - target_w) // 2)
        pad_y = max(10, (height - target_h) // 2)

        scaled_neck = sub_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        img.paste(scaled_neck, (pad_x, pad_y))

        def raw_to_canvas(raw_x: float, raw_y: float) -> tuple[int, int]:
            cx = pad_x + int((raw_x - cur_offset_x) * scale)
            cy = pad_y + int((raw_y - float(self.orig_crop_box[1])) * scale)
            return cx, cy

        # Compact fonts
        try:
            font_small = ImageFont.truetype("arial.ttf", 10)
            font_bold = ImageFont.truetype("arialbd.ttf", 11)
            font_badge = ImageFont.truetype("arialbd.ttf", 10)
        except Exception:
            font_small = ImageFont.load_default()
            font_bold = ImageFont.load_default()
            font_badge = ImageFont.load_default()

        # Build hitboxes
        hitboxes = {}
        for f in visible_frets:
            if f == 0:
                rx1 = float(self.nut_raw_x_start)
                rx2 = float(self.nut_raw_x_end)
            else:
                prev_f = f - 1
                rx1 = float(self.raw_frets[prev_f])
                rx2 = float(self.raw_frets[f])

            cx1, cy_top = raw_to_canvas(rx1, self.neck_y_bounds[0])
            cx2, cy_bot = raw_to_canvas(rx2, self.neck_y_bounds[1])
            cmid_x = (cx1 + cx2) // 2

            # Fret numbers text below fretboard (clean dark typography, no blue lines)
            if f > 0:
                is_active = (start_fret <= f <= end_fret)
                color = (15, 23, 42, 255) if is_active else (148, 163, 184, 180)
                font_to_use = font_bold if (f in {3, 5, 7, 9, 12} or is_active) else font_small
                draw.text((cmid_x, cy_bot + 12), str(f), fill=color, font=font_to_use, anchor="mt")

            mid_raw_x = (rx1 + rx2) / 2.0
            for s_num in range(1, 7):
                sy_raw = self.get_string_y(s_num, mid_raw_x)
                _, cy_str = raw_to_canvas(mid_raw_x, sy_raw)
                
                zone_h = max(16, int(12 * scale))
                y1 = cy_str - zone_h // 2
                y2 = cy_str + zone_h // 2
                hitboxes[(s_num, f)] = (cx1, y1, cx2, y2)

        # Nut Labels (clean text, no blue border)
        if 0 in visible_frets:
            nut_cx1, nut_cy_top = raw_to_canvas(self.nut_raw_x_start, self.neck_y_bounds[0])
            nut_cx2, nut_cy_bot = raw_to_canvas(self.nut_raw_x_end, self.neck_y_bounds[1])
            nut_mid_x = (nut_cx1 + nut_cx2) // 2

            nut_active = include_open_strings or (start_fret == 0)
            lbl_color = (15, 23, 42, 255) if nut_active else (148, 163, 184, 180)
            draw.text((nut_mid_x, nut_cy_bot + 12), "NUT (0)", fill=lbl_color, font=font_bold, anchor="mt")
            draw.text((nut_mid_x, nut_cy_top - 10), "Soltas", fill=lbl_color, font=font_bold, anchor="mb")

        # String Tuning Labels on Headstock
        tuning_labels = {6: "6ª E", 5: "5ª A", 4: "4ª D", 3: "3ª G", 2: "2ª B", 1: "1ª E"}
        for s_num in [6, 5, 4, 3, 2, 1]:
            if (s_num, 0) in hitboxes:
                hx1, _, _, _ = hitboxes[(s_num, 0)]
                sy_raw = self.get_string_y(s_num, float(self.nut_raw_x_start))
                _, cy_str = raw_to_canvas(float(self.nut_raw_x_start), sy_raw)
                draw.text((hx1 - 8, cy_str), tuning_labels[s_num], fill=(15, 23, 42, 240), font=font_bold, anchor="rm")

        # === TRANSPARENCY WASH ON UNSELECTED AREAS ONLY (NO BLUE LINES) ===
        if not zoom_mode:
            f_start = max(1, start_fret)
            f_end = min(max_fret, end_fret)

            # Neck Y bounds in canvas coordinates
            _, y_top_c = raw_to_canvas(self.nut_raw_x_start, self.neck_y_bounds[0])
            _, y_bot_c = raw_to_canvas(self.nut_raw_x_start, self.neck_y_bounds[1])
            neck_h_canvas = y_bot_c - y_top_c

            # 1. Unselected Nut / Open strings (if include_open_strings is False)
            if not include_open_strings and start_fret > 0:
                nut_x1_c, _ = raw_to_canvas(self.nut_raw_x_start, self.neck_y_bounds[0])
                nut_x2_c, _ = raw_to_canvas(self.nut_raw_x_end, self.neck_y_bounds[0])
                w_nut = nut_x2_c - nut_x1_c
                if w_nut > 0:
                    wash_nut = Image.new("RGBA", (w_nut, neck_h_canvas), (255, 255, 255, 175))
                    img.alpha_composite(wash_nut, (nut_cx1, y_top_c))

            # 2. Unselected frets to the LEFT of start_fret (between nut and start_fret)
            if f_start > 1:
                x_nut_end_c, _ = raw_to_canvas(self.raw_frets[0], self.neck_y_bounds[0])
                x_start_fret_c, _ = raw_to_canvas(self.raw_frets[f_start - 1], self.neck_y_bounds[0])
                wash_w_left = x_start_fret_c - x_nut_end_c
                if wash_w_left > 0:
                    wash_left = Image.new("RGBA", (wash_w_left, neck_h_canvas), (255, 255, 255, 175))
                    img.alpha_composite(wash_left, (x_nut_end_c, y_top_c))

            # 3. Unselected frets to the RIGHT of end_fret (from end_fret to 12th fret)
            if f_end < max_fret:
                x_end_fret_c, _ = raw_to_canvas(self.raw_frets[f_end], self.neck_y_bounds[0])
                x_f12_c, _ = raw_to_canvas(self.raw_frets[max_fret], self.neck_y_bounds[0])
                wash_w_right = x_f12_c - x_end_fret_c
                if wash_w_right > 0:
                    wash_right = Image.new("RGBA", (wash_w_right, neck_h_canvas), (255, 255, 255, 175))
                    img.alpha_composite(wash_right, (x_end_fret_c, y_top_c))

        # Badge radius
        badge_rad = max(7, int(8.5 * scale))

        # === STUDY MODE: SHOW ALL NOTES IN ACTIVE INTERVAL ===
        if show_interval_notes and interval_notes_info:
            for (s_num, f), label in interval_notes_info.items():
                if (s_num, f) in hitboxes:
                    # If this position is already found, the emerald badge below will render it
                    if found_positions and (s_num, f) in found_positions:
                        continue
                    bx1, by1, bx2, by2 = hitboxes[(s_num, f)]
                    cx = (bx1 + bx2) // 2
                    cy = (by1 + by2) // 2

                    # Elegant slate study badge
                    draw.ellipse([cx - badge_rad, cy - badge_rad, cx + badge_rad, cy + badge_rad], fill=(30, 41, 59, 230), outline=(71, 85, 105, 255), width=1)
                    draw.text((cx, cy), label, fill=(248, 250, 252, 255), font=font_badge, anchor="mm")

        # Target positions (Hints revealed via button)
        if target_positions:
            for (s_num, f) in target_positions:
                if (s_num, f) in hitboxes:
                    bx1, by1, bx2, by2 = hitboxes[(s_num, f)]
                    cx = (bx1 + bx2) // 2
                    cy = (by1 + by2) // 2
                    rad = max(7, int(8.0 * scale))
                    draw.ellipse([cx - rad - 3, cy - rad - 3, cx + rad + 3, cy + rad + 3], outline=(245, 158, 11, 100), width=1)
                    draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(245, 158, 11, 230), outline=(217, 119, 6, 255), width=2)
                    draw.text((cx, cy), "★", fill=(255, 255, 255, 255), font=font_small, anchor="mm")

        # === IDENTIFIED NOTES (COMPACT WITH LUMINOUS GLOW) ===
        if found_positions:
            for (s_num, f) in found_positions:
                if (s_num, f) in hitboxes:
                    bx1, by1, bx2, by2 = hitboxes[(s_num, f)]
                    cx = (bx1 + bx2) // 2
                    cy = (by1 + by2) // 2

                    # Luminous aura layers
                    draw.ellipse([cx - badge_rad - 6, cy - badge_rad - 6, cx + badge_rad + 6, cy + badge_rad + 6], outline=(52, 211, 153, 50), width=2)
                    draw.ellipse([cx - badge_rad - 3, cy - badge_rad - 3, cx + badge_rad + 3, cy + badge_rad + 3], outline=(16, 185, 129, 110), width=2)

                    # Jewel badge
                    draw.ellipse([cx - badge_rad, cy - badge_rad, cx + badge_rad, cy + badge_rad], fill=(5, 150, 105, 255), outline=(16, 185, 129, 255), width=2)
                    draw.arc([cx - badge_rad + 2, cy - badge_rad + 1, cx + badge_rad - 2, cy], start=180, end=360, fill=(209, 250, 229, 220), width=1)

                    note_txt = last_clicked_note_label or "✓"
                    draw.text((cx, cy), note_txt, fill=(255, 255, 255, 255), font=font_badge, anchor="mm")

        # Expanding Ripple Ring on Last Correct Hit
        if ripple_pos and ripple_progress > 0.0 and ripple_progress < 1.0:
            if ripple_pos in hitboxes:
                rx1, ry1, rx2, ry2 = hitboxes[ripple_pos]
                rcx = (rx1 + rx2) // 2
                rcy = (ry1 + ry2) // 2
                r_dist = int(badge_rad + (18.0 * ripple_progress))
                r_alpha = int(180 * (1.0 - ripple_progress))
                draw.ellipse([rcx - r_dist, rcy - r_dist, rcx + r_dist, rcy + r_dist], outline=(16, 185, 129, r_alpha), width=2)

        # Hover Halo
        if hover_pos and hover_pos in hitboxes:
            bx1, by1, bx2, by2 = hitboxes[hover_pos]
            cx = (bx1 + bx2) // 2
            cy = (by1 + by2) // 2
            h_rad = badge_rad + 2
            draw.ellipse([cx - h_rad, cy - h_rad, cx + h_rad, cy + h_rad], fill=(2, 132, 199, 40), outline=(2, 132, 199, 200), width=1)

        # Incorrect Click
        if last_clicked_pos and last_clicked_pos in hitboxes:
            if not last_click_is_correct:
                bx1, by1, bx2, by2 = hitboxes[last_clicked_pos]
                cx = (bx1 + bx2) // 2
                cy = (by1 + by2) // 2
                err_rad = badge_rad
                draw.ellipse([cx - err_rad - 3, cy - err_rad - 3, cx + err_rad + 3, cy + err_rad + 3], outline=(239, 68, 68, 90), width=2)
                draw.ellipse([cx - err_rad, cy - err_rad, cx + err_rad, cy + err_rad], fill=(220, 38, 38, 255), outline=(185, 28, 28, 255), width=2)
                draw.text((cx, cy), last_clicked_note_label or "✗", fill=(255, 255, 255, 255), font=font_badge, anchor="mm")

        return img, hitboxes
