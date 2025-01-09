# tests/dialogs/test_rename_dialog.py  
from tests.dialogs import BaseTest, QTest, patch
from src.RenameDialog import RenameDialog

class RenameDialogTest(BaseTest):
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