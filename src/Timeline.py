import sys
import yaml
from PyQt5.QtCore import Qt, QPointF, QTimer
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import (
    QGraphicsScene, QGraphicsTextItem, QGraphicsRectItem, QGraphicsItem,
    QApplication
)
from MusicItem import MusicItem
#from src.MusicItem import MusicItem

MIN_SCENE_HEIGHT = 600  # Sposta qui la costante

class Timeline(QGraphicsScene):
    def __init__(self,settings):
        super().__init__()
        self.settings = settings
        self.min_width = 2000
        self.min_height = MIN_SCENE_HEIGHT
        self.setSceneRect(0, 0, self.min_width, self.min_height)
        self.zoom_level = 1.0
        self.pixels_per_beat = 100
        self.min_grid_spacing = 20
        self.grid_height = 40
        self.track_height = 50
        self.num_tracks = self.settings.get('default_track_count', 8)
        self.setBackgroundBrush(QBrush(QColor(220, 220, 220)))
        self.draw_tracks()
        QTimer.singleShot(0,self.initialize_components)


    def initialize_components(self):
        """Inizializza e aggiorna tutti i componenti necessari"""
        if self.views():
            main_window = self.views()[0].window()
            if hasattr(main_window, 'timeline_container'):
                container = main_window.timeline_container
                
                # Aggiorna gli header delle tracce
                container.track_header_view.update_tracks(
                    self.num_tracks,
                    self.track_height
                )
                
                # Aggiorna e sincronizza il ruler
                if hasattr(container, 'ruler_view') and container.ruler_view:
                    ruler = container.ruler_view
                    ruler.update_zoom(self.zoom_level)
                    
                    # Sincronizza lo scroll orizzontale
                    if container.timeline_view:
                        current_scroll = container.timeline_view.horizontalScrollBar().value()
                        ruler.horizontalScrollBar().setValue(current_scroll)
                    
                    # Forza l'aggiornamento delle viste
                    ruler.viewport().update()
                    container.timeline_view.viewport().update()

    def draw_tracks(self):
        required_height = (self.num_tracks * self.track_height)
        current_height = max(required_height, self.min_height)
        
        if current_height != self.sceneRect().height():
            self.setSceneRect(0, 0, self.sceneRect().width(), current_height)
        
        track_color = self.settings.get('track_background_color', '#F0F0F0')
        
        for i in range(self.num_tracks):
            y = i * self.track_height
            track = TrackItem(0, y, self.sceneRect().width(), self.track_height, i)
            track.updateColors(track_color)  # Impostiamo i colori iniziali
            track.setPen(QPen(Qt.black))
            self.addItem(track)
            
            text = QGraphicsTextItem(f"Track {i+1}")
            text.setPos(-70, y + 15)
            self.addItem(text)
        # Aggiorna gli header nella view
        if self.views():
            view = self.views()[0]
            if view and view.window():
                main_window = view.window()
                if hasattr(main_window, 'timeline_container'):
                    main_window.timeline_container.track_header_view.update_tracks(
                        self.num_tracks,
                        self.track_height
                    )


    def delete_track(self, track_number):
        # Salva gli item di tutte le tracce
        track_items = []
        for i in range(self.num_tracks):
            items = []
            for item in self.items():
                if isinstance(item, MusicItem):
                    if item.pos().y() == i * self.track_height:
                        items.append({
                            'params': item.params.copy(),
                            'width': item.rect().width(),
                            'color': item.color,
                            'name': item.name,
                            'settings': item.settings
                        })
            track_items.append(items)
        
        # Rimuovi tutti gli item
        self.clear()
        
        # Decrementa il numero di tracce
        self.num_tracks -= 1
        
        # Ridisegna le tracce
        self.draw_tracks()
        
        # Ripristina gli item, saltando la traccia cancellata e spostando quelle successive verso l'alto
        for i in range(self.num_tracks + 1):
            if i == track_number:
                continue
            
            new_track = i if i < track_number else i - 1
            y = new_track * self.track_height
            
            for item_data in track_items[i]:
                item = MusicItem(0, 0, item_data['width'], item_data['name'], 
                            item_data['settings'], self.track_height)
                item.params = item_data['params']
                item.color = item_data['color']
                item.setBrush(item_data['color'])
                item.setPos(item.params['cAttacco'] * self.pixels_per_beat * self.zoom_level, y)
                self.addItem(item)
        # Aggiorna gli header dopo la cancellazione
        if self.views():
            main_view = self.views()[0]
            if hasattr(main_view, 'update_track_headers'):
                main_view.update_track_headers()
                

    def add_music_item(self, seconds, track_number, duration=14, name="Clip", settings=None):
        if 0 <= track_number < self.num_tracks:
            x = seconds * self.pixels_per_beat * self.zoom_level  # Include zoom_level
            y = track_number * self.track_height
            
            # Convert duration to width considering zoom_level
            if isinstance(duration, (list, tuple)):
                width = float(duration[0]) * self.pixels_per_beat * self.zoom_level
                duration_value = float(duration[0])
            else:
                width = float(duration) * self.pixels_per_beat * self.zoom_level
                duration_value = float(duration)
                
            item = MusicItem(0, 0, width, name, settings, self.track_height)
            item.track_index = track_number
            item.setPos(x, y)
            item.params['cAttacco'] = seconds  # Qui impostiamo l'attacco in beats/seconds
            item.params['durata'] = duration_value  # Imposta la durata
            self.addItem(item)
            return item

    def scale_track_height(self, factor):
        """
        Ridimensiona l'altezza delle tracce mantenendo le proporzioni
        Args:
            factor: fattore di scala (>1 per ingrandire, <1 per rimpicciolire)
        """
        # Calcola la nuova altezza delle tracce
        new_track_height = max(20, min(200, self.track_height * factor))  # Limiti min/max
        if new_track_height == self.track_height:
            return
            
        # Salva lo stato attuale degli item
        stored_items = []
        for item in self.items():
            if isinstance(item, MusicItem):
                stored_items.append({
                    'params': item.params.copy(),
                    'x': item.pos().x(),
                    'track_index': int(item.pos().y() / self.track_height),
                    'width': item.rect().width(),
                    'color': item.color,
                    'name': item.name,
                    'settings': item.settings
                })
        
        # Aggiorna l'altezza delle tracce
        self.track_height = new_track_height
        
        # Ricalcola l'altezza totale della scena
        required_height = self.num_tracks * self.track_height
        new_height = max(required_height, self.min_height)
        
        # Aggiorna la scena
        self.setSceneRect(0, 0, self.sceneRect().width(), new_height)
        self.clear()
        self.draw_tracks()
        
        # Ripristina gli item con le nuove proporzioni
        for item_data in stored_items:
            new_y = item_data['track_index'] * self.track_height
            item = MusicItem(0, 0, item_data['width'], item_data['name'], 
                            item_data['settings'], self.track_height)
            # Usa il nuovo metodo updateHeight per gestire il ridimensionamento
            item.updateHeight(self.track_height)
            item.params = item_data['params']
            item.color = item_data['color']
            item.setBrush(item_data['color'])
            item.setPos(item_data['x'], new_y)
            self.addItem(item)
        
        # Notifica il cambiamento agli altri componenti
        if self.views():
            main_window = self.views()[0].window()
            if hasattr(main_window, 'timeline_container'):
                container = main_window.timeline_container
                if hasattr(container, 'track_header_view'):
                    container.track_header_view.update_tracks(
                        self.num_tracks,
                        self.track_height
                    )

    def scale_scene(self, factor):
        self.zoom_level *= factor
        new_width = max(self.min_width * self.zoom_level, self.sceneRect().width())
        
        # Store reference mapping between old and new items
        item_references = {}
        
        # Store item data and selection state before clearing
        stored_items = []
        for item in self.items():
            if isinstance(item, MusicItem):
                stored_items.append({
                    'params': item.params.copy(),
                    'x': item.pos().x() * factor,
                    'y': item.pos().y(),
                    'width': item.rect().width() * factor,
                    'color': item.color,
                    'selected': item.isSelected(),
                    'name': item.name,
                    'settings': item.settings,
                    'original_item': item
                })

        # Update command manager references if needed
        if self.views():
            main_window = self.views()[0].window()
            if hasattr(main_window, 'command_manager'):
                for command in main_window.command_manager._undo_stack + main_window.command_manager._redo_stack:
                    for item_data in stored_items:
                        if hasattr(command, 'item') and command.item == item_data['original_item']:
                            # Aggiorniamo anche old_pos e new_pos nel comando
                            command.old_pos = QPointF(command.old_pos.x() * factor, command.old_pos.y())
                            command.new_pos = QPointF(command.new_pos.x() * factor, command.new_pos.y())
                            item_data['command'] = command

        current_height = self.sceneRect().height()
        self.clear()
        self.setSceneRect(0, 0, new_width, current_height)
        self.draw_tracks()
        
        # Recreate items with preserved properties
        for item_data in stored_items:
            item = MusicItem(0, 0, item_data['width'], item_data['name'], 
                            item_data['settings'], self.track_height)
            item.params = item_data['params']
            item.color = item_data['color']
            item.setBrush(item_data['color'])
            item.setPos(item_data['x'], item_data['y'])
            item.setSelected(item_data['selected'])
            self.addItem(item)
            
            # Update command reference if needed
            if 'command' in item_data:
                item_data['command'].item = item

        # Notifica il cambiamento di zoom al TimelineRuler
        if self.views():
            main_window = self.views()[0].window()
            if hasattr(main_window, 'timeline_container'):
                ruler = main_window.timeline_container.ruler_view.scene()
                if ruler:
                    ruler.update_zoom(self.zoom_level)



    def move_track(self, track_number, direction):
        """
        Sposta una traccia su o giù, portando con sé tutti i suoi item
        Args:
            track_number: il numero della traccia da spostare
            direction: -1 per su, 1 per giù
        """
        # Verifica che lo spostamento sia valido
        new_position = track_number + direction
        if new_position < 0 or new_position >= self.num_tracks:
            return

        # Raccogli tutti gli item e le loro informazioni per track_number e new_position
        items_on_tracks = {
            track_number: [],
            new_position: []
        }
        
        # Raccogli gli item su entrambe le tracce
        for item in self.items():
            if isinstance(item, MusicItem):
                current_track = int(item.pos().y() / self.track_height)
                if current_track in items_on_tracks:
                    items_on_tracks[current_track].append({
                        'params': item.params.copy(),
                        'width': item.rect().width(),
                        'color': item.color,
                        'name': item.name,
                        'settings': item.settings,
                        'pos_x': item.pos().x()
                    })

        # Pulisci la scena
        self.clear()
        self.draw_tracks()

        # Ridisegna gli item scambiando le posizioni y
        for track, items in items_on_tracks.items():
            new_y = new_position * self.track_height if track == track_number else track_number * self.track_height
            for item_data in items:
                item = MusicItem(0, 0, item_data['width'], item_data['name'], 
                            item_data['settings'], self.track_height)
                item.params = item_data['params']
                item.color = item_data['color']
                item.setBrush(item_data['color'])
                item.setPos(item_data['pos_x'], new_y)
                self.addItem(item)
                item.updateTextStyle()





class TrackItem(QGraphicsRectItem):
    def __init__(self, x, y, width, height, track_number):
        super().__init__(x, y, width, height)
        self.track_number = track_number
        self.setAcceptHoverEvents(True)
        self.base_color = None  # Colore di base dalla settings
        self.hover_color = None # Colore per hover
        
    def updateColors(self, base_color):
        self.base_color = QColor(base_color)
        self.setBrush(QBrush(self.base_color))
