# tests/test_timeline_ruler.py
from base_test import BaseTest
from TimelineRuler import TimelineRuler

class TimelineRulerTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.ruler_view = self.window.timeline_container.ruler_view
        self.ruler = self.ruler_view.scene()

    def test_ruler_zoom_sync(self):
        """Test sincronizzazione zoom tra ruler e timeline"""
        initial_zoom = self.timeline.zoom_level
        self.timeline.scale_scene(1.5)
        
        # Verifica che il ruler si sia aggiornato
        self.assertEqual(self.ruler.zoom_level, self.timeline.zoom_level)
        
    def test_ruler_scroll_sync(self):
        """Test sincronizzazione scroll"""
        scrollbar = self.timeline_container.timeline_view.horizontalScrollBar()
        scrollbar.setValue(100)
        
        # Verifica che il ruler si sia spostato
        self.assertEqual(
            self.ruler_view.horizontalScrollBar().value(),
            scrollbar.value()
        )

    def test_time_markers(self):
        """Test markers temporali del ruler"""
        # Zoom out per vedere più markers
        self.timeline.scale_scene(0.5)
        markers = [item for item in self.ruler.items() 
                  if isinstance(item, QGraphicsTextItem)]
        self.assertGreater(len(markers), 0)

    def test_interval_calculation(self):
        """Test calcolo intervalli basato su zoom"""
        ruler = self.window.timeline_container.ruler_view.scene()
        
        # Test diversi livelli di zoom
        test_zooms = [0.01, 0.1, 0.3, 1.0, 2.0, 5.0]
        for zoom in test_zooms:
            self.timeline.scale_scene(zoom/self.timeline.zoom_level)
            ruler.draw_ruler()
            
            # Verifica presenza elementi grafici
            text_items = [i for i in ruler.items() if isinstance(i, QGraphicsTextItem)]
            self.assertGreater(len(text_items), 0)

    def test_color_update(self):
        """Test aggiornamento colori"""
        ruler = self.window.timeline_container.ruler_view.scene()
        new_color = "#FF0000"
        self.window.settings.set('timeline_background_color', new_color)
        ruler.updateColors()
        self.assertEqual(ruler.backgroundBrush().color().name(), new_color)