# tests/test_edge_cases.py
from base_test import BaseTest
import yaml

class EdgeCasesTest(BaseTest):
    def test_invalid_file_load(self):
        """Test caricamento file invalido"""
        with self.assertRaises(yaml.YAMLError):
            self.window.current_file = "invalid.yaml"
            self.window.load_from_yaml()

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