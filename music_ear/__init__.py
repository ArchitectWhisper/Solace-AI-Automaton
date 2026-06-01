
"""
Emotion Music Plugin - Integrated Interface
"""

from .plugin_base import (
	 	 PluginBase,
	 	 PluginManager,
	 	 EmotionReading,
	 	 EmotionalState,
	 	 manager
)

from .music_listener import MusicEmotionListener

from .agent_connector import (
	 	 AgentConnector,
	 	 EmotionBlender,
	 	 connect_to_agent
)

__all__ = [
	 	 'PluginBase',
	 	 'PluginManager',	
	 	 'EmotionReading',
	 	 'EmotionalState',
	 	 'MusicEmotionListener',
	 	 'AgentConnector',
	 	 'EmotionBlender',
	 	 'connect_to_agent',
	 	 'manager',
]

__version__ = "1.0.0"

def check_dependencies() -> dict:
	 	 """Maintenance Check: Verifies if the 'Ears' are fully functional."""
	 	 status = {"pyaudio": False, "librosa": False}
	 	 try:
	 	 	 	 import pyaudio
	 	 	 	 status["pyaudio"] = True
	 	 except ImportError: pass
	 		
	 	 try:
	 	 	 	 import librosa
	 	 	 	 status["librosa"] = True
	 	 except ImportError: pass
	 		
	 	 return status

