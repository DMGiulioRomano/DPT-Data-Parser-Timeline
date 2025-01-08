class ViewSyncTest(BaseTest):
    def test_selection_sync(self):
        """Test sincronizzazione selezione tra viste"""
        # Seleziona da timeline
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        item.setSelected(True)
        
        # Verifica header
        header = self.window.timeline_container.track_header_view.scene.header_items[0]
        self.assertTrue(header.is_selected)
        
        # Seleziona da header
        header.setSelected(False)
        self.assertFalse(item.isSelected())

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