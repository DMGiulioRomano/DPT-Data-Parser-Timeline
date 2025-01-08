# tests/settings/test_settings.py
from settings import (
    BaseTest, patch,
    Settings,
    json, os
)

class SettingsTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.settings = Settings()

    def test_settings_persistence(self):
        """Test persistenza settings"""
        test_value = "/test/path"
        self.settings.set('last_open_directory', test_value)
        
        new_settings = Settings()
        self.assertEqual(
            new_settings.get('last_open_directory'),
            test_value
        )

    def test_default_settings(self):
        """Test valori default"""
        self.assertEqual(
            self.settings.get('default_track_count'),
            8
        )

    def test_settings_update(self):
        """Test aggiornamento settings"""
        new_color = "#FF0000"
        self.settings.set('text_color', new_color)
        
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.settings)
        self.assertEqual(
            item.text.defaultTextColor().name(),
            new_color
        )

    def test_file_permissions(self):
        """Test permessi file settings"""
        settings = Settings()
        
        with patch('builtins.open', side_effect=PermissionError):
            settings.set('test_key', 'test_value')
            self.assertEqual(settings.get('test_key'), 'test_value')

    def test_missing_settings_file(self):
        """Test file settings mancante"""
        if os.path.exists('settings.json'):
            os.rename('settings.json', 'settings.json.bak')
        
        try:
            settings = Settings()
            self.assertEqual(
                settings.get('default_track_count'),
                settings.default_settings['default_track_count']
            )
        finally:
            if os.path.exists('settings.json.bak'):
                os.rename('settings.json.bak', 'settings.json')