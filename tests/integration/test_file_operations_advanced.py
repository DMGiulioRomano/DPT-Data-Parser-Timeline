# tests/integration/test_file_operations_advanced.py
from tests.integration import (
    BaseTest, patch,
    MusicItem, QMessageBox,
    QCloseEvent,
    tempfile
)
import yaml
import os
class AdvancedFileTest(BaseTest):

    def test_file_state_recovery(self):
        """Test recupero stato file"""
        test_data = {
            "comportamenti": [{
                "cAttacco": 0,
                "durataArmonica": 26,
                "ritmo": [7,15],
                "durata": 5.0,
                "ampiezza": [-30,-0.25], 
                "frequenza": [6,1],
                "posizione": -8
            }]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            yaml.dump(test_data, tmp, allow_unicode=True)
            tmp_path = tmp.name

        try:
            self.window.current_file = tmp_path
            self.window.load_from_yaml(test_mode=True)
            
            items = [i for i in self.timeline.items() if isinstance(i, MusicItem)]
            self.assertEqual(items[0].params['cAttacco'], 0)
            
            items[0].params['cAttacco'] = 24
            self.window.load_from_yaml(test_mode=True)
            
            items = [i for i in self.timeline.items() if isinstance(i, MusicItem)]
            self.assertEqual(items[0].params['cAttacco'], 0)
        finally:
            os.unlink(tmp_path)
                        
    def test_autosave_behavior(self):
        """Test comportamento autosave"""
        # Simula chiusura con modifiche non salvate
        self.window.current_file = "test.yaml"
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        
        with patch('PyQt5.QtWidgets.QMessageBox.question') as mock_question:
            mock_question.return_value = QMessageBox.Yes
            self.window.closeEvent(QCloseEvent())
            mock_question.assert_called_once()