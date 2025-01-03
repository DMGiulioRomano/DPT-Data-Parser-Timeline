import yaml
import subprocess
from pathlib import Path
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, 
    QFileDialog
)
from Timeline import Timeline
from TimelineView import TimelineView
from RenameDialog import RenameDialog
from MusicItem import MusicItem
from Settings import Settings
from SettingsDialog import SettingsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
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
        
        settings_menu = menubar.addMenu('&Settings')
        settings_action = settings_menu.addAction('&Preferences')
        settings_action.setShortcut('Ctrl+,')
        settings_action.triggered.connect(self.show_settings_dialog)

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
        # Add to MainWindow.__init__ after other shortcuts
        move_right_action = edit_menu.addAction('Move Right')
        move_right_action.setShortcut('Ctrl+Right')  # Command/Meta + Right arrow
        move_right_action.triggered.connect(lambda: self.move_selected_items(1))

        move_left_action = edit_menu.addAction('Move Left')
        move_left_action.setShortcut('Ctrl+Left')  # Command/Meta + Left arrow
        move_left_action.triggered.connect(lambda: self.move_selected_items(-1))  

        move_up_action = edit_menu.addAction('Move Track Up')
        move_up_action.setShortcut('Ctrl+Up')
        move_up_action.triggered.connect(lambda: self.move_tracks(-1))

        move_down_action = edit_menu.addAction('Move Track Down')
        move_down_action.setShortcut('Ctrl+Down')
        move_down_action.triggered.connect(lambda: self.move_tracks(1))

        new_item_action = edit_menu.addAction('New Item')
        new_item_action.setShortcut('Ctrl+T')
        new_item_action.triggered.connect(self.add_new_item)

        param_dialog_action = edit_menu.addAction('Show Parameters')
        param_dialog_action.setShortcut('Ctrl+Return')
        param_dialog_action.triggered.connect(lambda: self.show_param_dialog_for_selected())

        make_button = QPushButton("Make")
        make_button.clicked.connect(self.run_make_command)
        
        for btn in [zoom_in, zoom_out, add_item, save_button, load_button,make_button]:
            controls_layout.addWidget(btn)
            
        layout.addWidget(controls)
        self.setCentralWidget(central_widget)


    def run_make_command(self):
        try:
            make_dir = self.settings.get('make_directory')
            
            # Controlla se c'è un file corrente
            if not self.current_file:
                print("Nessun file YAML caricato/salvato. Carica o salva prima un file.")
                return

            # Ottieni il nome del file senza estensione
            yaml_filename = os.path.splitext(os.path.basename(self.current_file))[0]

            # Costruisci il comando make con la SEZIONE
            command = f"cd {make_dir} && make SEZIONE={yaml_filename}"

            print(f"Esecuzione comando: {command}")

            # Esegui il comando
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=True,
                cwd=make_dir  # Imposta la directory di lavoro
            )
            
            print("Make completato con successo!")
            print("Output:", result.stdout)
            
        except subprocess.CalledProcessError as e:
            print("Errore nell'esecuzione del comando make:")
            print("Exit code:", e.returncode)
            print("Output errore:", e.stderr)
            print("Output standard:", e.stdout)


    def show_settings_dialog(self):
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_():
            self.update_all_items_style()  # Aggiorna lo stile dopo che le impostazioni sono cambiat
            
    def show_param_dialog_for_selected(self):
        selected = self.scene.selectedItems()
        if selected and isinstance(selected[0], MusicItem):
            selected[0].showParamDialog()

    def move_tracks(self, direction):
        selected_items = self.scene.selectedItems()
        
        # Raggruppa gli item per track corrente
        track_groups = {}
        for item in selected_items:
            if isinstance(item, MusicItem):
                current_y = item.pos().y()
                track_groups.setdefault(current_y, []).append(item)
        
        # Muovi ogni gruppo separatamente
        for y_pos, items in track_groups.items():
            current_track = int((y_pos - self.scene.grid_height) / self.scene.track_height)
            new_track = max(0, min(current_track + direction, self.scene.num_tracks - 1))
            new_y = self.scene.grid_height + (new_track * self.scene.track_height)
            
            for item in items:
                item.track_index = new_track
                item.setPos(item.pos().x(), new_y)



    def move_selected_items(self, direction):
        grid_size = (self.scene.pixels_per_beat * self.scene.zoom_level) / 16
        delta = grid_size * direction
            
        for item in self.scene.selectedItems():
            if isinstance(item, MusicItem):
                new_x = item.pos().x() + delta
                item.setPos(new_x, item.pos().y())
                item.params['cAttacco'] = new_x / (self.scene.pixels_per_beat * self.scene.zoom_level)

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
        
        self.scene.add_music_item(beats, track_number, 3, "New Clip", self.settings)


    def save_to_yaml(self):
        if not self.current_file:
            # Ottieni il percorso come stringa dal settings
            last_dir = self.settings.get('last_save_directory')
            if not os.path.exists(last_dir):
                last_dir = self.settings.get('last_open_directory')
            
            # Verifica che il percorso esista
            if os.path.exists(last_dir):
                initial_dir = os.path.join(last_dir, '')  # Aggiungi separatore alla fine
            else:
                initial_dir = ""  # fallback alla directory corrente

            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Save YAML", 
                initial_dir,
                "YAML Files (*.yaml)"
            )
            if file_path:
                self.current_file = file_path
                # Aggiorna il last_save_directory con il nuovo percorso
                self.settings.set('last_save_directory', str(Path(file_path).parent))
        
        if self.current_file:
            items = []
            for item in self.scene.items():
                if isinstance(item, MusicItem):
                    params = {
                        key: value[:] if isinstance(value, list) else value 
                        for key, value in item.params.items()
                    }
                    items.append(params)
            
            try:
                with open(self.current_file, 'w') as f:
                    yaml.dump({"comportamenti": items}, f, default_flow_style=None, sort_keys=False, indent=1, allow_unicode=True)
                self.update_window_title()
            except Exception as e:
                print(f"Errore nel salvataggio del file: {e}")


    def load_from_yaml(self):
        last_dir = self.settings.get('last_open_directory')

        if os.path.exists(last_dir):
            initial_dir = os.path.join(last_dir, '')  # Aggiungi separatore alla fine
        else:
            initial_dir = ""  # fallback alla directory corrente

        file_path, _ = QFileDialog.getOpenFileName(self, "Open YAML", initial_dir, "YAML Files (*.yaml)")


        if file_path:
            self.settings.set('last_open_directory', str(Path(file_path).parent))
            self.current_file = file_path
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                
            self.scene.clear()
            self.scene.num_tracks = len(data['comportamenti'])
            self.scene.setSceneRect(0, -30, self.scene.sceneRect().width(), 
                                self.scene.grid_height + (self.scene.num_tracks * self.scene.track_height))
            
            self.scene.draw_timeline()
            self.scene.draw_tracks()
            
            for i, item_data in enumerate(data['comportamenti']):
                x_pos = round(float(item_data['cAttacco']) * self.scene.pixels_per_beat * self.scene.zoom_level,2)
                width = float(item_data['durata'][0] if isinstance(item_data['durata'], (list, tuple)) else item_data['durata'])
                width *= round(self.scene.pixels_per_beat * self.scene.zoom_level,2)
                
                item = MusicItem(0, 0, width, "Clip", self.settings)
                item.params = item_data
                item.setPos(x_pos, self.scene.grid_height + (i * self.scene.track_height))
                self.scene.addItem(item)
                
            self.update_window_title()  

    def save_as_yaml(self):
        # Ottieni il percorso come stringa dal settings
        last_dir = self.settings.get('last_save_directory')

        if not os.path.exists(last_dir):
            last_dir = self.settings.get('last_open_directory')

        # Verifica che il percorso esista
        if os.path.exists(last_dir):
            initial_dir = last_dir
        else:
            initial_dir = ""  # fallback alla directory corrente

        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save YAML As", 
            initial_dir,
            "YAML Files (*.yaml)"
        )
        
        if file_path:
            # Aggiorna il last_save_directory con il nuovo percorso
            self.settings.set('last_save_directory', str(Path(file_path).parent))
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

    def closeEvent(self, event):
        # Resetta last_save_directory al valore di last_open_directory
        last_open = self.settings.get('last_open_directory')
        self.settings.set('last_save_directory', last_open)
        # Chiama l'evento di chiusura della classe padre
        super().closeEvent(event)

    def update_all_items_style(self):
        for item in self.scene.items():
            if isinstance(item, MusicItem):
                item.updateTextStyle()

    def delete_selected_items(self):
        selected_items = self.scene.selectedItems()
        for item in selected_items:
            if isinstance(item, MusicItem):
                self.scene.removeItem(item)