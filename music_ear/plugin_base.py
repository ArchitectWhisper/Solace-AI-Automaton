from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum
import threading
from collections import deque
import queue

# ... [EmotionalState and EmotionReading remain the same] ...

class PluginBase(ABC):
    """Base class for all emotion sensors"""
    def __init__(self, name: str):
        self.name = name
        self.is_active = False
        self._callbacks: List[Callable[[EmotionReading], None]] = []
        self._event_queue = queue.Queue(maxsize=50) # Prevents memory leaks if unread
        
    def register_callback(self, callback: Callable[[EmotionReading], None]):
        self._callbacks.append(callback)
        
    def emit_emotion(self, reading: EmotionReading):
        """Broadcast signal to the brain"""
        for callback in self._callbacks:
            try:
                callback(reading)
            except Exception as e:
                print(f"[{self.name}] Signal Error: {e}")
        
        if self._event_queue.full():
            try: self._event_queue.get_nowait() # Clear old data
            except queue.Empty: pass
        self._event_queue.put(reading)

class PluginManager:
    """The central fuse box for all emotion plugins"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized: return
        self._plugins: Dict[str, PluginBase] = {}
        # Maintenance: Deque is a conveyor belt, much faster than a list for history
        self._emotion_history = deque(maxlen=100)
        self._agent_callback: Optional[Callable] = None
        self._initialized = True
        
    def register_plugin(self, plugin: PluginBase):
        plugin.register_callback(self._on_emotion_received)
        self._plugins[plugin.name] = plugin
        print(f"[PluginManager] Wired up: {plugin.name}")

    def _on_emotion_received(self, reading: EmotionReading):
        """Thread-safe update of emotion history"""
        with self._lock:
            self._emotion_history.append(reading)
            if self._agent_callback:
                try: self._agent_callback(reading)
                except Exception as e: print(f"[Manager] Callback Fault: {e}")

    def get_blended_state(self) -> Optional[EmotionReading]:
        """Mixes all active sensor signals into one output"""
        with self._lock:
            active_states = [p.get_current_state() for p in self._plugins.values() 
                             if p.is_active and p.get_current_state()]
        
        if not active_states: return None
            
        # Weighted blend logic
        total_weight = sum(s.confidence for s in active_states)
        if total_weight == 0: return active_states[0]

        avg_e = sum(s.e_value * s.confidence for s in active_states) / total_weight
        avg_v = sum(s.v_value * s.confidence for s in active_states) / total_weight
        
        # Dominant source (The 'Loudest' signal)
        dominant = max(active_states, key=lambda x: x.confidence)
        
        return EmotionReading(
            state=dominant.state,
            e_value=avg_e,
            v_value=avg_v,
            confidence=min(total_weight, 1.0),
            source="blended",
            metadata={"sources": [s.source for s in active_states]}
        )
