import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys

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
        try:
            # Importiamo qui per evitare problemi di importazione circolare
            from src.MainWindow import MainWindow
            self.window = MainWindow()
            self.timeline = self.window.scene
            # Assicurati che la finestra sia visibile
            self.window.show()
        except Exception as e:
            print(f"Error in setUp: {str(e)}")
            raise

    def tearDown(self):
        """Cleanup dopo ogni test"""
        if hasattr(self, 'window'):
            self.window.hide()  # Nascondi prima di chiudere
            self.window.deleteLater()
        # Processa gli eventi pendenti
        self.app.processEvents()

    @classmethod
    def tearDownClass(cls):
        """Cleanup finale"""
        # Non chiudiamo l'app qui, altrimenti i test successivi falliranno
        pass