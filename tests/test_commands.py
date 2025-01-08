# tests/test_commands.py
from base_test import BaseTest
from PyQt5.QtCore import QPointF
from Commands import MoveItemCommand
from base_test import BaseTest

from Commands import CommandManager, MoveItemCommand
from PyQt5.QtCore import QPointF
from MusicItem import MusicItem

class CommandsTest(BaseTest):
    """Test del sistema di comandi"""
    def setUp(self):
        super().setUp()
        self.command_manager = CommandManager()

    def test_command_stack_limit(self):
        """Test limite stack comandi"""
        # Crea più comandi del limite (50)
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        for i in range(55):  # Superiamo il limite di 50
            old_pos = QPointF(i, 0)
            new_pos = QPointF(i + 1, 0)
            cmd = MoveItemCommand(item, old_pos, new_pos)
            self.command_manager.execute(cmd)
            
        # Verifica che lo stack sia limitato
        self.assertLessEqual(len(self.command_manager._undo_stack), 50)

    def test_redo_stack_clear(self):
        """Test pulizia stack redo dopo nuovo comando"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        
        # Crea e esegui un comando
        cmd1 = MoveItemCommand(item, QPointF(0, 0), QPointF(100, 0))
        self.command_manager.execute(cmd1)
        
        # Undo e poi nuovo comando
        self.command_manager.undo()
        self.assertTrue(len(self.command_manager._redo_stack) > 0)
        
        cmd2 = MoveItemCommand(item, QPointF(0, 0), QPointF(50, 0))
        self.command_manager.execute(cmd2)
        
        # Verifica che redo stack sia vuoto
        self.assertEqual(len(self.command_manager._redo_stack), 0)
        
    def test_move_command(self):
        """Test comando di movimento"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        initial_pos = item.pos()
        new_pos = QPointF(initial_pos.x() + 100, initial_pos.y())

        # Esegui comando
        command = MoveItemCommand(item, initial_pos, new_pos)
        self.window.command_manager.execute(command)
        self.assertEqual(item.pos(), new_pos)

        # Test undo
        self.window.command_manager.undo()
        self.assertEqual(item.pos(), initial_pos)