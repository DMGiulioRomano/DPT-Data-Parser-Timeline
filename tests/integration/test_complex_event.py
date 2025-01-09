# tests/integration/test_complex_event.py
from tests.integration import (
    BaseTest, 
    QPointF
)

class ComplexEventTest(BaseTest):
    def test_concurrent_operations(self):
        """Test operazioni concorrenti"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        
        initial_width = item.rect().width()
        item.setPos(item.pos() + QPointF(100,0))
        
        # Seleziona l'item prima di modificarne la larghezza
        item.setSelected(True)
        self.window.modify_item_width(1.5)
        
        self.assertNotEqual(item.pos().x(), 0)
        self.assertAlmostEqual(item.rect().width(), initial_width * 1.5, places=1)
