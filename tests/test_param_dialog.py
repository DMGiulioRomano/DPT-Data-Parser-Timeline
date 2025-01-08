# tests/test_param_dialog.py
from base_test import BaseTest
from ParamDialog import ParamDialog
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class ParamDialogTest(BaseTest):
    def test_color_selection(self):
        """Test selezione colore"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        dialog = ParamDialog(item.params)
        
        # Test aggiornamento colore
        new_color = QColor(255, 0, 0)
        dialog.color = new_color
        dialog.updateColorButton()
        
        self.assertEqual(dialog.color, new_color)
        
    def test_parameter_validation(self):
        """Test validazione parametri"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        dialog = ParamDialog(item.params)
        
        # Test input valido
        dialog.inputs['cAttacco'].setText("1.5")
        dialog.accept()
        self.assertEqual(item.params['cAttacco'], 1.5)
        
        # Test input non valido
        dialog.inputs['cAttacco'].setText("invalid")
        dialog.accept()
        self.assertNotEqual(item.params['cAttacco'], "invalid")

    def test_key_events(self):
        """Test gestione eventi tastiera"""
        dialog = ParamDialog({}, QColor(0,0,0))
        
        # Test chiusura con Ctrl+W
        event = QKeyEvent(
            QEvent.KeyPress, 
            Qt.Key_W, 
            Qt.ControlModifier
        )
        dialog.keyPressEvent(event)
        self.assertFalse(dialog.result())
        
    def test_parameter_list_handling(self):
        """Test gestione parametri lista"""
        params = {'test_list': [1, 2, 3]}
        dialog = ParamDialog(params, QColor(0,0,0))
        
        # Verifica formattazione lista
        self.assertEqual(
            dialog.inputs['test_list'].text(),
            '[1, 2, 3]'
        )