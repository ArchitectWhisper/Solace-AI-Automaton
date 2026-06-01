
import threading
import time
import numpy as np
from collections import deque
from typing import Optional, Dict

# ... (Keep your imports and try/except blocks as they are) ...

class MusicEmotionListener(PluginBase):
	 	 def __init__(self, sample_rate=22050, chunk_size=2048, analysis_interval=0.5, device_index=None):
	 	 	 	 super().__init__("music_listener")
	 	 	 	 self.sample_rate = sample_rate
	 	 	 	 self.chunk_size = chunk_size
	 	 	 	 self.analysis_interval = analysis_interval
	 	 	 		
	 	 	 	 # Audio piping
	 	 	 	 self._audio_buffer = deque(maxlen=int(sample_rate * 3))	
	 	 	 	 self._stop_event = threading.Event()
	 	 	 	 self._state_lock = threading.Lock() # Prevents reading while writing
	 	 	 		
	 	 	 	 self._current_state: Optional[EmotionReading] = None
	 	 	 	 self._feature_history = deque(maxlen=10)

	 	 def _analyze_audio(self):
	 	 	 	 """Analyze buffer with focus on efficiency"""
	 	 	 	 if not LIBROSA_AVAILABLE:
	 	 	 	 	 	 self._basic_analysis()
	 	 	 	 	 	 return

	 	 	 	 # Optimization: Only pull what we need from the buffer
	 	 	 	 audio = np.array(self._audio_buffer)
	 	 	 	 if len(audio) < self.sample_rate: return

	 	 	 	 try:
	 	 	 	 	 	 features = self._extract_features(audio)
	 	 	 	 	 	 reading = self._map_features_to_emotion(features)
	 	 	 	 	 		
	 	 	 	 	 	 with self._state_lock:
	 	 	 	 	 	 	 	 self._current_state = reading
	 	 	 	 	 		
	 	 	 	 	 	 self.emit_emotion(reading)
	 	 	 	 except Exception as e:
	 	 	 	 	 	 print(f"[MusicListener] Analysis error: {e}")

	 	 def _extract_features(self, audio: np.ndarray) -> Dict[str, float]:
	 	 	 	 """Lightweight feature extraction"""
	 	 	 	 features = {}
	 	 	 		
	 	 	 	 # Energy (Loudness)
	 	 	 	 rms = librosa.feature.rms(y=audio)[0]
	 	 	 	 features['energy'] = float(np.mean(rms))
	 	 	 		
	 	 	 	 # Spectral Centroid (Brightness/Sharpness)
	 	 	 	 # We downsample the analysis for speed
	 	 	 	 spec_cent = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)[0]
	 	 	 	 features['brightness'] = float(np.mean(spec_cent))

	 	 	 	 # Tempo - Only calculate if buffer is large enough, otherwise use last known
	 	 	 	 # Maintenance Tip: This is the 'heavy' part of the engine.	
	 	 	 	 if len(audio) >= self.sample_rate * 2:
	 	 	 	 	 	 try:
	 	 	 	 	 	 	 	 tempo, _ = librosa.beat.beat_track(y=audio, sr=self.sample_rate)
	 	 	 	 	 	 	 	 features['tempo'] = float(tempo)
	 	 	 	 	 	 except:
	 	 	 	 	 	 	 	 features['tempo'] = 120.0
	 	 	 		
	 	 	 	 return features

	 	 def to_context(self) -> dict:
	 	 	 	 """
	 	 	 	 Maintenance Bridge: Maps Ear sensors to the Emotion Engine inputs.
	 	 	 	 Call this to get data for your 'ContextSnapshot'.
	 	 	 	 """
	 	 	 	 with self._state_lock:
	 	 	 	 	 	 if not self._current_state:
	 	 	 	 	 	 	 	 return {"novelty": 0, "reward": 0, "threat": 0}
	 	 	 	 	 		
	 	 	 	 	 	 # Logic: High energy + High brightness = Novelty
	 	 	 	 	 	 # High harmonic complexity or dissonance = Threat
	 	 	 	 	 	 s = self._current_state
	 	 	 	 	 	 return {
	 	 	 	 	 	 	 	 "novelty": self.clamp(s.e_value * 0.7),
	 	 	 	 	 	 	 	 "reward": self.clamp(s.v_value) if s.v_value &gt; 0 else 0,
	 	 	 	 	 	 	 	 "threat": self.clamp(abs(s.v_value)) if s.v_value < -0.4 else 0,
	 	 	 	 	 	 	 	 "time_pressure": self.clamp((s.metadata.get('tempo', 120) - 60) / 120)
	 	 	 	 	 	 }

	 	 @staticmethod
	 	 def clamp(x: float) -> float:
	 	 	 	 return max(0.0, min(1.0, x))

	 	 # ... (Keep stop/start and callback logic as they are) ...


