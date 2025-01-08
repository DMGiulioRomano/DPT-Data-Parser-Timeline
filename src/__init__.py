# src/__init__.py
# Import dei moduli principali
from .Commands import Command, CommandManager, MoveItemCommand
from .MainWindow import MainWindow
from .MusicItem import MusicItem
from .Timeline import Timeline, TrackItem
from .TimelineView import TimelineView
from .TimelineRuler import TimelineRuler
from .TimelineContainer import TimelineContainer
from .TrackHeaderView import TrackHeaderView, TrackHeaderItem, TrackHeaderScene
from .ParamDialog import ParamDialog
from .RenameDialog import RenameDialog
from .Settings import Settings
from .SettingsDialog import SettingsDialog

__all__ = [
    # Command Pattern
    'Command',
    'CommandManager',
    'MoveItemCommand',
    
    # Main Components
    'MainWindow',
    'MusicItem',
    
    # Timeline Components
    'Timeline',
    'TrackItem',
    'TimelineView',
    'TimelineRuler',
    'TimelineContainer',
    
    # Track Header Components
    'TrackHeaderView',
    'TrackHeaderItem',
    'TrackHeaderScene',
    
    # Dialogs
    'ParamDialog',
    'RenameDialog',
    'SettingsDialog',
    
    # Settings
    'Settings'
]