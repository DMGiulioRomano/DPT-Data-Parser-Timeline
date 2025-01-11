# tests/dialogs/test_dialogs.py
from tests.dialogs import (
    BaseTest, QTest, patch,
    DEFAULT_PARAMS,
    QColor
)
from src.ParamDialog import ParamDialog
from src.RenameDialog import RenameDialog
from unittest.mock import patch
from PyQt5.QtWidgets import QMessageBox

class DialogTest(BaseTest):
    def setUp(self):
        # Mock del QMessageBox.question per evitare il popup di autosave
        self.patcher = patch('PyQt5.QtWidgets.QMessageBox.question', return_value=QMessageBox.No)
        self.mock_question = self.patcher.start()
        super().setUp()

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()

    def test_param_dialog(self):
        """Test dialogo parametri"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        item.params['cAttacco'] = 0.0  # forza il tipo a float
        dialog = ParamDialog(item.params, QColor(100, 150, 200), item=item)

        # Test modifica parametri
        new_attack = 1.5
        dialog.inputs['cAttacco'].setText(str(new_attack))
        dialog.accept()
        self.assertEqual(item.params['cAttacco'], new_attack)

    def test_rename_dialog(self):
        """Test dialogo rinomina"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        dialog = RenameDialog(item)  # Passiamo l'item al dialog
        
        # Test rinomina
        new_name = "New Test Name"
        dialog.name_input.setText(new_name)
        dialog.accept()
        self.assertEqual(item.name, new_name)
        
    def test_param_validation(self):
        """Test validazione parametri"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        original_value = item.params['cAttacco']
        original_type = type(original_value)
        dialog = ParamDialog(item.params, QColor(100, 150, 200))

        # Test input invalido
        dialog.inputs['cAttacco'].setText("invalid")
        dialog.accept()
        
        # Verifica che il valore originale e il suo tipo siano mantenuti
        self.assertEqual(type(item.params['cAttacco']), original_type)
        self.assertEqual(item.params['cAttacco'], original_value)