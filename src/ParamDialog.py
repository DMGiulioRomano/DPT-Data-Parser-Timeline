import sys
import yaml
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont, QKeySequence
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView, 
    QGraphicsRectItem, QVBoxLayout, QPushButton, QDialog, 
    QFormLayout, QLineEdit, QDialogButtonBox, QWidget,
    QGraphicsTextItem, QGraphicsLineItem, QHBoxLayout, 
    QGraphicsItem, QFileDialog, QShortcut, QColorDialog
)

class ParamDialog(QDialog):
    def __init__(self, params,color=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Parameters")
        self.color = color or QColor(100, 150, 200)  # Default color        
        layout = QFormLayout()
        self.inputs = {}
        
        for key, value in params.items():
            if isinstance(value, list):
                self.inputs[key] = QLineEdit(str(value)[1:-1])
            else:
                self.inputs[key] = QLineEdit(str(value))
            layout.addRow(key, self.inputs[key])

        # Add color button
        self.colorButton = QPushButton("Choose Color")
        self.colorButton.clicked.connect(self.chooseColor)
        layout.addRow("Color", self.colorButton)
        self.updateColorButton()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def chooseColor(self):
        color = QColorDialog.getColor(self.color, self)
        if color.isValid():
            self.color = color
            self.updateColorButton()
    
    def updateColorButton(self):
        self.colorButton.setStyleSheet(
            f"background-color: {self.color.name()}; color: {'black' if self.color.lightness() > 128 else 'white'}"
        )

    def keyPressEvent(self, event):
        if (event.modifiers() & (Qt.ControlModifier | Qt.MetaModifier)) and event.key() == Qt.Key_W:
            self.reject()
        else:
            super().keyPressEvent(event)