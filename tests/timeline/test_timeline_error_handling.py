# tests/timeline/test_error_handling.py
from tests.timeline import (
    BaseTest
)
from src.Timeline import Timeline
from src.MusicItem import MusicItem
import yaml  # Per gestione errori YAML
from src.Settings import Settings

class ErrorHandlingTest(BaseTest):
    def test_invalid_file_operations(self):
        """Test operazioni file invalide"""
        # Test caricamento file non esistente
        self.window.current_file = "nonexistent.yaml"
        with self.assertRaises(FileNotFoundError):
            self.window.load_from_yaml(test_mode=True)
            
    def test_corrupted_settings(self):
        """Test settings corrotte"""
        # Corrompi file settings
        with open(self.window.settings.settings_file, 'w') as f:
            f.write("invalid json")
            
        # Verifica che vengano caricati i default
        new_settings = Settings()
        self.assertEqual(
            new_settings.get('default_track_count'),
            new_settings.default_settings['default_track_count']
        )