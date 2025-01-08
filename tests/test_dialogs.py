# tests/test_dialogs.py
from base_test import BaseTest
from ParamDialog import ParamDialog
from RenameDialog import RenameDialog
from PyQt5.QtGui import QColor

class DialogTest(BaseTest):
    def test_param_dialog(self):
        """Test dialogo parametri"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        dialog = ParamDialog(item.params, QColor(100, 150, 200))
        
        # Test modifica parametri
        new_attack = 1.5
        dialog.inputs['cAttacco'].setText(str(new_attack))
        dialog.accept()
        self.assertEqual(float(item.params['cAttacco']), new_attack)

    def test_rename_dialog(self):
        """Test dialogo rinomina"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        dialog = RenameDialog()
        
        # Test rinomina
        new_name = "New Test Name"
        dialog.name_input.setText(new_name)
        dialog.accept()
        self.assertEqual(item.name, new_name)

    def test_param_validation(self):
        """Test validazione parametri"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        dialog = ParamDialog(item.params, QColor(100, 150, 200))
        
        # Test input invalido
        dialog.inputs['cAttacco'].setText("invalid")
        dialog.accept()
        # Verifica che il valore originale sia mantenuto
        self.assertEqual(type(item.params['cAttacco']), float)