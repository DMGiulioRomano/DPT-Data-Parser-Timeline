from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFileDialog, QTabWidget,
    QWidget, QColorDialog, QSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Settings")
        self.resize(600, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Crea il tab widget
        tab_widget = QTabWidget()
        
        # Tab per le directories
        directories_tab = QWidget()
        self.setup_directories_tab(directories_tab)
        tab_widget.addTab(directories_tab, "Directories")
        
        # Tab per lo stile del testo
        text_style_tab = QWidget()
        self.setup_text_style_tab(text_style_tab)
        tab_widget.addTab(text_style_tab, "Text Style")
        
        layout.addWidget(tab_widget)

        # Pulsanti OK/Cancel
        buttons = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)

    def setup_directories_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Directory per il comando make
        make_layout = QHBoxLayout()
        self.make_dir_edit = QLineEdit(self.settings.get('make_directory'))
        make_layout.addWidget(QLabel("Make Directory:"))
        make_layout.addWidget(self.make_dir_edit)
        browse_make_btn = QPushButton("Browse...")
        browse_make_btn.clicked.connect(lambda: self.browse_directory('make'))
        make_layout.addWidget(browse_make_btn)
        layout.addLayout(make_layout)

        # Directory di default per Open
        open_layout = QHBoxLayout()
        self.open_dir_edit = QLineEdit(self.settings.get('last_open_directory'))
        open_layout.addWidget(QLabel("Default Open Directory:"))
        open_layout.addWidget(self.open_dir_edit)
        browse_open_btn = QPushButton("Browse...")
        browse_open_btn.clicked.connect(lambda: self.browse_directory('open'))
        open_layout.addWidget(browse_open_btn)
        layout.addLayout(open_layout)

        # Directory di default per Save
        save_layout = QHBoxLayout()
        self.save_dir_edit = QLineEdit(self.settings.get('last_save_directory'))
        save_layout.addWidget(QLabel("Default Save Directory:"))
        save_layout.addWidget(self.save_dir_edit)
        browse_save_btn = QPushButton("Browse...")
        browse_save_btn.clicked.connect(lambda: self.browse_directory('save'))
        save_layout.addWidget(browse_save_btn)
        layout.addLayout(save_layout)

    def setup_text_style_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Text Color
        color_layout = QHBoxLayout()
        self.text_color = QColor(self.settings.get('text_color', '#000000'))
        self.color_button = QPushButton()
        self.update_color_button()
        color_layout.addWidget(QLabel("Text Color:"))
        color_layout.addWidget(self.color_button)
        self.color_button.clicked.connect(self.choose_color)
        layout.addLayout(color_layout)

        # Text Size
        size_layout = QHBoxLayout()
        self.text_size_spin = QSpinBox()
        self.text_size_spin.setRange(8, 72)
        self.text_size_spin.setValue(self.settings.get('text_size', 12))
        size_layout.addWidget(QLabel("Text Size:"))
        size_layout.addWidget(self.text_size_spin)
        layout.addLayout(size_layout)

        layout.addStretch()

    def update_color_button(self):
        self.color_button.setStyleSheet(
            f"background-color: {self.text_color.name()}; "
            f"color: {'black' if self.text_color.lightness() > 128 else 'white'}; "
            f"min-width: 60px; min-height: 30px;"
        )
        self.color_button.setText(self.text_color.name())

    def choose_color(self):
        color = QColorDialog.getColor(self.text_color, self)
        if color.isValid():
            self.text_color = color
            self.update_color_button()

    def keyPressEvent(self, event):
        if (event.modifiers() & (Qt.ControlModifier | Qt.MetaModifier)) and event.key() == Qt.Key_W:
            self.reject()
        else:
            super().keyPressEvent(event)

    def browse_directory(self, type_):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            if type_ == 'make':
                self.make_dir_edit.setText(dir_path)
            elif type_ == 'open':
                self.open_dir_edit.setText(dir_path)
            else:
                self.save_dir_edit.setText(dir_path)

    def accept(self):
        self.settings.set('make_directory', self.make_dir_edit.text())
        self.settings.set('last_open_directory', self.open_dir_edit.text())
        self.settings.set('last_save_directory', self.save_dir_edit.text())
        self.settings.set('text_color', self.text_color.name())
        self.settings.set('text_size', self.text_size_spin.value())
        super().accept()