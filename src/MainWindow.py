import yaml
import subprocess
from pathlib import Path
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, 
    QFileDialog, QComboBox, QLineEdit, QLabel, QMessageBox, QTextEdit
)
from PyQt5.QtGui import QKeySequence  # Nuovo import
"""
from Timeline import *
from TimelineView import TimelineView
from RenameDialog import RenameDialog
from MusicItem import MusicItem
from Settings import Settings
from SettingsDialog import SettingsDialog
from Commands import CommandManager, ResizeItemCommand,SetPosCommand
from TimelineContainer import TimelineContainer
from TrackHeaderView import TrackHeaderItem

"""
from src.Timeline import *
from src.TimelineView import TimelineView
from src.RenameDialog import RenameDialog
from src.MusicItem import MusicItem
from src.Settings import Settings
from src.SettingsDialog import SettingsDialog
from src.Commands import CommandManager, ResizeItemCommand,SetPosCommand, MoveItemCommand
from src.TimelineContainer import TimelineContainer
from src.TrackHeaderView import TrackHeaderItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.command_manager = CommandManager()
        self.setWindowTitle("DPT - Delta Personal Timeline")
        self.setGeometry(100, 100, 1200, 600)
        self.current_file = None
        
        # Setup menus
        menubar = self.menuBar()
        self._setup_file_menu(menubar)
        self._setup_edit_menu(menubar)
        self._setup_view_menu(menubar)
        self._setup_help_menu(menubar)
        self._setup_settings_menu(menubar)
        
        # Main widget setup
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        self.selected_track = None
        self.scene = Timeline(self.settings)
        self.timeline_container = TimelineContainer(self.scene)
        layout.addWidget(self.timeline_container)
        self.timeline_container.track_header_view.scene.track_selection_changed.connect(self.on_track_selection_changed)
        # Search bar
        layout.addWidget(self._create_search_bar())
        
        # Bottom container for controls and log
        bottom_container = QWidget()
        bottom_layout = QHBoxLayout(bottom_container)
        
        # Controls on the left
        controls = self._create_controls()
        controls.setMaximumWidth(int(self.width() * 0.5))
        bottom_layout.addWidget(controls)
        
        # Log window on the right
        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)
        self.log_window.setMaximumHeight(100)
        bottom_layout.addWidget(self.log_window)
        
        layout.addWidget(bottom_container)
        self.setCentralWidget(central_widget)

        QTimer.singleShot(0, lambda: self.timeline_container.timeline_view.setFocus())

    def _create_search_bar(self):
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        
        self.search_param = QComboBox()
        self.search_param.addItems(['cAttacco', 'durataArmonica', 'ritmo', 'durata', 'ampiezza', 'frequenza', 'posizione'])
        
        self.search_value = QLineEdit()
        self.search_value.setPlaceholderText("Enter value to search...")
        self.search_value.returnPressed.connect(self.perform_search)
        
        clear_search_btn = QPushButton("Clear Search")
        clear_search_btn.clicked.connect(self.clear_search)
        
        search_layout.addWidget(QLabel("Search Parameter:"))
        search_layout.addWidget(self.search_param)
        search_layout.addWidget(QLabel("Value:"))
        search_layout.addWidget(self.search_value)
        search_layout.addWidget(clear_search_btn)
        
        return search_widget

    def _create_controls(self):
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        
        zoom_in = QPushButton("ZOOM IN")
        zoom_out = QPushButton("ZOOM OUT")
        add_item = QPushButton("Add Item")
        save_button = QPushButton("Save")
        load_button = QPushButton("Load")
        make_button = QPushButton("Make")
        
        zoom_in.clicked.connect(lambda: (
            self.scene.scale_scene(1.3),
            self.timeline_container.ruler_view.update_zoom(self.scene.zoom_level)
        ))
        zoom_out.clicked.connect(lambda: (
            self.scene.scale_scene(0.7),
            self.timeline_container.ruler_view.update_zoom(self.scene.zoom_level)
        ))
        add_item.clicked.connect(self.add_new_item)
        save_button.clicked.connect(self.save_to_yaml)
        load_button.clicked.connect(self.load_from_yaml)
        make_button.clicked.connect(self.run_make_command)
        
        for btn in [zoom_in, zoom_out, add_item, save_button, load_button, make_button]:
            controls_layout.addWidget(btn)
        
        return controls

    def _setup_file_menu(self, menubar):
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
        
        save_as_action = file_menu.addAction('Save &As...')
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_as_yaml)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction('&Exit')
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)

    def _setup_edit_menu(self, menubar):
        edit_menu = menubar.addMenu('&Edit')

        # Aggiungi i comandi Undo/Redo all'inizio del menu Edit
        undo_action = edit_menu.addAction('&Undo')
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.command_manager.undo)
        undo_action.setEnabled(False)
        self.undo_action = undo_action  
        
        redo_action = edit_menu.addAction('&Redo')
        redo_action.setShortcuts([QKeySequence.Redo, QKeySequence("Ctrl+Y"), QKeySequence("Ctrl+Shift+Z")])
        redo_action.triggered.connect(self.command_manager.redo)
        redo_action.setEnabled(False)
        self.redo_action = redo_action  
        
        edit_menu.addSeparator()  

        rename_action = edit_menu.addAction('&Rename Clip')
        rename_action.setShortcut(Qt.Key_Return)
        rename_action.triggered.connect(self.rename_selected_clips)
        
        new_item_action = edit_menu.addAction('New Item')
        new_item_action.setShortcut('Ctrl+1')
        new_item_action.triggered.connect(self.add_new_item)
        
        new_track_action = edit_menu.addAction('New Track')
        new_track_action.setShortcut('Ctrl+2')
        new_track_action.triggered.connect(self.add_new_track)
        
        delete_track_action = edit_menu.addAction('Delete Selected Track')
        delete_track_action.setShortcut('Alt+Del')
        delete_track_action.triggered.connect(self.delete_selected_track)
        
        param_dialog_action = edit_menu.addAction('Show Parameters')
        param_dialog_action.setShortcut('Ctrl+Return')
        param_dialog_action.triggered.connect(lambda: self.show_param_dialog_for_selected())
        
        # Movement actions
        move_right_action = edit_menu.addAction('Move Right')
        move_right_action.setShortcut('Ctrl+Right')
        move_right_action.triggered.connect(lambda: self.move_selected_items(1))
        
        move_left_action = edit_menu.addAction('Move Left')
        move_left_action.setShortcut('Ctrl+Left')
        move_left_action.triggered.connect(lambda: self.move_selected_items(-1))
        
        move_up_action = edit_menu.addAction('Move Item On Track Up')
        move_up_action.setShortcut('Ctrl+Up')
        move_up_action.triggered.connect(lambda: self.move_items_on_tracks(-1))
        
        move_down_action = edit_menu.addAction('Move Item On Track Down')
        move_down_action.setShortcut('Ctrl+Down')
        move_down_action.triggered.connect(lambda: self.move_items_on_tracks(1))

    def _setup_view_menu(self, menubar):
        view_menu = menubar.addMenu('&View')
        
        zoom_in_action = view_menu.addAction('Zoom &In')
        zoom_in_action.setShortcut('Ctrl++')
        zoom_in_action.triggered.connect(lambda: (
            self.scene.scale_scene(1.2),
            self.timeline_container.ruler_view.update_zoom(self.scene.zoom_level)
        ))
        
        zoom_out_action = view_menu.addAction('Zoom &Out')
        zoom_out_action.setShortcut('Ctrl+-')
        zoom_out_action.triggered.connect(lambda: (
            self.scene.scale_scene(0.8),
            self.timeline_container.ruler_view.update_zoom(self.scene.zoom_level)
        ))
        
        increase_width_action = view_menu.addAction('Increase Width')
        increase_width_action.setShortcut('Ctrl+Shift+Right')
        increase_width_action.triggered.connect(lambda: self.modify_item_width(1.2))
        
        decrease_width_action = view_menu.addAction('Decrease Width')
        decrease_width_action.setShortcut('Ctrl+Shift+Left')
        decrease_width_action.triggered.connect(lambda: self.modify_item_width(0.8))
        
        # Add View Log action
        view_log_action = view_menu.addAction('Show Log Window')
        view_log_action.setCheckable(True)
        view_log_action.setChecked(True)
        view_log_action.triggered.connect(lambda checked: self.log_window.setVisible(checked))

        increase_height_action = view_menu.addAction('Increase Track Height')
        increase_height_action.setShortcut('Ctrl+Shift+Up')
        increase_height_action.triggered.connect(lambda: self.modify_track_height(1.2))
        
        decrease_height_action = view_menu.addAction('Decrease Track Height')
        decrease_height_action.setShortcut('Ctrl+Shift+Down')
        decrease_height_action.triggered.connect(lambda: self.modify_track_height(0.8))

    def modify_track_height(self, factor):
        """Modifica l'altezza delle tracce"""
        self.scene.scale_track_height(factor)

    def _setup_settings_menu(self, menubar):
        settings_menu = menubar.addMenu('&Settings')
        settings_action = settings_menu.addAction('&Preferences')
        settings_action.setShortcut('Ctrl+,')
        settings_action.triggered.connect(self.show_settings_dialog)

    def _setup_help_menu(self, menubar):
        help_menu = menubar.addMenu('&Help')
        shortcuts_action = help_menu.addAction('Keyboard Shortcuts')
        shortcuts_action.triggered.connect(self.show_shortcuts)

    def show_shortcuts(self):
        shortcuts = """
        File:
        - New: Ctrl+N
        - Open: Ctrl+O  
        - Save: Ctrl+S
        - Save As: Ctrl+Shift+S
        - Exit: Ctrl+Q

        Edit:
        - Undo: Ctrl+Z
        - Redo: Ctrl+Y/Ctrl+Shift+Z
        - Rename Clip: Return
        - New Item: Ctrl+1  
        - New Track: Ctrl+2
        - Delete Track: Alt+Del
        - Show Parameters: Ctrl+Return
        - Duplicate: Ctrl+D

        Navigation:
        - Move Right: Ctrl+Right
        - Move Left: Ctrl+Left  
        - Move Track Up: Ctrl+Up
        - Move Track Down: Ctrl+Down

        View:
        - Zoom In: Ctrl++ 
        - Zoom Out: Ctrl+-
        - Increase Width: Ctrl+Shift+Right
        - Decrease Width: Ctrl+Shift+Left

        Settings:
        - Preferences: Ctrl+,
        """
        QMessageBox.information(self, "Keyboard Shortcuts", shortcuts)


    def log_message(self, message):
        """Aggiunge un messaggio alla finestra di log"""
        self.log_window.append(message)

    def run_make_command(self):
        try:
            make_dir = self.settings.get('make_directory')
            
            if not self.current_file:
                self.log_message("Nessun file YAML caricato/salvato. Carica o salva prima un file.")
                return

            yaml_filename = os.path.splitext(os.path.basename(self.current_file))[0]
            command = f"cd {make_dir} && make SEZIONE={yaml_filename}"

            self.log_message(f"Esecuzione comando: {command}")

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=True,
                cwd=make_dir
            )
            
            self.log_message("Make completato con successo!")
            self.log_message(f"Output:\n{result.stdout}")
            
        except subprocess.CalledProcessError as e:
            self.log_message("Errore nell'esecuzione del comando make:")
            self.log_message(f"Exit code: {e.returncode}")
            self.log_message(f"Output errore:\n{e.stderr}")
            self.log_message(f"Output standard:\n{e.stdout}")

    def add_new_track(self):
        self.scene.num_tracks += 1
        required_height = self.scene.num_tracks * self.scene.track_height
        current_height = max(required_height, self.scene.min_height)
        self.scene.setSceneRect(0, 0, self.scene.sceneRect().width(), current_height)
        
        stored_items = []
        for item in self.scene.items():
            if isinstance(item, MusicItem):
                stored_items.append({
                    'params': item.params.copy(),
                    'pos': item.pos(),
                    'width': item.rect().width(),
                    'color': item.color,
                    'name': item.name,
                    'settings': item.settings
                })
        
        self.scene.clear()
        self.scene.draw_tracks()
        
        for item_data in stored_items:
            item = MusicItem(0, 0, item_data['width'], item_data['name'], 
                        item_data['settings'], self.scene.track_height)
            item.params = item_data['params']
            item.color = item_data['color']
            item.setBrush(item_data['color'])
            item.setPos(item_data['pos'])
            self.scene.addItem(item)

    def delete_selected_track(self):
        """Elimina la traccia selezionata, sia dalla selezione dell'header che della traccia stessa"""
        # Controlla prima gli header selezionati
        selected_headers = [item for item in self.timeline_container.track_header_view.scene.items() 
                        if isinstance(item, TrackHeaderItem) and item.is_selected]
        
        if selected_headers:
            for header in selected_headers:
                self.scene.delete_track(header.track_number)
        else:
            # Comportamento esistente per la selezione della traccia
            for item in self.scene.selectedItems():
                if isinstance(item, TrackItem):
                    self.scene.delete_track(item.track_number)
                    break

    def set_item_pos(self, item, new_pos):
        old_pos = item.pos()
        command = SetPosCommand(item, old_pos, new_pos)
        self.command_manager.execute(command)


    def sort_items_by_attack(self, items):
        return sorted(items, key=lambda x: float(x['cAttacco']))

    def show_settings_dialog(self):
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_():
            stored_items = []
            for item in self.scene.items():
                if isinstance(item, MusicItem):
                    stored_items.append({
                        'params': item.params.copy(),
                        'pos': item.pos(),
                        'width': item.rect().width(),
                        'color': item.color,
                        'name': item.name,
                        'settings': item.settings
                    })
            
            self.scene.clear()
            self.scene.draw_tracks()
            self.timeline_container.ruler_scene.updateColors()
            self.timeline_container.ruler_scene.draw_ruler()
            
            for item_data in stored_items:
                item = MusicItem(0, 0, item_data['width'], item_data['name'], 
                            item_data['settings'], self.scene.track_height)
                item.params = item_data['params']
                item.color = item_data['color']
                item.setBrush(item_data['color'])
                item.setPos(item_data['pos'])
                self.scene.addItem(item)
                item.updateTextStyle()

    def show_param_dialog_for_selected(self):
        selected = self.scene.selectedItems()
        if selected and isinstance(selected[0], MusicItem):
            selected[0].showParamDialog()

    def move_items_on_tracks(self, direction):
        selected_items = self.scene.selectedItems()
        track_groups = {}
        
        for item in selected_items:
            if isinstance(item, MusicItem):
                current_y = item.pos().y()
                track_groups.setdefault(current_y, []).append(item)
        
        for y_pos, items in track_groups.items():
            current_track = int((y_pos) / self.scene.track_height)
            new_track = max(0, min(current_track + direction, self.scene.num_tracks - 1))
            new_y = (new_track * self.scene.track_height)
            
            for item in items:
                item.track_index = new_track
                item.setPos(item.pos().x(), new_y)



    def move_selected_items(self, direction):
        grid_size = (self.scene.pixels_per_beat / 16) / self.scene.zoom_level
        delta = grid_size * direction
        selected_items = [item for item in self.scene.selectedItems() if isinstance(item, MusicItem)]
        
        if direction > 0:
            for item in selected_items:
                old_pos = item.pos()
                new_x = old_pos.x() + delta
                current_track = int(old_pos.y() / self.scene.track_height)
                track_y = current_track * self.scene.track_height
                new_pos = QPointF(new_x, track_y)
                command = MoveItemCommand(item, old_pos, new_pos)
                self.command_manager.execute(command)
        else:
            for item in selected_items:
                old_pos = item.pos()
                new_x = max(0, old_pos.x() + delta)
                current_track = int(old_pos.y() / self.scene.track_height)
                track_y = current_track * self.scene.track_height
                new_pos = QPointF(new_x, track_y)
                command = MoveItemCommand(item, old_pos, new_pos)
                self.command_manager.execute(command)

    def modify_item_width(self, scale_factor):
        items = self.scene.selectedItems()
        if not items:
            return

        for item in items:
            if isinstance(item, MusicItem):
                old_width = item.rect().width()
                new_width = old_width * scale_factor

                command = ResizeItemCommand(item, old_width, new_width)
                self.command_manager.execute(command)

    def new_file(self):
        self.current_file = None
        self.scene.clear()
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

    def on_track_selection_changed(self, track_number, is_selected):
        if is_selected:
            self.selected_track = track_number
        else:
            self.selected_track = None

    def add_new_item(self):
        if self.selected_track is not None:
            self.scene.add_music_item(0, self.selected_track, 3, "New Clip", self.settings)
        else:
            track_number = 0
            self.scene.add_music_item(0, track_number, 3, "New Clip", self.settings)

    def save_to_yaml(self):
        if not self.current_file:
            last_dir = self.settings.get('last_save_directory')
            if not os.path.exists(last_dir):
                last_dir = self.settings.get('last_open_directory')
            
            if os.path.exists(last_dir):
                initial_dir = os.path.join(last_dir, '')
            else:
                initial_dir = ""

            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Save YAML", 
                initial_dir,
                "YAML Files (*.yaml)"
            )
            if file_path:
                self.current_file = file_path
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
            
            sorted_items = self.sort_items_by_attack(items)
            
            class CustomDumper(yaml.SafeDumper):
                def represent_sequence(self, tag, sequence, flow_style=None):
                    if len(sequence) > 0 and isinstance(sequence[0], list):
                        flow_style = True
                    return super().represent_sequence(tag, sequence, flow_style)
            
            try:
                with open(self.current_file, 'w') as f:
                    yaml.dump({"comportamenti": sorted_items}, f, 
                            Dumper=CustomDumper, 
                            default_flow_style=None, 
                            sort_keys=False, 
                            indent=1, 
                            allow_unicode=True)
                self.update_window_title()
                self.log_message(f"File salvato con successo: {self.current_file}")
            except Exception as e:
                self.log_message(f"Errore nel salvataggio del file: {e}")

    def load_from_yaml(self, test_mode=False):
        if not test_mode:
            last_dir = self.settings.get('last_open_directory')
            initial_dir = os.path.join(last_dir, '') if os.path.exists(last_dir) else ""
            file_path, _ = QFileDialog.getOpenFileName(self, "Open YAML", initial_dir, "YAML Files (*.yaml)")
        else:
            file_path = self.current_file

        if file_path:
            try:
                self.settings.set('last_open_directory', str(Path(file_path).parent))
                self.current_file = file_path
                
                with open(file_path, 'r') as f:
                    data = yaml.safe_load(f)

                self.scene.clear()
                self.scene.num_tracks = len(data['comportamenti'])
                self.scene.setSceneRect(0, 0, self.scene.sceneRect().width(),
                                        (self.scene.num_tracks * self.scene.track_height))
                self.scene.draw_tracks()

                for i, item_data in enumerate(data['comportamenti']):
                    processed_data = {}
                    for key, value in item_data.items():
                        if isinstance(value, list):
                            processed_value = [str(item) if isinstance(item, str) else item for item in value]
                            processed_data[key] = processed_value
                        else:
                            processed_data[key] = value

                    x_pos = round(float(processed_data['cAttacco']) * self.scene.pixels_per_beat * self.scene.zoom_level, 2)
                    width = float(processed_data['durata'][0] if isinstance(processed_data['durata'], (list, tuple)) 
                                else processed_data['durata'])
                    width *= round(self.scene.pixels_per_beat * self.scene.zoom_level, 2)
                    
                    item = MusicItem(0, 0, width, "Clip", self.settings, self.scene.track_height)
                    item.params = {k: (str(v) if isinstance(v, str) else v) for k, v in processed_data.items()}
                    item.setPos(x_pos, (i * self.scene.track_height))
                    self.scene.addItem(item)
                    item.updateTextStyle()

                self.update_window_title()
                self.log_message(f"File caricato con successo: {file_path}")
                
                for view in [self.timeline_container.timeline_view,
                            self.timeline_container.ruler_view,
                            self.timeline_container.track_header_view]:
                    view.viewport().update()

                current_scroll = self.timeline_container.timeline_view.horizontalScrollBar().value()
                self.timeline_container.ruler_view.horizontalScrollBar().setValue(current_scroll)

            except Exception as e:
                self.log_message(f"Errore nel caricamento del file: {e}")

    def save_as_yaml(self):
        last_dir = self.settings.get('last_save_directory')

        if not os.path.exists(last_dir):
            last_dir = self.settings.get('last_open_directory')

        if os.path.exists(last_dir):
            initial_dir = last_dir
        else:
            initial_dir = ""

        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save YAML As", 
            initial_dir,
            "YAML Files (*.yaml)"
        )
        
        if file_path:
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

    def update_undo_redo_actions(self):
        """Aggiorna lo stato dei pulsanti Undo/Redo"""
        if self.undo_action and self.redo_action:  # Verifica che esistano
            self.undo_action.setEnabled(self.command_manager.can_undo)
            self.redo_action.setEnabled(self.command_manager.can_redo)

    def update_track_headers(self):
        self.timeline_container.track_header_view.update_tracks(
            self.scene.num_tracks,
            self.scene.track_height
        )

    def update_window_title(self):
        base_title = "DPT - Delta Personal Timeline"
        if self.current_file:
            self.setWindowTitle(f"{base_title} - {self.current_file}")
        else:
            self.setWindowTitle(base_title)

    def closeEvent(self, event):
        # Controlla se ci sono modifiche non salvate confrontando il file corrente
        if self.current_file:
            # Mostra dialog di conferma
            reply = QMessageBox.question(
                self,
                'Salva Modifiche',
                'Ci sono modifiche non salvate. Vuoi salvare prima di uscire?',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Yes:
                self.save_to_yaml()
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return

        # Salva le ultime directory usate
        last_open = self.settings.get('last_open_directory')
        self.settings.set('last_save_directory', last_open)
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
                
    def perform_search(self):
        param = self.search_param.currentText()
        value = self.search_value.text()
        
        try:
            if value.startswith('[') and value.endswith(']'):
                search_value = eval(value)
            else:
                search_value = float(value)
                
            self.clear_search()
            
            for item in self.scene.items():
                if isinstance(item, MusicItem):
                    item_value = item.params.get(param)
                    
                    if isinstance(item_value, (list, tuple)) and isinstance(search_value, (list, tuple)):
                        if len(item_value) == len(search_value) and all(abs(a - b) < 0.001 for a, b in zip(item_value, search_value)):
                            item.highlighted = True
                    elif not isinstance(item_value, (list, tuple)) and not isinstance(search_value, (list, tuple)):
                        if abs(item_value - search_value) < 0.001:
                            item.highlighted = True
            
            self.scene.update()
            
        except (ValueError, SyntaxError) as e:
            self.log_message(f"Errore nella ricerca: {str(e)}")
            QMessageBox.warning(self, "Search Error", f"Invalid search value: {str(e)}")
            
    def clear_search(self):
        for item in self.scene.items():
            if isinstance(item, MusicItem):
                if hasattr(item, 'highlighted'):
                    item.highlighted = False
        self.scene.update()