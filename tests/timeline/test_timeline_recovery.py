# tests/timeline/test_timeline_recovery.py
from tests.timeline import (
    BaseTest
)
from src.Timeline import Timeline
from src.MusicItem import MusicItem
from src.ParamDialog import ParamDialog
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
            self.window.load_from_yaml(test_mode=True)
            
        # Verifica che la timeline sia in stato consistente
        self.assertGreaterEqual(self.timeline.num_tracks, 1)
        
    def test_invalid_parameter_recovery(self):
        """Test recupero da parametri invalidi"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        
        # Imposta parametro invalido
        item.params['cAttacco'] = "invalid"
        
        # Crea una istanza di ParamDialog
        dialog = ParamDialog(item.params, item.color, item=item)
        
        # Simula l'inserimento di un valore valido nella casella di testo 'cAttacco'
        dialog.inputs['cAttacco'].setText("1.5")
        
        # Accetta il dialogo
        dialog.accept()
        
        # Verifica che il parametro sia stato corretto
        self.assertIsInstance(item.params['cAttacco'], (int, float))