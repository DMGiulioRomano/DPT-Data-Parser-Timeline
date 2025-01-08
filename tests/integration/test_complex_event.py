# tests/integration/test_complex_event.py
from integration import (
    BaseTest, 
    MusicItem,
    QPointF
)

class ComplexEventTest(BaseTest):
    def test_concurrent_operations(self):
        """Test operazioni concorrenti"""
        # Simula operazioni simultanee
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        
        # Muovi e scala contemporaneamente
        item.setPos(item.pos() + QPointF(100,0))
        self.window.modify_item_width(1.5)
        
        # Verifica che entrambe le operazioni abbiano effetto
        self.assertNotEqual(item.pos().x(), 0)
        self.assertGreater(item.rect().width(), 300)