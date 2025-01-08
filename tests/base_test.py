import unittest
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtTest import QTest

class BaseTest(unittest.TestCase):
    """Classe base per tutti i test che necessitano di QApplication"""
    
    @classmethod
    def setUpClass(cls):
        """Setup della classe di test"""
        # Inizializza l'applicazione Qt
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)
        
        # Imposta il flag per evitare la chiusura dell'app durante i test
        cls.app.setQuitOnLastWindowClosed(False)

    def setUp(self):
        """Setup per ogni test individuale"""
        from MainWindow import MainWindow
        self.window = MainWindow()
        self.timeline = self.window.scene
        # Assicurati che la finestra sia visibile
        self.window.show()
        # Processa gli eventi in sospeso
        QTest.qWaitForWindowExposed(self.window)
        
    def tearDown(self):
        """Cleanup dopo ogni test"""
        if hasattr(self, 'window'):
            self.window.close()
            self.window.deleteLater()
        # Processa gli eventi in sospeso
        QApplication.processEvents()

    @classmethod
    def tearDownClass(cls):
        """Cleanup finale"""
        if cls.app:
            cls.app.quit()
            
    def processEvents(self):
        """Utility per processare gli eventi Qt in sospeso"""
        QApplication.processEvents()