# tests/timeline/test_edge_cases.py
from tests.timeline import (
    BaseTest,
)
from src.MusicItem import MusicItem
import yaml  # Questa importazione esterna è necessaria per test YAML
import tempfile
import os
class EdgeCasesTest(BaseTest):

    def test_invalid_file_load(self):
        """Test caricamento file YAML sintatticamente invalido"""
        # Crea un file YAML temporaneo con contenuto invalido
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
            tmp.write("comportamenti: [this is not valid yaml}")  # Sintassi YAML invalida
            tmp_path = tmp.name

        try:
            # Imposta il file come current_file
            self.window.current_file = tmp_path
            # Tenta di caricare il file invalido (dovrebbe sollevare YAMLError)
            with self.assertRaises(yaml.YAMLError):
                self.window.load_from_yaml(test_mode=True)
                
        finally:
            # Pulisci il file temporaneo
            os.unlink(tmp_path)
    def test_boundary_movements(self):
        """Test movimenti ai limiti della timeline"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        
        # Prova a muovere prima di 0
        item.setPos(-100, 0)
        self.assertGreaterEqual(item.pos().x(), 0)
        
        # Prova a muovere sotto l'ultima traccia
        max_y = (self.timeline.num_tracks - 1) * self.timeline.track_height
        item.setPos(0, max_y + 100)
        self.assertLessEqual(item.pos().y(), max_y)

    def test_item_overlap_behavior(self):
        """Test comportamento sovrapposizione item"""
        item1 = self.timeline.add_music_item(0, 0, 3, "Test1", self.window.settings)
        item2 = self.timeline.add_music_item(0, 0, 3, "Test2", self.window.settings)
        
        # Verifica che gli item possano sovrapporsi
        self.assertEqual(item1.pos().x(), item2.pos().x())
        self.assertEqual(item1.pos().y(), item2.pos().y())