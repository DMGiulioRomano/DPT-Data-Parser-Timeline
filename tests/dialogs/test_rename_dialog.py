# tests/dialogs/test_rename_dialog.py  
from tests.dialogs import BaseTest, QTest
from src.RenameDialog import RenameDialog

class RenameDialogTest(BaseTest):
    def test_dialog_validation(self):
        """Test validazione input"""
        dialog = RenameDialog()
        
        # Test input vuoto
        dialog.name_input.setText("")
        dialog.accept()
        self.assertFalse(dialog.result())
        
        # Test input valido
        dialog.name_input.setText("Valid Name")
        dialog.accept()
        self.assertTrue(dialog.result())