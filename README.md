# Solace AI Automaton

Emotional regulation and safety framework for autonomous animatronic systems.

## Overview

Solace is a comprehensive emotional intelligence system designed for physical embodied agents. It combines:

- **Emotional Engine**: Real-time emotion simulation based on arousal, valence, urgency, and compliance
- **Safety Gates (Oath Gate)**: Governor patterns that prevent emotional escalation and system instability
- **Sensory Integration**: Music listener and visual perception systems
- **Memory Architecture**: Multi-layered memory with reflection and self-modeling
- **Hardware Abstraction**: ANS (Automaton Nervous System) protocol for hardware control

## System Architecture

### Core Components

```
Sensory Input (Music/Vision)
    ↓
Emotional Engine (E/V/U/C States)
    ↓
Governor (Safety Gates)
    ↓
ANS Output Vector
    ↓
Physical Hardware (Servos, Pupils, Eyelids)
```

### Core Files

- `self_model.py` - Self-awareness and introspection
- `self_memory.py` - Memory management and recall
- `oath_gate.py` - Safety governor and emotional regulation
- `emotion_blender.py` - Emotional state fusion and synthesis
- `reflection.py` - Reflection and learning mechanisms
- `nerve.py` - Neural pathway simulation
- `categorized_memory.py` - Structured memory storage
- `solace_type.py` - Type definitions and schemas
- `main.py` - System orchestration

### Sensory Systems

#### Music Ear (`music_ear/`)
- Real-time audio processing and emotional feature extraction
- Music listener with affect detection
- Plugin architecture for extensibility

#### Solace Vision (`solace_vision/`)
- Camera-based perception system
- Vision memory and sensor integration
- Real-time visual processing

### Memory Systems

- `solace_memory/` - JSON-based persistent memory storage
- `solace_images/` - Capture and organize visual data from sensory systems

## Installation

```bash
cd music_ear
pip install -r requirements.txt
```

## Features

### Emotional Model

The system uses a dimensional emotional model with four primary states:
- **Arousal (A)**: Energy level and activity intensity
- **Valence (V)**: Positivity/negativity of emotional tone
- **Urgency (U)**: Time pressure and importance weighting
- **Compliance (C)**: Safety adherence and constraint satisfaction

### Safety Architecture

The Governor pattern prevents emotional spiraling through:
- Threshold-based escalation gates
- Temporal decay mechanisms
- Compliance monitoring
- Fail-safe neutral states

## ANS (Automaton Nervous System)

Specification for hardware communication:
- **Transport**: Shared memory buffer or JSON-over-Serial
- **Cycle Rate**: 60Hz nominal
- **Latency Budget**: <100ms end-to-end
- **Output Vector**: Pupil dilation, eyelid aperture, saccade vectors, brow tension, mouth curve
- **Input Feedback**: Motor stall detection, touch pressure, joint position, system temperature

## Status

**Early Development** - Core systems implemented and tested. Stress tests completed on emotional stability.

## License

MIT License
