# tests/test_settings.py
from base_test import BaseTest
from Settings import Settings
import json
import os

class SettingsTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.settings = Settings()

    def test_settings_persistence(self):
        """Test persistenza settings"""
        # Modifica setting
        test_value = "/test/path"
        self.settings.set('last_open_directory', test_value)
        
        # Ricarica settings
        new_settings = Settings()
        self.assertEqual(
            new_settings.get('last_open_directory'),
            test_value
        )

    def test_default_settings(self):
        """Test valori default"""
        self.assertEqual(
            self.settings.get('default_track_count'),
            8  # valore default atteso
        )

    def test_settings_update(self):
        """Test aggiornamento settings"""
        # Cambia colore testo
        new_color = "#FF0000"
        self.settings.set('text_color', new_color)
        
        # Verifica che l'UI si sia aggiornata
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.settings)
        self.assertEqual(
            item.text.defaultTextColor().name(),
            new_color
        )

    def test_file_permissions(self):
        """Test permessi file settings"""
        settings = Settings()
        
        # Test scrittura con permessi insufficienti
        with patch('builtins.open', side_effect=PermissionError):
            settings.set('test_key', 'test_value')
            # Verifica che non ci siano errori e il valore sia in memoria
            self.assertEqual(settings.get('test_key'), 'test_value')

    def test_missing_settings_file(self):
        """Test file settings mancante"""
        import os
        
        # Rimuovi file settings
        if os.path.exists('settings.json'):
            os.rename('settings.json', 'settings.json.bak')
        
        try:
            settings = Settings()
            # Verifica valori default
            self.assertEqual(
                settings.get('default_track_count'),
                settings.default_settings['default_track_count']
            )
        finally:
            # Ripristina file
            if os.path.exists('settings.json.bak'):
                os.rename('settings.json.bak', 'settings.json')