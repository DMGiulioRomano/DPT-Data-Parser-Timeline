import yaml
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, 
    QFileDialog
)
from Timeline import Timeline
from TimelineView import TimelineView
from RenameDialog import RenameDialog
from MusicItem import MusicItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DPT - Delta Personal Timeline")
        self.setGeometry(100, 100, 1200, 600)
        self.current_file = None
        
        # Create menu bar
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        new_action = file_menu.addAction('&New')
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)
        
        open_action = file_menu.addAction('&Open')
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.load_from_yaml)
        
        save_action = file_menu.addAction('&Save')
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_to_yaml)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction('&Exit')
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu('&Edit')
        
        rename_action = edit_menu.addAction('&Rename Clip')

        #rename_action.setShortcut('Ctrl+R')
        rename_action.setShortcut(Qt.Key_Return)
        rename_action.triggered.connect(self.rename_selected_clips)
        save_as_action = file_menu.addAction('Save &As...')
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_as_yaml)
        # View menu
        view_menu = menubar.addMenu('&View')
        
        zoom_in_action = view_menu.addAction('Zoom &In')
        zoom_in_action.setShortcut('Ctrl++')
        zoom_in_action.triggered.connect(lambda: self.scene.scale_scene(1.2))
        
        zoom_out_action = view_menu.addAction('Zoom &Out')
        zoom_out_action.setShortcut('Ctrl+-')
        zoom_out_action.triggered.connect(lambda: self.scene.scale_scene(0.8))
        

                # Width modification shortcuts
        increase_width_action = view_menu.addAction('Increase Width')
        increase_width_action.setShortcut('Ctrl+Shift+Right')
        increase_width_action.triggered.connect(lambda: self.modify_item_width(1.2))

        decrease_width_action = view_menu.addAction('Decrease Width')
        decrease_width_action.setShortcut('Ctrl+Shift+Left')
        decrease_width_action.triggered.connect(lambda: self.modify_item_width(0.8))

        # Main widget setup
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Timeline view
        self.scene = Timeline()
        self.view = TimelineView(self.scene)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.view.setViewportMargins(70, 0, 0, 0)
        layout.addWidget(self.view)
        
        # Controls
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        
        zoom_in = QPushButton("Zoom In")
        zoom_out = QPushButton("Zoom Out")
        add_item = QPushButton("Add Item")
        save_button = QPushButton("Save")
        load_button = QPushButton("Load")
        
        zoom_in.clicked.connect(lambda: self.scene.scale_scene(1.2))
        zoom_out.clicked.connect(lambda: self.scene.scale_scene(0.8))
        add_item.clicked.connect(self.add_new_item)
        save_button.clicked.connect(self.save_to_yaml)
        load_button.clicked.connect(self.load_from_yaml)
        
        for btn in [zoom_in, zoom_out, add_item, save_button, load_button]:
            controls_layout.addWidget(btn)
            
        layout.addWidget(controls)
        self.setCentralWidget(central_widget)

    def modify_item_width(self, scale_factor):
        for item in self.scene.selectedItems():
            if isinstance(item, MusicItem):
                new_width = item.rect().width() * scale_factor
                item.params['durata'] = round(new_width / (self.scene.pixels_per_beat * self.scene.zoom_level),3)
                item.setRect(0, 0, new_width, item.rect().height())
                item.text.setPos(5, 10)

    def new_file(self):
        self.current_file = None
        self.scene.clear()
        self.scene.draw_timeline()
        self.scene.draw_tracks()
        self.update_window_title()


    def rename_selected_clips(self):
        selected_items = self.scene.selectedItems()
        if not selected_items:
            return
            
        dialog = RenameDialog(self)
        if dialog.exec_():
            new_name = dialog.name_input.text()
            for item in selected_items:
                if isinstance(item, MusicItem):
                    item.name = new_name
                    item.text.setPlainText(new_name)

    def add_new_item(self):
        viewport_center = self.view.mapToScene(
            self.view.viewport().width() // 2,
            self.view.viewport().height() // 2
        )
        
        track_number = max(0, min(
            int((viewport_center.y() - self.scene.grid_height) / self.scene.track_height),
            self.scene.num_tracks - 1
        ))
        
        x_pos = viewport_center.x()
        beats = x_pos / (self.scene.pixels_per_beat * self.scene.zoom_level)
        
        self.scene.add_music_item(beats, track_number, 3, "New Clip")

    def save_to_yaml(self):
        if not self.current_file:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save YAML", "", "YAML Files (*.yaml)")
            if file_path:
                self.current_file = file_path
        
        if self.current_file:
            items = []
            for item in self.scene.items():
                if isinstance(item, MusicItem):
                    params = item.params.copy()
                    params['ritmo'] = list(params['ritmo'])
                    params['ampiezza'] = list(params['ampiezza'])
                    params['frequenza'] = list(params['frequenza'])
                    items.append(params)
            
            with open(self.current_file, 'w') as f:
                yaml.dump({"comportamenti": items}, f, default_flow_style=None, sort_keys=False, indent=1)
            self.update_window_title()

    def load_from_yaml(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open YAML", "", "YAML Files (*.yaml)")
        if file_path:
            self.current_file = file_path  # Save the file path
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                
            self.scene.clear()
            self.scene.draw_timeline()
            self.scene.draw_tracks()
            
            for i, item_data in enumerate(data['comportamenti']):
                item = self.scene.add_music_item(
                    item_data['cAttacco'], 
                    i % self.scene.num_tracks,
                    item_data['durata']
                )
                item.params = item_data
            self.update_window_title()

    def save_as_yaml(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save YAML As", "", "YAML Files (*.yaml)")
        if file_path:
            self.current_file = file_path
            self.save_to_yaml()
            self.update_window_title()

    def increase_grid(self):
        self.scene.grid_division *= 2
        self.scene.draw_timeline()
        
    def decrease_grid(self):
        if self.scene.grid_division > 1:
            self.scene.grid_division //= 2
            self.scene.draw_timeline()

    def update_window_title(self):
        base_title = "DPT - Delta Personal Timeline"
        if self.current_file:
            self.setWindowTitle(f"{base_title} - {self.current_file}")
        else:
            self.setWindowTitle(base_title)
