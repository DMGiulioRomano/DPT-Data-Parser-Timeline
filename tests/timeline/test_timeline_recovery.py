# tests/timeline/test_timeline_recovery.py
from timeline import (
    BaseTest,
    MusicItem,
    Timeline
)
import yaml  # Per test recupero YAML

class RecoveryTest(BaseTest):
    def test_corrupted_file_recovery(self):
        """Test recupero da file corrotto"""
        # Crea file corrotto
        with open('corrupted.yaml', 'w') as f:
            f.write("invalid: yaml: content}")
            
        # Tenta caricamento
        self.window.current_file = 'corrupted.yaml'
        with self.assertRaises(yaml.YAMLError):
            self.window.load_from_yaml()
            
        # Verifica che la timeline sia in stato consistente
        self.assertGreaterEqual(self.timeline.num_tracks, 1)
        
    def test_invalid_parameter_recovery(self):
        """Test recupero da parametri invalidi"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        
        # Imposta parametro invalido
        item.params['cAttacco'] = "invalid"
        
        # Forza aggiornamento
        item.showParamDialog()
        
        # Verifica che il parametro sia stato corretto
        self.assertIsInstance(item.params['cAttacco'], (int, float))