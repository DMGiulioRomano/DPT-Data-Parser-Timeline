import unittest
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtCore import Qt, QEvent, QPoint
import sys
from unittest.mock import patch, MagicMock
import os

class BaseTest(unittest.TestCase):
    """Classe base per tutti i test che necessitano di QApplication"""
    
    @classmethod
    def setUpClass(cls):
        """Setup della classe di test"""
        # Controllo se esiste già un'istanza di QApplication
        cls.app = QApplication.instance()
        if cls.app is None:
            # Crea una nuova istanza solo se non esiste
            cls.app = QApplication([])
            
    def setUp(self):
        """Setup per ogni test individuale"""
        self.temp_files = []  # Lista dei file temporanei creati
        try:
            # Importiamo qui per evitare problemi di importazione circolare
            from src.MainWindow import MainWindow
            self.window = MainWindow()
            self.timeline = self.window.scene
            # Assicurati che la finestra sia visibile
            self.window.hide()
            # Processa gli eventi immediatamente dopo la creazione
            self.app.processEvents()
        except Exception as e:
            print(f"Error in setUp: {str(e)}")
            raise


    def tearDown(self):
        """Cleanup dopo ogni test"""
        if hasattr(self, 'window'):
            try:
                # Nascondi prima di chiudere
                self.window.hide()
                
                # Chiudi esplicitamente
                self.window.close()
                
                # Schedula la deletion
                self.window.deleteLater()
                
                # Processa gli eventi pendenti
                self.app.processEvents()
                
                # Rimuovi i riferimenti
                self.window = None
                self.timeline = None
                
            except Exception as e:
                print(f"Warning in tearDown: {str(e)}")
        if hasattr(self, 'temp_files'):
            for file_path in self.temp_files:
                try:
                    os.remove(file_path)
                except OSError:
                    pass


    @classmethod
    def tearDownClass(cls):
        """Cleanup finale"""
        # Non chiudiamo l'app qui, altrimenti i test successivi falliranno
        pass

    def mock_message_box(self, return_value=QMessageBox.No):
        """Helper per effettuare il mocking di QMessageBox.question"""
        patcher = patch('PyQt5.QtWidgets.QMessageBox.question', return_value=return_value)
        patcher.start()
        self.addCleanup(patcher.stop)

    def simulate_event(self, widget, event_type, **kwargs):
        """Helper per simulare eventi Qt"""
        if event_type == QEvent.MouseButtonPress:
            # Crea evento mouse
            event = QMouseEvent(
                QEvent.MouseButtonPress,
                kwargs.get('pos', QPoint()),
                kwargs.get('button', Qt.LeftButton),
                kwargs.get('buttons', Qt.LeftButton),
                kwargs.get('modifiers', Qt.NoModifier)
            )
        elif event_type == QEvent.KeyPress:
            # Crea evento tastiera
            event = QKeyEvent(
                QEvent.KeyPress,
                kwargs.get('key', 0),
                kwargs.get('modifiers', Qt.NoModifier),
                kwargs.get('text', '')
            )
        
        QApplication.postEvent(widget, event)
        QApplication.processEvents()

    def verify_signal_emitted(self, signal, callback=None, timeout=1000):
        """Helper per verificare l'emissione di segnali"""
        signal_received = False
        def slot(*args):
            nonlocal signal_received
            signal_received = True
            if callback:
                callback(*args)
        
        signal.connect(slot)
        QApplication.processEvents(timeout)
        signal.disconnect(slot)
        return signal_received

    def create_temp_file(self, content="", suffix=".yaml"):
        """Helper per creare file temporanei per i test"""
        import tempfile
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        temp.write(content.encode())
        temp.close()
        self.temp_files.append(temp.name)
        return temp.name