# tests/timeline/test_timeline_specific_behavior.py
from timeline import (
    BaseTest,
    MusicItem,
    Qt, QTest,
    patch
)
class SpecificBehaviorTest(BaseTest):
    def test_multi_monitor_support(self):
        """Test comportamento su setup multi-monitor"""
        # Simula secondo monitor
        with patch('PyQt5.QtWidgets.QDesktopWidget.screenCount') as mock_count:
            mock_count.return_value = 2
            # Sposta finestra tra monitor
            self.window.move(2000, 0)  # Posizione tipica secondo monitor
            self.assertTrue(self.window.geometry().isValid())

    def test_clipboard_operations(self):
        """Test operazioni clipboard"""
        # Crea item e copia/incolla
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        item.setSelected(True)
        
        # Simula Ctrl+C e Ctrl+V
        QTest.keyClick(self.window, Qt.Key_C, Qt.ControlModifier)
        QTest.keyClick(self.window, Qt.Key_V, Qt.ControlModifier)
        
        # Verifica item duplicato
        items = [i for i in self.timeline.items() if isinstance(i, MusicItem)]
        self.assertEqual(len(items), 2)

    def test_state_consistency(self):
        """Test consistenza stato dopo operazioni multiple"""
        # Esegui serie di operazioni che potrebbero corrompere lo stato
        for _ in range(10):
            # Aggiungi item
            item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
            # Modifica
            item.setSelected(True)
            self.window.move_selected_items(1)
            # Cancella
            self.window.delete_selected_items()
            # Undo tutto
            while self.window.command_manager.can_undo:
                self.window.command_manager.undo()
                
        # Verifica stato finale
        self.assertEqual(len([i for i in self.timeline.items() 
                            if isinstance(i, MusicItem)]), 0)