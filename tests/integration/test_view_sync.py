# tests/integration/test_view_sync.py
from tests.integration import (
    BaseTest,
    MusicItem,
    TrackItem,
    Qt
)

class ViewSyncTest(BaseTest):

    def test_selection_sync(self):
        """Test sincronizzazione selezione tra viste"""
        # Seleziona da timeline
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        item.setSelected(True)
        
        # Verifica che l'header NON sia selezionato quando si seleziona un item
        header = self.window.timeline_container.track_header_view.scene.header_items[0]
        self.assertFalse(header.is_selected)
        
        # Verifica che selezionando l'header venga aggiornata la traccia corrente
        header.setSelected(True)
        self.assertEqual(self.window.selected_track, 0)
        
        # Deselezionando l'header, la traccia corrente dovrebbe essere None
        header.setSelected(False)
        self.assertIsNone(self.window.selected_track)

    def test_scroll_sync_complex(self):
        """Test sincronizzazione scroll complessa"""
        container = self.window.timeline_container
        
        # Scroll orizzontale con zoom
        self.timeline.scale_scene(2.0)
        container.timeline_view.horizontalScrollBar().setValue(100)
        
        self.assertEqual(
            container.ruler_view.horizontalScrollBar().value(),
            container.timeline_view.horizontalScrollBar().value()
        )