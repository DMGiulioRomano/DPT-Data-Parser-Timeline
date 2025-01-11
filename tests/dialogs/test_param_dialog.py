# tests/dialogs/test_param_dialog.py
from tests.dialogs import (
    BaseTest, QTest, patch,  
    QEvent, QKeyEvent, QColor, Qt,
    DEFAULT_PARAMS
)
from src.ParamDialog import ParamDialog
from unittest.mock import patch
from PyQt5.QtWidgets import QMessageBox

class ParamDialogTest(BaseTest):
    def setUp(self):
        # Mock del QMessageBox.question per evitare il popup di autosave
        self.patcher = patch('PyQt5.QtWidgets.QMessageBox.question', return_value=QMessageBox.No)
        self.mock_question = self.patcher.start()
        super().setUp()

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()

    def test_color_selection(self):
        """Test selezione colore"""
        dialog = ParamDialog(DEFAULT_PARAMS)
        
        # Test aggiornamento colore
        new_color = QColor(255, 0, 0)
        dialog.color = new_color
        dialog.updateColorButton()
        
        self.assertEqual(dialog.color, new_color)
        
    def test_param_dialog(self):
        """Test dialogo parametri"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        dialog = ParamDialog(item.params, QColor(100, 150, 200))

        # Test modifica parametri
        new_attack = 1.5
        dialog.inputs['cAttacco'].setText(str(new_attack))
        dialog.accept()
        self.assertEqual(item.params['cAttacco'], new_attack)
        dialog = ParamDialog(item.params, QColor(100, 150, 200))
        new_dur = 1.5
        dialog.inputs['durata'].setText(str(new_dur))
        dialog.accept()
        self.assertEqual(item.params['durata'], new_dur)


    def test_key_events(self):
        """Test gestione eventi tastiera"""
        dialog = ParamDialog(DEFAULT_PARAMS, QColor(0,0,0))
        
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
        # Utilizzo il parametro 'ritmo' da DEFAULT_PARAMS che è una lista
        params = {'test_list': DEFAULT_PARAMS['ritmo']}
        dialog = ParamDialog(params, QColor(0,0,0))
        
        # Verifica formattazione lista
        self.assertEqual(
            dialog.inputs['test_list'].text(),
            '[7, 15]'
        )