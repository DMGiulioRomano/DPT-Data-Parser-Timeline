# tests/timeline/test_music_items.py
from timeline import (
    BaseTest,
    MusicItem,
    Qt, QPointF, QColor,
    QMouseEvent, QKeyEvent
)

class MusicItemTest(BaseTest):
    """Test specifici per gli item musicali"""

    def test_mouse_interaction(self):
        """Test interazioni mouse con item"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        
        # Test hover
        item.hoverEnterEvent(None)
        self.assertTrue(item.is_hovered)
        item.hoverLeaveEvent(None)
        self.assertFalse(item.is_hovered)
        
    def test_item_scaling(self):
        """Test scaling item"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        initial_width = item.rect().width()
        
        # Test modifica durata
        item.params['durata'] = 6  # Doppia durata
        new_width = item.rect().width()
        self.assertAlmostEqual(new_width/initial_width, 2, places=1)
        
    def test_color_changes(self):
        """Test cambiamenti colore"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        new_color = QColor(255, 0, 0)
        
        # Cambia colore
        item.color = new_color
        item.setBrush(new_color)
        
        self.assertEqual(item.brush().color(), new_color)

    def test_item_creation(self):
        """Test creazione item"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        self.assertIsInstance(item, MusicItem)
        self.assertEqual(item.name, "Test")
        self.assertEqual(item.params['cAttacco'], 0)

    def test_parameter_update(self):
        """Test aggiornamento parametri"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        
        # Modifica parametri
        item.params['cAttacco'] = 1.0
        item.params['durata'] = 4.0
        
        # Verifica posizione
        expected_x = item.params['cAttacco'] * self.timeline.pixels_per_beat * self.timeline.zoom_level
        self.assertAlmostEqual(item.pos().x(), expected_x, places=2)

    def test_text_style_update(self):
        """Test aggiornamento stile testo"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        old_size = item.text.font().pointSize()
        self.window.settings.set('item_text_size', old_size + 2)
        item.updateTextStyle()
        self.assertEqual(item.text.font().pointSize(), old_size + 2)
        
    def test_item_height_update(self):
        """Test aggiornamento altezza"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        new_height = 100
        item.updateHeight(new_height)
        self.assertEqual(item.rect().height(), new_height)

    def test_group_movement(self):
        """Test movimento di gruppo"""
        item1 = self.timeline.add_music_item(0, 0, 3, "Test1", self.window.settings)
        item2 = self.timeline.add_music_item(0, 1, 3, "Test2", self.window.settings)
        item1.setSelected(True)
        item2.setSelected(True)
        
        # Simula movimento gruppo
        initial_delta = abs(item2.pos().x() - item1.pos().x())
        item1.setPos(item1.pos().x() + 100, item1.pos().y())
        new_delta = abs(item2.pos().x() - item1.pos().x())
        self.assertAlmostEqual(initial_delta, new_delta, places=1)