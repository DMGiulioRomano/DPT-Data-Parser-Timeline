from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox
)

class RenameDialog(QDialog):
    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rename Clip")
        self.item = item  # Salviamo riferimento all'item
        
        layout = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.setText(item.name)  # Mostra il nome corrente
        layout.addRow("New name:", self.name_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if (event.modifiers() & (Qt.ControlModifier | Qt.MetaModifier)) and event.key() == Qt.Key_W:
            self.reject()
        else:
            super().keyPressEvent(event)

    def accept(self):
        """Aggiorna il nome dell'item quando il dialog viene accettato"""
        new_name = self.name_input.text().strip()
        if new_name:  # Nome valido
            self.item.name = new_name
            self.item.text.setPlainText(new_name)
            super().accept()
        else:  # Nome vuoto - mostra warning
            QMessageBox.warning(
                self,
                "Invalid Name",
                "The clip name cannot be empty.",
                QMessageBox.Ok
            )