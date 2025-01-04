import sys
import yaml
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import (
    QGraphicsScene, QGraphicsTextItem
)
from MusicItem import MusicItem

class Timeline(QGraphicsScene):
    def __init__(self,settings):
        super().__init__()
        self.settings = settings
        self.min_width = 2000
        self.min_height = 600
        self.setSceneRect(0, -30, self.min_width, self.min_height)
        self.zoom_level = 1.0
        self.pixels_per_beat = 100
        self.min_grid_spacing = 20
        self.grid_height = 40
        self.track_height = 50
        self.num_tracks = 8
        self.draw_timeline()
        self.setBackgroundBrush(QBrush(QColor(220, 220, 220)))
        self.draw_tracks()
            
    def expand_timeline(self, x_pos):
        if x_pos > self.sceneRect().width() * 0.8:  # Expand when near edge
            new_width = max(self.sceneRect().width() * 1.5, x_pos * 1.2)
            self.setSceneRect(0, -30, new_width, 430)
            self.draw_timeline()
            self.draw_tracks()

    def draw_tracks(self):
        # Calculate required height based on number of tracks
        required_height = self.grid_height + (self.num_tracks * self.track_height) + self.track_height
        current_height = max(required_height, self.min_height)
        # Update scene rect if needed
        if current_height != self.sceneRect().height():
            self.setSceneRect(0, -30, self.sceneRect().width(), current_height)
            
        for i in range(self.num_tracks):
            y = self.grid_height + (i * self.track_height)
            # Track background
            rect = self.addRect(0, y, self.sceneRect().width(), self.track_height, 
                            QPen(Qt.black), QBrush(QColor(240, 240, 240)))
            # Track label
            text = QGraphicsTextItem(f"Track {i+1}")
            text.setPos(-70, y + 15)
            self.addItem(text)


    def add_music_item(self, seconds, track_number, duration=14, name="Clip", settings=None):
        if 0 <= track_number < self.num_tracks:
            x = seconds * self.pixels_per_beat * self.zoom_level  # Include zoom_level
            y = self.grid_height + (track_number * self.track_height)
            
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


    def scale_scene(self, factor):
        old_zoom = self.zoom_level
        self.zoom_level *= factor
        new_width = max(self.min_width * self.zoom_level, self.sceneRect().width())
        
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
                    'selected': item.isSelected(),  # Store selection state
                    'name': item.name,  # Store the name
                    'settings': item.settings  # Store the settings reference
                })

        # Mantieni le dimensioni attuali della scena quando la ridisegni
        current_height = self.sceneRect().height()
        self.clear()
        self.setSceneRect(0, -30, new_width, current_height)
        self.draw_timeline()
        self.draw_tracks()
        
        # Recreate items with preserved properties
        for item_data in stored_items:
            item = MusicItem(0, 0, item_data['width'], item_data['name'], item_data['settings'], self.track_height)  # Pass stored settings
            item.params = item_data['params']
            item.color = item_data['color']
            item.setBrush(item_data['color'])
            item.setPos(item_data['x'], item_data['y'])
            self.addItem(item)
            item.setSelected(item_data['selected'])  # Restore selection state


    def draw_timeline(self):
        self.clear()
        
        # Base spacing
        grid_spacing = self.pixels_per_beat * self.zoom_level
        width = int(self.sceneRect().width())
        
        # Determina l'intervallo in base allo zoom
        if self.zoom_level < 0.15:
            interval = 60
            subdivisions = 6  # Numero di stanghette intermedie        
        elif self.zoom_level < 0.2:
            interval = 30
            subdivisions = 6  # Numero di stanghette intermedie
        elif self.zoom_level < 0.75:
            interval = 10
            subdivisions = 5
        elif self.zoom_level < 1:
            interval = 5
            subdivisions = 5
        elif self.zoom_level < 3:
            interval = 1
            subdivisions = 4
        elif self.zoom_level < 5:
            interval = 0.5
            subdivisions = 4
        else:
            interval = 0.1
            subdivisions = 2
        
        # Disegna la griglia temporale
        current_time = 0
        current_sub_time = 0
        x = 0
        while x < width:
            # Disegna la stanghetta principale con il numero
            self.addLine(x, 0, x, self.grid_height, QPen(Qt.black, 2))
            text = QGraphicsTextItem(f"{current_time:.1f}")

            # Imposta la dimensione del testo usando le settings
            if self.settings:  # Controlla se le settings sono disponibili
                font = text.font()
                font.setPointSize(self.settings.get('timeline_text_size', 14))
                text.setFont(font)
            text.setDefaultTextColor(Qt.black)
            text.setPos(x - text.boundingRect().width()/2, -20)
            self.addItem(text)
            
            # Disegna le stanghette intermedie
            sub_interval = interval / subdivisions
            sub_spacing = grid_spacing * interval / subdivisions
            for i in range(1, subdivisions):
                sub_x = x + (i * sub_spacing)
                current_sub_time += sub_interval
                if sub_x < width:
                    # Stanghetta grigia più corta
                    self.addLine(sub_x, self.grid_height/2, sub_x, self.grid_height, 
                            QPen(QColor(150, 150, 150), 1))  # Grigio, più sottile
                    #text = QGraphicsTextItem(f"{current_sub_time:.2f}")
                    #text.setDefaultTextColor(Qt.black)
                    #text.setPos(sub_x - text.boundingRect().width()/2, -10)
                    #self.addItem(text)
            
            current_sub_time += sub_interval
            current_time += interval
            x += interval * grid_spacing
        
        # Linea principale
        self.addLine(0, self.grid_height, width, self.grid_height, QPen(Qt.black, 2))
        
        self.draw_tracks()