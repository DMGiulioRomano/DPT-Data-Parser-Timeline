from PyQt5.QtWidgets import QGraphicsScene, QGraphicsTextItem
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPen, QColor, QBrush

class TimelineRuler(QGraphicsScene):
    zoom_changed = pyqtSignal(float)
    
    def __init__(self, settings, main_timeline):
        super().__init__()
        self.settings = settings
        self.main_timeline = main_timeline
        self.zoom_level = main_timeline.zoom_level
        self.pixels_per_beat = main_timeline.pixels_per_beat
        self.grid_height = 50
        self.total_height = 70  
        self.text_margin = 20  # Spazio per il testo superiore
        self.setSceneRect(0, 0, main_timeline.sceneRect().width(), self.total_height)
        self.updateColors()
        self.draw_ruler()
        
        # Connessione per aggiornamenti dalla timeline principale
        self.main_timeline.sceneRectChanged.connect(self.update_width)
        
    def update_width(self):
        """Aggiorna la larghezza del ruler quando la timeline principale cambia"""
        self.setSceneRect(0, 0, self.main_timeline.sceneRect().width(), self.total_height)
        self.draw_ruler()
        
    def draw_ruler(self):
        self.clear()
        grid_spacing = self.pixels_per_beat * self.zoom_level
        width = int(self.sceneRect().width())
        
        # Determina l'intervallo in base allo zoom
        if self.zoom_level < 0.05:
            interval = 60
            subdivisions = 2
        elif self.zoom_level < 0.15:
            interval = 60
            subdivisions = 6
        elif self.zoom_level < 0.2:
            interval = 30
            subdivisions = 6
        elif self.zoom_level < 0.75:
            interval = 10
            subdivisions = 5
        elif self.zoom_level < 1.25:
            interval = 5
            subdivisions = 5
        elif self.zoom_level < 3:
            interval = 1
            subdivisions = 4
        elif self.zoom_level < 4:
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
            self.addLine(x, self.total_height/2, x, self.total_height, QPen(Qt.black, 2))
            text = QGraphicsTextItem(f"{current_time:.1f}")
            
            # Imposta la dimensione del testo usando le settings
            if self.settings:
                font = text.font()
                font.setPointSize(self.settings.get('timeline_text_size', 14))
                text.setFont(font)
            text.setDefaultTextColor(Qt.black)
            text.setPos(x - text.boundingRect().width()/2, self.text_margin/2)
            self.addItem(text)
            
            # Disegna le stanghette intermedie
            sub_interval = interval / subdivisions
            sub_spacing = grid_spacing * interval / subdivisions
            
            for i in range(1, subdivisions):
                sub_x = x + (i * sub_spacing)
                current_sub_time += sub_interval
                
                if sub_x < width:
                    # Stanghetta grigia più corta
                    self.addLine(sub_x, self.grid_height, sub_x, self.total_height,
                               QPen(QColor(150, 150, 150), 1))  # Grigio, più sottile
                    
                    # Formatta il numero per le suddivisioni
                    s = int(current_sub_time) if current_sub_time == int(current_sub_time) else round(current_sub_time, 2)
                    text = QGraphicsTextItem(f"{s}")
                    
                    if self.settings:
                        font = text.font()
                        font.setPointSize(self.settings.get('timeline_text_size', 14)-3)  # Testo più piccolo per le suddivisioni
                        text.setFont(font)
                    text.setDefaultTextColor(Qt.black)
                    text.setPos(sub_x - text.boundingRect().width()/2, self.text_margin)
                    self.addItem(text)
            
            current_sub_time += sub_interval
            current_time += interval
            x += interval * grid_spacing
            
        # Linea principale orizzontale
        self.addLine(0, self.total_height, width, self.total_height, QPen(Qt.black, 2))

    def update_zoom(self, new_zoom):
        """Aggiorna il livello di zoom e ridisegna il ruler"""
        self.zoom_level = new_zoom
        self.draw_ruler()

    def updateColors(self):
        # Nuovo metodo per gestire l'aggiornamento dei colori
        background_color = self.settings.get('timeline_background_color', '#F0F0F0')
        self.setBackgroundBrush(QColor(background_color))