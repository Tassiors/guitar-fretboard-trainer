"""
sound_engine.py - Realistic synthesized guitar audio playback for Windows.
Synthesizes plucked string guitar tones with natural harmonics and exponential decay,
caching WAV audio in memory and playing asynchronously using winsound.
"""

import math
import struct
import threading
import winsound

class GuitarSoundEngine:
    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate
        self.cache: dict[int, bytes] = {}
        self.enabled = True
        self._lock = threading.Lock()
        # Pre-cache common open string notes
        threading.Thread(target=self._precache_common, daemon=True).start()

    def _precache_common(self):
        # Pre-cache standard guitar notes (MIDI 40 to 88)
        for midi in range(40, 89):
            if midi not in self.cache:
                self.cache[midi] = self._synthesize_pluck(midi)

    def _synthesize_pluck(self, midi_pitch: int, duration: float = 0.65) -> bytes:
        freq = 440.0 * (2.0 ** ((midi_pitch - 69.0) / 12.0))
        n_samples = int(self.sample_rate * duration)
        raw_audio = bytearray()
        
        # Pluck parameters: rich guitar harmonics
        # Lower strings have more rich overtone presence
        for i in range(n_samples):
            t = float(i) / self.sample_rate
            # Realistic plucked decay: high harmonics decay faster
            env_fund = math.exp(-4.5 * t)
            env_h2 = math.exp(-7.0 * t)
            env_h3 = math.exp(-10.0 * t)
            env_h4 = math.exp(-14.0 * t)
            env_h5 = math.exp(-18.0 * t)
            
            s = (
                1.00 * math.sin(2.0 * math.pi * freq * t) * env_fund +
                0.55 * math.sin(2.0 * math.pi * 2.0 * freq * t) * env_h2 +
                0.28 * math.sin(2.0 * math.pi * 3.0 * freq * t) * env_h3 +
                0.15 * math.sin(2.0 * math.pi * 4.0 * freq * t) * env_h4 +
                0.08 * math.sin(2.0 * math.pi * 5.0 * freq * t) * env_h5
            )
            # Slight pluck attack transient at t < 0.005s
            if t < 0.005:
                s *= (t / 0.005)
                
            val = int(s * 13500)
            val = max(-32767, min(32767, val))
            raw_audio.extend(struct.pack('<h', val))
            
        byte_rate = self.sample_rate * 2
        block_align = 2
        wav_header = struct.pack(
            '<4sI4s4sIHHIIHH4sI',
            b'RIFF', 36 + len(raw_audio), b'WAVE',
            b'fmt ', 16, 1, 1, self.sample_rate, byte_rate, block_align, 16,
            b'data', len(raw_audio)
        )
        return wav_header + raw_audio

    def play_midi_pitch(self, midi_pitch: int):
        if not self.enabled:
            return
        
        def _play():
            try:
                with self._lock:
                    if midi_pitch not in self.cache:
                        self.cache[midi_pitch] = self._synthesize_pluck(midi_pitch)
                    wav_data = self.cache[midi_pitch]
                winsound.PlaySound(wav_data, winsound.SND_MEMORY | winsound.SND_ASYNC)
            except Exception:
                pass

        threading.Thread(target=_play, daemon=True).start()

    def play_correct_chime(self):
        if not self.enabled:
            return
        # Two ascending pleasant notes
        def _chime():
            try:
                # E5 (76) -> G#5 (80)
                wav1 = self._synthesize_pluck(76, duration=0.2)
                winsound.PlaySound(wav1, winsound.SND_MEMORY)
                wav2 = self._synthesize_pluck(80, duration=0.35)
                winsound.PlaySound(wav2, winsound.SND_MEMORY)
            except Exception:
                pass
        threading.Thread(target=_chime, daemon=True).start()

    def play_error_thud(self):
        if not self.enabled:
            return
        def _thud():
            try:
                # Low soft dull thud
                n_samples = int(self.sample_rate * 0.18)
                raw_audio = bytearray()
                for i in range(n_samples):
                    t = float(i) / self.sample_rate
                    env = math.exp(-15.0 * t)
                    s = (math.sin(2.0 * math.pi * 110.0 * t) + 0.5 * math.sin(2.0 * math.pi * 116.0 * t)) * env
                    val = int(s * 10000)
                    raw_audio.extend(struct.pack('<h', max(-32767, min(32767, val))))
                byte_rate = self.sample_rate * 2
                wav_header = struct.pack(
                    '<4sI4s4sIHHIIHH4sI',
                    b'RIFF', 36 + len(raw_audio), b'WAVE',
                    b'fmt ', 16, 1, 1, self.sample_rate, byte_rate, 2, 16,
                    b'data', len(raw_audio)
                )
                winsound.PlaySound(wav_header + raw_audio, winsound.SND_MEMORY | winsound.SND_ASYNC)
            except Exception:
                pass
        threading.Thread(target=_thud, daemon=True).start()

    def toggle_sound(self) -> bool:
        self.enabled = not self.enabled
        return self.enabled
