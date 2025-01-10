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

        # Tab per le impostazioni generali
        general_tab = QWidget()
        self.setup_general_tab(general_tab)
        tab_widget.addTab(general_tab, "General")

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

    def setup_general_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Numero di tracce di default
        tracks_layout = QHBoxLayout()
        self.default_tracks_spin = QSpinBox()
        self.default_tracks_spin.setRange(1, 50)  # Permettiamo da 1 a 50 tracce
        self.default_tracks_spin.setValue(self.settings.get('default_track_count', 8))
        tracks_layout.addWidget(QLabel("Default Number of Tracks:"))
        tracks_layout.addWidget(self.default_tracks_spin)
        layout.addLayout(tracks_layout)
        
        layout.addStretch()

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
        self.color_button.setFocusPolicy(Qt.NoFocus)  # Aggiungiamo questa riga
        self.update_color_button()
        color_layout.addWidget(QLabel("Text Color:"))
        color_layout.addWidget(self.color_button)
        self.color_button.clicked.connect(self.choose_color)
        layout.addLayout(color_layout)

        # Timeline Text Size
        timeline_size_layout = QHBoxLayout()
        self.timeline_text_size_spin = QSpinBox()
        self.timeline_text_size_spin.setRange(8, 72)
        self.timeline_text_size_spin.setValue(self.settings.get('timeline_text_size', 14))
        timeline_size_layout.addWidget(QLabel("Timeline Text Size:"))
        timeline_size_layout.addWidget(self.timeline_text_size_spin)
        layout.addLayout(timeline_size_layout)

        # Item Text Size
        item_size_layout = QHBoxLayout()
        self.item_text_size_spin = QSpinBox()
        self.item_text_size_spin.setRange(8, 72)
        self.item_text_size_spin.setValue(self.settings.get('item_text_size', 12))
        item_size_layout.addWidget(QLabel("Item Text Size:"))
        item_size_layout.addWidget(self.item_text_size_spin)
        layout.addLayout(item_size_layout)


        # Timeline Background Color
        timeline_color_layout = QHBoxLayout()
        self.timeline_color = QColor(self.settings.get('timeline_background_color', '#F0F0F0'))
        self.timeline_color_button = QPushButton()
        self.timeline_color_button.setFocusPolicy(Qt.NoFocus)  # Aggiungiamo questa riga
        self.update_timeline_color_button()
        timeline_color_layout.addWidget(QLabel("Timeline Background Color:"))
        timeline_color_layout.addWidget(self.timeline_color_button)
        self.timeline_color_button.clicked.connect(self.choose_timeline_color)
        layout.addLayout(timeline_color_layout)


        # Track Background Color
        track_color_layout = QHBoxLayout()
        self.track_color = QColor(self.settings.get('track_background_color', '#F0F0F0'))
        self.track_color_button = QPushButton()
        self.track_color_button.setFocusPolicy(Qt.NoFocus)  # Aggiungiamo questa riga
        self.update_track_color_button()
        track_color_layout.addWidget(QLabel("Track Background Color:"))
        track_color_layout.addWidget(self.track_color_button)
        self.track_color_button.clicked.connect(self.choose_track_color)
        layout.addLayout(track_color_layout)

        layout.addStretch()

    def choose_track_color(self):
        color = QColorDialog.getColor(self.track_color, self)
        if color.isValid():
            self.track_color = color
            self.update_track_color_button()

    def update_track_color_button(self):
        self.track_color_button.setStyleSheet(
            f"background-color: {self.track_color.name()}; "
            f"color: {'black' if self.track_color.lightness() > 128 else 'white'}; "
            f"min-width: 60px; min-height: 30px;"
        )
        self.track_color_button.setText(self.track_color.name())

    def choose_timeline_color(self):
        color = QColorDialog.getColor(self.timeline_color, self)
        if color.isValid():
            self.timeline_color = color
            self.update_timeline_color_button()

    def update_timeline_color_button(self):
        self.timeline_color_button.setStyleSheet(
            f"background-color: {self.timeline_color.name()}; "
            f"color: {'black' if self.timeline_color.lightness() > 128 else 'white'}; "
            f"min-width: 60px; min-height: 30px;"
        )
        self.timeline_color_button.setText(self.timeline_color.name())


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
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:  # Aggiungiamo questo elif
            self.accept()
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
        self.settings.set('item_text_size', self.item_text_size_spin.value())
        self.settings.set('timeline_text_size', self.timeline_text_size_spin.value())
        self.settings.set('track_background_color', self.track_color.name())
        self.settings.set('timeline_background_color', self.timeline_color.name())
        self.settings.set('default_track_count', self.default_tracks_spin.value())
        # Forza il ridisegno delle tracce con il nuovo colore
        self.settings.save_settings()
        if self.parent() and hasattr(self.parent(), 'timeline_container'):
            self.parent().timeline_container.timeline_view.scene().draw_tracks()
        super().accept()