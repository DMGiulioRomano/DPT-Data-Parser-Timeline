# tests/test_timeline_core.py
from base_test import BaseTest
from Timeline import Timeline
from MusicItem import MusicItem

class TimelineCoreTest(BaseTest):
    """Test delle funzionalità core della timeline"""
    
    def test_track_management(self):
        """Test gestione tracce"""
        initial_tracks = self.timeline.num_tracks
        self.window.add_new_track()
        self.assertEqual(self.timeline.num_tracks, initial_tracks + 1)

    def test_zoom_functionality(self):
        """Test funzionalità zoom"""
        initial_zoom = self.timeline.zoom_level
        self.timeline.scale_scene(1.2)
        self.assertGreater(self.timeline.zoom_level, initial_zoom)