# tests/timeline/test_timeline.py
from tests.timeline import (
    BaseTest, QTest
)
from src.Timeline import Timeline
from src.MusicItem import MusicItem
from src.Timeline import TrackItem
class TimelineTest(BaseTest):

    def test_scene_rect_update(self):
        """Test aggiornamento dimensioni scena"""
        initial_height = self.timeline.sceneRect().height()
        initial_tracks = self.timeline.num_tracks
        
        try:
            self.timeline.num_tracks += 13
            self.timeline.draw_tracks()
            self.assertGreater(self.timeline.sceneRect().height(), initial_height)
        finally:
            self.timeline.num_tracks = initial_tracks
            self.timeline.draw_tracks()

    def test_track_color_update(self):
        """Test aggiornamento colore tracce"""
        initial_tracks = self.timeline.num_tracks
        new_color = "#FF0000"
        
        try:
            self.window.settings.set('track_background_color', new_color)
            self.timeline.draw_tracks()
            track_items = [item for item in self.timeline.items() if isinstance(item, TrackItem)]
            self.assertTrue(len(track_items) > 0)
            self.assertEqual(track_items[0].base_color.name().upper(), new_color.upper())
        finally:
            self.timeline.num_tracks = initial_tracks
            self.timeline.draw_tracks()

    def test_move_track(self):
        """Test spostamento traccia"""
        # Aggiungi items su due tracce
        item1 = self.timeline.add_music_item(0, 0, 3, "Test1", self.window.settings)
        item2 = self.timeline.add_music_item(0, 1, 3, "Test2", self.window.settings)
        
        initial_y1 = item1.pos().y()
        initial_y2 = item2.pos().y()
        
        # Sposta tracce
        self.timeline.move_track(0, 1)
        
        # Verifica che gli items si siano spostati correttamente
        self.assertEqual(item1.pos().y(), initial_y2)
        self.assertEqual(item2.pos().y(), initial_y1)

    def test_initialize_components(self):
        """Test inizializzazione componenti"""
        self.timeline.initialize_components()
        container = self.window.timeline_container
        self.assertEqual(
            container.track_header_view.scene.header_items[0].track_number,
            0
        )

    def test_scale_track_height_constraints(self):
        """Test vincoli altezza tracce"""
        initial_height = self.timeline.track_height
        
        # Test limite minimo
        self.timeline.scale_track_height(0.1)  # Dovrebbe limitare a min_height
        self.assertGreaterEqual(self.timeline.track_height, 20)
        
        # Test limite massimo
        self.timeline.scale_track_height(10)  # Dovrebbe limitare a max_height
        self.assertLessEqual(self.timeline.track_height, 200)

    def test_draw_tracks_update_headers(self):
        """Test aggiornamento header durante disegno tracce"""
        initial_tracks = self.timeline.num_tracks
        self.timeline.num_tracks += 1
        self.timeline.draw_tracks()
        
        # Verifica che gli header siano aggiornati
        container = self.window.timeline_container
        self.assertEqual(
            len(container.track_header_view.scene.header_items),
            initial_tracks + 1
        )