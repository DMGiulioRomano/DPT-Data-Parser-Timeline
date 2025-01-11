# tests/dialogs/test_rename_dialog.py  
from tests.dialogs import BaseTest, QTest, patch
from src.RenameDialog import RenameDialog
from unittest.mock import patch
from PyQt5.QtWidgets import QMessageBox

class RenameDialogTest(BaseTest):
    def setUp(self):
        # Mock del QMessageBox.question per evitare il popup di autosave
        self.patcher = patch('PyQt5.QtWidgets.QMessageBox.question', return_value=QMessageBox.No)
        self.mock_question = self.patcher.start()
        super().setUp()

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()

    def test_dialog_validation(self):
        """Test validazione input"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        dialog = RenameDialog(item)
        
        # Test input vuoto
        with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning:
            dialog.name_input.setText("")
            dialog.accept()
            # Verifica che il warning sia stato mostrato
            mock_warning.assert_called_once()
            # Verifica che il dialog non sia stato accettato
            self.assertFalse(dialog.result())
        
        # Test input valido
        dialog.name_input.setText("Valid Name")
        dialog.accept()
        self.assertTrue(dialog.result())