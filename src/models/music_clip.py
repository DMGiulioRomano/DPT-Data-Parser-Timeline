from dataclasses import dataclass
from typing import List, Union, Optional
from PyQt5.QtCore import QObject, pyqtSignal

@dataclass
class MusicClipParams:
    cAttacco: float = 0.0
    durataArmonica: int = 26
    ritmo: List[int] = None
    durata: Union[float, List[float]] = 5.0
    ampiezza: List[float] = None
    frequenza: List[int] = None
    posizione: int = -8

    def __post_init__(self):
        if self.ritmo is None:
            self.ritmo = [7, 15]
        if self.ampiezza is None:
            self.ampiezza = [-30, -0.25]
        if self.frequenza is None:
            self.frequenza = [6, 1]

class MusicClipModel(QObject):
    """Model class for music clips with business logic and validation"""
    
    # Signals for MVC pattern
    params_changed = pyqtSignal(str, object)  # (param_name, new_value)
    name_changed = pyqtSignal(str)
    position_changed = pyqtSignal(float, float)  # (x, y)
    
    def __init__(self, name: str = "Clip"):
        super().__init__()
        self._name = name
        self._params = MusicClipParams()
        self._x = 0.0
        self._y = 0.0
        self._track_index = 0
        self._duration = 5.0  # Default duration
        
    @property
    def name(self) -> str:
        return self._name
        
    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Clip name cannot be empty")
        self._name = value.strip()
        self.name_changed.emit(self._name)

    @property
    def params(self) -> MusicClipParams:
        return self._params

    def set_param(self, name: str, value: Union[float, int, List]):
        """Set a parameter with validation"""
        if not hasattr(self._params, name):
            raise ValueError(f"Invalid parameter name: {name}")
            
        old_value = getattr(self._params, name)
        
        # Type validation
        if isinstance(old_value, (int, float)):
            if isinstance(value, (list, tuple)):
                value = value[0] if len(value) > 0 else 0
            try:
                value = type(old_value)(value)
                # Additional numeric validation
                if name == "cAttacco" and value < 0:
                    raise ValueError("cAttacco cannot be negative")
                if name == "durata" and value <= 0:
                    raise ValueError("durata must be positive")
            except (ValueError, TypeError):
                raise ValueError(f"Invalid value type for {name}")
        elif isinstance(old_value, list):
            if not isinstance(value, (list, tuple)):
                value = [value]
            if len(value) != len(old_value):
                raise ValueError(f"List length mismatch for {name}")
            # Validate numeric ranges for specific parameters
            if name == "ritmo":
                if not all(isinstance(x, (int, float)) and x > 0 for x in value):
                    raise ValueError("ritmo values must be positive numbers")
            elif name == "ampiezza":
                if not all(isinstance(x, (int, float)) for x in value):
                    raise ValueError("ampiezza values must be numbers")
            elif name == "frequenza":
                if not all(isinstance(x, (int, float)) and x > 0 for x in value):
                    raise ValueError("frequenza values must be positive numbers")
                
        # Only emit if value actually changed
        if value != old_value:
            setattr(self._params, name, value)
            self.params_changed.emit(name, value)
        
    @property
    def position(self) -> tuple[float, float]:
        return (self._x, self._y)
        
    @position.setter 
    def position(self, pos: tuple[float, float]):
        self._x, self._y = pos
        self.position_changed.emit(self._x, self._y)
        
    @property
    def track_index(self) -> int:
        return self._track_index
        
    @track_index.setter
    def track_index(self, value: int):
        if value < 0:
            raise ValueError("Track index cannot be negative")
        self._track_index = value

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML serialization"""
        return {
            "name": self._name,
            "cAttacco": self._params.cAttacco,
            "durataArmonica": self._params.durataArmonica,
            "ritmo": self._params.ritmo,
            "durata": self._params.durata,
            "ampiezza": self._params.ampiezza,
            "frequenza": self._params.frequenza,
            "posizione": self._params.posizione
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'MusicClipModel':
        """Create from dictionary (YAML deserialization)"""
        clip = cls(name=data.get("name", "Clip"))
        for key, value in data.items():
            if key == "name":
                continue
            if hasattr(clip._params, key):
                clip.set_param(key, value)
        return clip