import sys
import yaml
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import (
    QGraphicsScene, QGraphicsTextItem
)
from MusicItem import MusicItem

class Timeline(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.min_width = 2000
        self.setSceneRect(0, -30, self.min_width, 430)
        self.zoom_level = 1.0
        self.base_grid_division = 4
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
        for i in range(self.num_tracks):
            y = self.grid_height + (i * self.track_height)
            # Track background
            rect = self.addRect(0, y, self.sceneRect().width(), self.track_height, 
                              QPen(Qt.black), QBrush(QColor(240, 240, 240)))
            # Track label
            text = QGraphicsTextItem(f"Track {i+1}")
            text.setPos(-70, y + 15)
            self.addItem(text)

    def add_music_item(self, seconds, track_number, duration=14, name="Clip"):
        if 0 <= track_number < self.num_tracks:
            x = seconds * self.pixels_per_beat  # Convert seconds to pixels
            y = self.grid_height + (track_number * self.track_height)
            width = duration * self.pixels_per_beat  # Convert duration to width
            item = MusicItem(0, 0, width, name)
            item.setPos(x, y)
            self.addItem(item)
            return item

    """
    def calculate_grid_division(self):
        seconds_per_unit = 1 / max(0.1, self.zoom_level)
        
        if seconds_per_unit > 20:
            return max(1, self.base_grid_division // 8)
        elif seconds_per_unit > 10:
            return max(1, self.base_grid_division // 4)
        elif seconds_per_unit > 5:
            return max(1, self.base_grid_division // 2)
        elif self.zoom_level > 2:
            return self.base_grid_division * 2
        return max(1, self.base_grid_division)
        """
    def draw_timeline(self):
        self.clear()
        grid_division = max(1, self.calculate_grid_division())
        grid_spacing = max(1, int(self.pixels_per_beat * self.zoom_level / grid_division))
        
        # Main horizontal line
        self.addLine(0, self.grid_height, self.sceneRect().width(), self.grid_height, QPen(Qt.black, 2))
        
        width = int(self.sceneRect().width())
        
        for x in range(0, width, grid_spacing):
            beat_time = x / max(1, (self.pixels_per_beat * self.zoom_level))
            
            # Major lines and labels
            self.addLine(x, 0, x, self.grid_height, QPen(Qt.black, 2))
            text = QGraphicsTextItem(f"{beat_time:.1f}")
            text.setDefaultTextColor(Qt.black)
            text.setPos(x - text.boundingRect().width()/2, -20)
            self.addItem(text)


    def scale_scene(self, factor):
        old_zoom = self.zoom_level
        self.zoom_level *= factor
        new_width = max(self.min_width * self.zoom_level, self.sceneRect().width())
        
        # Store item data before clearing
        stored_items = []
        for item in self.items():
            if isinstance(item, MusicItem):
                stored_items.append({
                    'params': item.params.copy(),
                    'x': item.pos().x() * factor,
                    'y': item.pos().y(),
                    'width': item.rect().width() * factor
                })
        
        self.clear()
        self.setSceneRect(0, -30, new_width, 430)
        self.draw_timeline()
        self.draw_tracks()
        
        # Recreate items with new positions and sizes
        for item_data in stored_items:
            item = MusicItem(0, 0, item_data['width'])
            item.params = item_data['params']
            item.setPos(item_data['x'], item_data['y'])
            self.addItem(item)

    def calculate_grid_division(self):
        seconds_per_unit = 1 / max(0.1, self.zoom_level)
        
        if seconds_per_unit > 20:
            return 1
        elif seconds_per_unit > 10:
            return 2
        elif seconds_per_unit > 5:
            return 4
        elif self.zoom_level > 2:
            return 8
        return 4

    def snap_to_grid(self, x_pos):
        grid_spacing = max(1, self.pixels_per_beat * self.zoom_level / 4)  # Fixed division
        return round(x_pos / grid_spacing) * grid_spacing
