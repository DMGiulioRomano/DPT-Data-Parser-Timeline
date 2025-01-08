from tests.ui import BaseTest



class ComplexUITest(BaseTest):
    def test_multi_view_interaction(self):
        """Test interazioni multiple viste"""
        container = self.window.timeline_container
        
        # Modifica traccia da header
        header = container.track_header_view.scene.header_items[0]
        header.setSelected(True)
        
        # Verifica effetto su timeline
        self.assertEqual(self.window.selected_track, 0)
        
        # Modifica da timeline
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        item.setSelected(True)
        
        # Verifica sincronizzazione
        self.assertTrue(header.is_selected)