# tests/test_error_handling.py
class ErrorHandlingTest(BaseTest):
    def test_invalid_file_operations(self):
        """Test operazioni file invalide"""
        # Test caricamento file non esistente
        self.window.current_file = "nonexistent.yaml"
        with self.assertRaises(FileNotFoundError):
            self.window.load_from_yaml()
            
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