# tests/dialogs/__init__.py
from tests import (
    BaseTest, QTest, patch,
    QEvent, QKeyEvent, QColor, 
    QMessageBox, Qt
)
from ParamDialog import ParamDialog
from RenameDialog import RenameDialog
from SettingsDialog import SettingsDialog

# Constants per i test dei dialoghi
DEFAULT_PARAMS = {
    'cAttacco': 0,
    'durata': 5,
    'ritmo': [7, 15]
}

__all__ = [
    # Test utilities
    'BaseTest',
    'QTest', 
    'patch',
    'QEvent',
    'QKeyEvent',
    'QColor',
    'QMessageBox',
    'Qt',
    
    # Source components
    'ParamDialog',
    'RenameDialog',
    'SettingsDialog',
    
    # Constants
    'DEFAULT_PARAMS'
]