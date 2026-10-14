"""
music_theory.py - Guitar fretboard music theory, notes mapping, tuning and challenge logic.
Supports open strings (Nut / Casa 0) inclusion, EADGBE string order, and multi-position tracking.
"""

import random

# Standard Guitar Tuning (String 6 = Low E on TOP, String 1 = High E on BOTTOM)
# Top to bottom: E (6), A (5), D (4), G (3), B (2), E (1)
OPEN_STRING_MIDI = {
    6: 40,  # 6ª corda - E2 (Grave / Bordão - Topo)
    5: 45,  # 5ª corda - A2
    4: 50,  # 4ª corda - D3
    3: 55,  # 3ª corda - G3
    2: 59,  # 2ª corda - B3
    1: 64,  # 1ª corda - E4 (Agudo - Inferior)
}

STRING_NAMES_PT = {
    6: "6ª Corda (Mi / E - Bordão)",
    5: "5ª Corda (Lá / A)",
    4: "4ª Corda (Ré / D)",
    3: "3ª Corda (Sol / G)",
    2: "2ª Corda (Si / B)",
    1: "1ª Corda (Mi / E - Aguda)",
}

NOTE_NAMES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_NAMES_FLAT  = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

NOTE_NAMES_SOLFEGE_SHARP = ["Dó", "Dó#", "Ré", "Ré#", "Mi", "Fá", "Fá#", "Sol", "Sol#", "Lá", "Lá#", "Si"]
NOTE_NAMES_SOLFEGE_FLAT  = ["Dó", "Réb", "Ré", "Mib", "Mi", "Fá", "Solb", "Sol", "Láb", "Lá", "Sib", "Si"]

NATURAL_SEMITONES = {0, 2, 4, 5, 7, 9, 11}  # C, D, E, F, G, A, B

class FretboardTheory:
    @staticmethod
    def midi_to_semitone(midi_pitch: int) -> int:
        return midi_pitch % 12

    @staticmethod
    def get_pitch(string_num: int, fret: int) -> int:
        return OPEN_STRING_MIDI[string_num] + fret

    @classmethod
    def get_note_display(cls, semitone: int, notation: str = "cifra", accident_pref: str = "sharp") -> str:
        idx = semitone % 12
        if notation == "solfejo":
            return NOTE_NAMES_SOLFEGE_SHARP[idx] if accident_pref == "sharp" else NOTE_NAMES_SOLFEGE_FLAT[idx]
        else:
            return NOTE_NAMES_SHARP[idx] if accident_pref == "sharp" else NOTE_NAMES_FLAT[idx]

    @classmethod
    def get_full_note_label(cls, semitone: int) -> str:
        idx = semitone % 12
        sharp_cifra = NOTE_NAMES_SHARP[idx]
        flat_cifra = NOTE_NAMES_FLAT[idx]
        sharp_solf = NOTE_NAMES_SOLFEGE_SHARP[idx]
        flat_solf = NOTE_NAMES_SOLFEGE_FLAT[idx]
        
        if idx in NATURAL_SEMITONES:
            return f"{sharp_cifra} ({sharp_solf})"
        else:
            return f"{sharp_cifra}/{flat_cifra} ({sharp_solf}/{flat_solf})"

    @classmethod
    def get_note_info(cls, string_num: int, fret: int) -> dict:
        pitch = cls.get_pitch(string_num, fret)
        semitone = cls.midi_to_semitone(pitch)
        is_natural = semitone in NATURAL_SEMITONES
        octave = (pitch // 12) - 1
        return {
            "string": string_num,
            "fret": fret,
            "midi": pitch,
            "semitone": semitone,
            "is_natural": is_natural,
            "octave": octave,
            "cifra_sharp": NOTE_NAMES_SHARP[semitone],
            "cifra_flat": NOTE_NAMES_FLAT[semitone],
            "solfejo_sharp": NOTE_NAMES_SOLFEGE_SHARP[semitone],
            "solfejo_flat": NOTE_NAMES_SOLFEGE_FLAT[semitone],
            "full_label": cls.get_full_note_label(semitone)
        }

    @classmethod
    def get_all_notes_in_region(cls, start_fret: int, end_fret: int, natural_only: bool = True, include_open_strings: bool = True) -> list[int]:
        found = set()
        # Frets in region
        fret_range = list(range(start_fret, end_fret + 1))
        if include_open_strings and 0 not in fret_range:
            fret_range.append(0)

        for s in range(1, 7):
            for f in fret_range:
                p = cls.get_pitch(s, f)
                semi = cls.midi_to_semitone(p)
                if not natural_only or (semi in NATURAL_SEMITONES):
                    found.add(semi)
        return sorted(list(found))

    @classmethod
    def find_positions_for_semitone(cls, semitone: int, start_fret: int, end_fret: int, include_open_strings: bool = True) -> list[tuple[int, int]]:
        positions = []
        fret_range = list(range(start_fret, end_fret + 1))
        if include_open_strings and 0 not in fret_range:
            fret_range.append(0)

        for s in range(1, 7):
            for f in fret_range:
                p = cls.get_pitch(s, f)
                if cls.midi_to_semitone(p) == semitone:
                    positions.append((s, f))
        return positions

    @classmethod
    def generate_challenge(
        cls,
        start_fret: int,
        end_fret: int,
        natural_only: bool = True,
        include_open_strings: bool = True,
        previous_semitone: int | None = None
    ) -> dict:
        available = cls.get_all_notes_in_region(start_fret, end_fret, natural_only, include_open_strings)
        if not available:
            available = [0, 2, 4, 5, 7, 9, 11]
            
        choices = [s for s in available if s != previous_semitone]
        if not choices:
            choices = available
            
        target_semitone = random.choice(choices)
        valid_positions = cls.find_positions_for_semitone(target_semitone, start_fret, end_fret, include_open_strings)
        
        return {
            "semitone": target_semitone,
            "cifra_sharp": NOTE_NAMES_SHARP[target_semitone],
            "cifra_flat": NOTE_NAMES_FLAT[target_semitone],
            "solfejo_sharp": NOTE_NAMES_SOLFEGE_SHARP[target_semitone],
            "solfejo_flat": NOTE_NAMES_SOLFEGE_FLAT[target_semitone],
            "full_label": cls.get_full_note_label(target_semitone),
            "is_natural": target_semitone in NATURAL_SEMITONES,
            "valid_positions": set(valid_positions),  # set of (string, fret)
            "num_positions": len(valid_positions),
            "start_fret": start_fret,
            "end_fret": end_fret,
            "include_open_strings": include_open_strings
        }
