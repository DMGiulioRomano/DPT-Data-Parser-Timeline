# tests/dialogs/test_param_dialog.py
from dialogs import (
    BaseTest, QTest, patch,  
    QEvent, QKeyEvent, QColor, Qt,
    ParamDialog, DEFAULT_PARAMS
)

class ParamDialogTest(BaseTest):
    def test_color_selection(self):
        """Test selezione colore"""
        dialog = ParamDialog(DEFAULT_PARAMS)
        
        # Test aggiornamento colore
        new_color = QColor(255, 0, 0)
        dialog.color = new_color
        dialog.updateColorButton()
        
        self.assertEqual(dialog.color, new_color)
        
    def test_parameter_validation(self):
        """Test validazione parametri"""
        dialog = ParamDialog(DEFAULT_PARAMS)
        
        # Test input valido
        dialog.inputs['cAttacco'].setText("1.5")
        dialog.accept()
        self.assertEqual(float(dialog.inputs['cAttacco'].text()), 1.5)
        
        # Test input non valido
        dialog.inputs['cAttacco'].setText("invalid")
        dialog.accept()
        self.assertNotEqual(dialog.inputs['cAttacco'].text(), "invalid")

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