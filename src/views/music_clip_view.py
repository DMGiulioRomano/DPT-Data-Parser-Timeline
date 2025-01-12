from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem

class MusicClipView(QGraphicsRectItem):
    """Vista grafica per un MusicClipModel"""
    def __init__(self, model, settings=None, track_height=40):
        super().__init__(0, 0, 0, track_height)
        self.model = model
        self.settings = settings
        self.track_height = track_height
        
        # Setup grafico base
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        
        # Colore di default e stile
        self.color = QColor(100, 150, 200)
        self.setBrush(self.color)
        self.setPen(QPen(Qt.black))
        
        # Testo
        self.text = QGraphicsTextItem(self.model.name, self)
        self.text.setPos(5, track_height/4)
        if settings:
            self.text.setDefaultTextColor(QColor(settings.get('text_color', '#000000')))
            self.updateTextStyle()
            
        # Connessione ai segnali del modello
        self.model.name_changed.connect(self.onNameChanged)
        self.model.params_changed.connect(self.onParamsChanged)
        self.model.position_changed.connect(self.onPositionChanged)
        
        # Flag per hover
        self.is_hovered = False

        self.highlight_color = QColor(255, 255, 0) 

    def setHighlighted(self, highlighted):
        self.highlighted = highlighted
        if highlighted:
            self.setBrush(self.highlight_color)
        else:
            self.setBrush(self.color)

    def onNameChanged(self, new_name):
        """Handler per cambio nome"""
        self.text.setPlainText(new_name)
        
    def onParamsChanged(self, param_name, value):
        """Handler per cambio parametri"""
        if param_name == "durata":
            if isinstance(value, (list, tuple)):
                width = float(value[0])
            else:
                width = float(value)
            # Calcola larghezza in pixel
            if self.scene():
                pixels_per_beat = self.scene().pixels_per_beat
                zoom_level = self.scene().zoom_level
                new_width = width * pixels_per_beat * zoom_level
                self.setRect(0, 0, new_width, self.rect().height())
                self.text.setPos(5, self.rect().height()/4)

    def onPositionChanged(self, x, y):
        """Handler per cambio posizione"""
        if not self.scene():
            return
        pixels_per_beat = self.scene().pixels_per_beat
        zoom_level = self.scene().zoom_level
        scene_x = x * pixels_per_beat * zoom_level
        scene_y = y
        self.setPos(scene_x, scene_y)

    def updateHeight(self, new_height):
        """Aggiorna l'altezza del clip e riscala il testo"""
        current_rect = self.rect()
        self.setRect(0, 0, current_rect.width(), new_height)
        
        if self.settings:
            # Calcola dimensione testo proporzionale
            base_text_size = self.settings.get('item_text_size', 12)
            height_ratio = new_height / 50
            new_text_size = max(8, min(base_text_size * height_ratio, 24))
            
            font = self.text.font()
            font.setPointSize(int(new_text_size))
            self.text.setFont(font)
            
            # Centra verticalmente
            text_height = self.text.boundingRect().height()
            vertical_center = (new_height - text_height) / 2
            self.text.setPos(5, vertical_center)

    def updateTextStyle(self):
        """Aggiorna lo stile del testo dalle impostazioni"""
        if self.settings:
            font = self.text.font()
            font.setPointSize(self.settings.get('item_text_size', 12))
            self.text.setFont(font)
            self.text.setDefaultTextColor(QColor(self.settings.get('text_color', '#000000')))

    def mousePressEvent(self, event):
        if event.modifiers() & Qt.MetaModifier:
            # Gestione modifica parametri
            if self.scene() and self.scene().views():
                view = self.scene().views()[0]
                if view and view.window():
                    view.window().showParamDialog(self.model)
            return
            
        super().mousePressEvent(event)
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            # Snap to grid
            newPos = value
            grid_size = (self.scene().pixels_per_beat * self.scene().zoom_level) / 16
            
            # Calcola posizione sulla griglia
            if newPos.x() < grid_size:
                grid_x = 0
            else:
                grid_x = round(newPos.x() / grid_size) * grid_size
                
            # Calcola traccia
            new_track = max(0, min(
                int(newPos.y() / self.scene().track_height),
                self.scene().num_tracks - 1
            ))
            track_y = new_track * self.scene().track_height
            
            # Aggiorna modello
            self.model.track_index = new_track
            beats_pos = grid_x / (self.scene().pixels_per_beat * self.scene().zoom_level)
            self.model.set_param('cAttacco', float(round(beats_pos, 3)))
            
            return QPointF(grid_x, track_y)
            
        return super().itemChange(change, value)
        
    def hoverEnterEvent(self, event):
        self.is_hovered = True
        self.update()
        super().hoverEnterEvent(event)
        
    def hoverLeaveEvent(self, event):
        self.is_hovered = False
        self.update()
        super().hoverLeaveEvent(event)
            
    def paint(self, painter, option, widget):
        original_brush = self.brush()

        if self.isSelected():
            lighter_color = self.color.lighter(140)
            self.setBrush(lighter_color)
        elif self.is_hovered:
            lighter_color = self.color.lighter(110)
            self.setBrush(lighter_color)
        elif hasattr(self, 'highlighted') and self.highlighted:
            highlight_color = QColor(255, 255, 0)  # Giallo per l'evidenziazione
            self.setBrush(highlight_color)

        if hasattr(self, 'highlighted') and self.highlighted:
            pen = QPen(QColor(255, 165, 0), 3)
            painter.setPen(pen)
            painter.drawRect(self.rect())

        super().paint(painter, option, widget)
        self.setBrush(original_brush)