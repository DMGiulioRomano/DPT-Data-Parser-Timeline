# tests/timeline/test_stress.py
from tests.timeline import (
    BaseTest
)
from src.MusicItem import MusicItem
class StressTest(BaseTest):
    def test_rapid_operations(self):
        """Test operazioni rapide"""
        # Rapide operazioni undo/redo
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        for i in range(100):
            self.window.command_manager.undo()
            self.window.command_manager.redo()
            
    def test_multiple_selections(self):
        """Test selezioni multiple rapide"""
        items = []
        for i in range(20):
            items.append(self.timeline.add_music_item(i, 0, 3, f"Test{i}", 
                                                    self.window.settings))
            
        # Seleziona/deseleziona rapidamente
        for _ in range(50):
            for item in items:
                item.setSelected(True)
            for item in items:
                item.setSelected(False)