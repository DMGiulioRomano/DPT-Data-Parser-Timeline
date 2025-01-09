# tests/integration/test_event_handling_complex.py
from tests.integration import (
    BaseTest,
    MusicItem,
    QPointF
)

class ComplexEventHandlingTest(BaseTest):
    def test_multi_track_operations(self):
        """Test operazioni multi-traccia"""
        items = []
        for track in range(3):
            items.append(self.timeline.add_music_item(0, track, 3, 
                                                    f"Test{track}", 
                                                    self.window.settings))
        
        # Seleziona tutti gli items
        for item in items:
            item.setSelected(True)
            
        # Muovi tutti gli items
        self.window.move_selected_items(1)
        
        # Verifica che le posizioni relative siano mantenute
        y_distances = [items[i+1].pos().y() - items[i].pos().y() 
                      for i in range(len(items)-1)]
        self.assertEqual(y_distances[0], y_distances[1])

    def test_undo_redo_complex_operations(self):
        """Test undo/redo operazioni complesse"""
        # Crea una sequenza di operazioni
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)

        item.setSelected(True)
        initial_state = (item.pos(), item.rect().width())

        operations = [
            lambda: self.window.move_selected_items(1),
            lambda: self.window.modify_item_width(1.2),
            lambda: self.window.set_item_pos(item, item.pos() + QPointF(0, self.timeline.track_height))
        ]
        
        # Esegui operazioni
        
        for op in operations:
            op()
            
        # Undo tutte le operazioni
        for _ in range(len(operations)):
            self.window.command_manager.undo()
            
        final_state = (item.pos(), item.rect().width())
        self.assertEqual(initial_state, final_state)