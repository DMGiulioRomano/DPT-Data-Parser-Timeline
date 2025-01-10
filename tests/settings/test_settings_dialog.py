# tests/settings/test_settings_dialog.py
from tests.settings import (
    BaseTest,
    Qt, QColor
)
from src.SettingsDialog import SettingsDialog
class SettingsDialogTest(BaseTest):
    def test_directory_selection(self):
        """Test selezione directory"""
        dialog = SettingsDialog(self.window.settings)
        
        test_path = "/test/path"
        dialog.make_dir_edit.setText(test_path)
        dialog.accept()
        
        self.assertEqual(
            self.window.settings.get('make_directory'),
            test_path
        )
        
    def test_color_settings(self):
        """Test impostazioni colori"""
        dialog = SettingsDialog(self.window.settings)
        
        new_color = QColor(255, 0, 0)
        dialog.text_color = new_color
        dialog.accept()
        
        self.assertEqual(
            self.window.settings.get('text_color'),
            new_color.name()
        )