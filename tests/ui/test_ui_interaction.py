# tests/test_ui_interaction.py
from tests.ui import BaseTest, QTest, Qt


class UIInteractionTest(BaseTest):
    """Test delle interazioni UI"""
    
    def test_keyboard_shortcuts(self):
        """Test scorciatoie da tastiera"""
        initial_items = len(self.timeline.items())
        QTest.keyClick(self.window, Qt.Key_1, Qt.ControlModifier)
        self.assertGreater(len(self.timeline.items()), initial_items)

    def test_search_functionality(self):
        """Test funzionalità di ricerca"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        item.params['posizione'] = -8
        
        self.window.search_param.setCurrentText('posizione')
        self.window.search_value.setText('-8')
        self.window.perform_search()
        
        self.assertTrue(hasattr(item, 'highlighted') and item.highlighted)