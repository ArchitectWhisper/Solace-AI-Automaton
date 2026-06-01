
from typing import Callable, Optional, Dict
import time

# ---- Integration Bridge ----
class AgentBridge:
	 	 """Translates Raw Sensor Data into Context for the Emotion Engine"""
	 		
	 	 @staticmethod
	 	 def to_context(blended: EmotionReading) -&gt; ContextSnapshot:
	 	 	 	 # Map Valence (V) to Reward/Threat
	 	 	 	 reward = max(0.0, blended.v_value) if blended.v_value &gt; 0 else 0.0
	 	 	 	 threat = abs(blended.v_value) if blended.v_value &lt; -0.3 else 0.0
	 	 	 		
	 	 	 	 # Map Energy (E) to Novelty/Pressure
	 	 	 	 novelty = max(0.0, blended.e_value - 0.5)	
	 	 	 	 time_pressure = max(0.0, blended.e_value * 0.4)
	 	 	 		
	 	 	 	 return ContextSnapshot(
	 	 	 	 	 	 novelty=novelty,
	 	 	 	 	 	 reward=reward,
	 	 	 	 	 	 threat=threat,
	 	 	 	 	 	 goal_blocked=False,
	 	 	 	 	 	 time_pressure=time_pressure,
	 	 	 	 	 	 social_support=0.5 if blended.source == "voice" else 0.2,
	 	 	 	 	 	 skills_fit=1.0,
	 	 	 	 	 	 resources=1.0,
	 	 	 	 	 	 constraint=0.0
	 	 	 	 )

# ---- Optimized Blender ----
class EmotionBlender:
	 	 def __init__(self, decay_rate: float = 0.9):
	 	 	 	 self.decay_rate = decay_rate
	 	 	 	 self._emotions: Dict[str, EmotionReading] = {}
	 	 	 	 self._weights = {"typing": 1.0, "voice": 1.2, "music": 0.6}

	 	 def update(self, reading: EmotionReading):
	 	 	 	 self._emotions[reading.source] = reading

	 	 def blend(self) -&gt; Optional[EmotionReading]:
	 	 	 	 if not self._emotions: return None
	 	 	 	 	 		
	 	 	 	 total_w, e_sum, v_sum = 0.0, 0.0, 0.0
	 	 	 		
	 	 	 	 # Find the most intense reading (The "Loudest Pipe" logic)
	 	 	 	 # If one source is screaming 'Danger', we don't want to ignore it.
	 	 	 	 dominant = max(self._emotions.values(), key=lambda x: abs(x.v_value) * x.confidence)

	 	 	 	 for src, em in self._emotions.items():
	 	 	 	 	 	 weight = self._weights.get(src, 1.0) * em.confidence
	 	 	 	 	 	 e_sum += em.e_value * weight
	 	 	 	 	 	 v_sum += em.v_value * weight
	 	 	 	 	 	 total_w += weight
	 	 	 	 	 		
	 	 	 	 if total_w == 0: return None
	 	 	 	 	 		
	 	 	 	 return EmotionReading(
	 	 	 	 	 	 state=dominant.state,
	 	 	 	 	 	 e_value=round(e_sum / total_w, 2),
	 	 	 	 	 	 v_value=round(v_sum / total_w, 2),
	 	 	 	 	 	 confidence=round(min(total_w, 1.0), 2),
	 	 	 	 	 	 source="blended"
	 	 	 	 )


