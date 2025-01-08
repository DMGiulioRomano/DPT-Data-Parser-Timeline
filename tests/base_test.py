# tests/base_test.py
import unittest
from PyQt5.QtWidgets import QApplication
import sys
from MainWindow import MainWindow

class BaseTest(unittest.TestCase):
    """Classe base per tutti i test che necessitano di QApplication"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)

    def setUp(self):
        self.window = MainWindow()
        self.timeline = self.window.scene