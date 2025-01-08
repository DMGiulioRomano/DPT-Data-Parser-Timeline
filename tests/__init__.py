# tests/__init__.py
from .base_test import BaseTest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtTest import QTest

__all__ = [
    # Classi base e utilities per i test
    'BaseTest',
    'patch',
    'MagicMock',
    'QTest',
    
    # PyQt Widgets principali
    'QApplication',
    'QMainWindow',
    'QWidget',
    'QDialog',
    'QMessageBox',
    
    # PyQt Core
    'Qt',
    'QPoint',
    'QPointF',
    'QRect',
    'QRectF',
    'QSize',
    'QEvent',
    
    # PyQt Gui
    'QColor',
    'QPen',
    'QBrush',
    'QFont',
    'QKeyEvent',
    'QMouseEvent'
]