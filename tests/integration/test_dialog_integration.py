# tests/integration/test_dialog_integration.py
from tests.integration import (
    BaseTest, 
    ParamDialog, SettingsDialog,
    TrackItem, Qt,
    QColor
)

class DialogIntegrationTest(BaseTest):
    def test_param_dialog_update_timeline(self):
        """Test aggiornamento timeline dopo modifiche parametri"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        old_pos = item.pos()
        
        # Apri dialog e modifica cAttacco
        dialog = ParamDialog(item.params, item.color,item=item)
        dialog.inputs['cAttacco'].setText("2.0")
        dialog.accept()
        
        # Verifica che la timeline sia aggiornata
        expected_x = 2.0 * self.timeline.pixels_per_beat * self.timeline.zoom_level
        self.assertAlmostEqual(item.pos().x(), expected_x, places=1)
        
    def test_settings_dialog_live_update(self):
        """Test aggiornamento live dopo cambio settings"""
        dialog = SettingsDialog(self.window.settings, self.window)
        
        # Cambia colore sfondo tracce
        new_color = "#FF0000"
        dialog.track_color = QColor(new_color)
        dialog.accept()
        
        # Verifica che le tracce siano aggiornate
        for item in self.timeline.items():
            if isinstance(item, TrackItem):
                self.assertEqual(item.base_color.name().lower(), new_color.lower())