# tests/timeline/test_timeline_specific_behavior.py
from tests.timeline import (
    BaseTest,
    Qt, QTest,
    patch
)
from src.MusicItem import MusicItem
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QAction
from PyQt5.QtGui import QKeySequence

class SpecificBehaviorTest(BaseTest):
    def test_multi_monitor_support(self):
        """Test comportamento su setup multi-monitor"""
        # Simula secondo monitor
        with patch('PyQt5.QtWidgets.QDesktopWidget.screenCount') as mock_count:
            mock_count.return_value = 2
            # Sposta finestra tra monitor
            self.window.move(2000, 0)  # Posizione tipica secondo monitor
            self.assertTrue(self.window.geometry().isValid())
        
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

    def test_clipboard_operations(self):
        """Test operazioni clipboard"""
        # Crea item e copia/incolla
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        item.setSelected(True)
        
        # Trova e attiva direttamente le azioni di menu
        for action in self.window.findChildren(QAction):
            if action.shortcut() == QKeySequence.Copy:
                action.trigger()
            
        QApplication.processEvents()
        
        for action in self.window.findChildren(QAction):
            if action.shortcut() == QKeySequence.Paste:
                action.trigger()
                
        QApplication.processEvents()
        
        # Verifica item duplicato
        items = [i for i in self.timeline.items() if isinstance(i, MusicItem)]
        self.assertEqual(len(items), 2)