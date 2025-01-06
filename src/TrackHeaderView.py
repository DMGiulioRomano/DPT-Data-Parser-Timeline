from PyQt5.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, 
    QGraphicsTextItem, QGraphicsItem, QLineEdit
)
from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QPen, QColor, QBrush, QFont, QPainter

class EditableTextItem(QGraphicsTextItem):
    """Testo editabile per l'header della traccia"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setDefaultTextColor(Qt.black)
        self.setTextWidth(60)  # Limita la larghezza del testo
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.setAcceptHoverEvents(True)
        
    def mouseDoubleClickEvent(self, event):
        """Attiva l'editing quando si fa doppio click"""
        editor = QLineEdit(self.toPlainText())
        editor.setStyleSheet("background: white; padding: 2px;")
        
        # Posiziona l'editor nella view
        view = self.scene().views()[0]
        scene_pos = self.scenePos()
        view_pos = view.mapFromScene(scene_pos)
        editor.move(view.viewport().mapToGlobal(view_pos.toPoint()))
        editor.resize(60, 25)
        
        def finish_editing():
            new_text = editor.text()
            if new_text:
                self.setPlainText(new_text)
            editor.deleteLater()
            
        editor.editingFinished.connect(finish_editing)
        editor.show()
        editor.setFocus()

class TrackHeaderItem(QGraphicsRectItem):
    """Rappresenta l'header di una singola traccia"""
    def __init__(self, x, y, width, height, track_number):
        super().__init__(x, y, width, height)
        self.track_number = track_number
        self.setAcceptHoverEvents(True)
        self.base_color = QColor(240, 240, 240)
        self.hover_color = QColor(220, 220, 220)
        self.selected_color = QColor(200, 200, 220)
        self.is_selected = False
        self.setBrush(QBrush(self.base_color))
        self.setPen(QPen(Qt.black))
        
        # Aggiungi il testo editabile
        self.text = EditableTextItem(f"Track {track_number + 1}", self)
        # Centra il testo verticalmente
        text_y = (height - self.text.boundingRect().height()) / 2
        self.text.setPos(5, text_y)

    def hoverEnterEvent(self, event):
        if not self.is_selected:
            self.setBrush(QBrush(self.hover_color))
        super().hoverEnterEvent(event)
        
    def hoverLeaveEvent(self, event):
        if not self.is_selected:
            self.setBrush(QBrush(self.base_color))
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        scene = self.scene()
        if scene:
            # Gestisci la selezione multipla con CTRL/CMD
            if not (event.modifiers() & Qt.ControlModifier):
                for item in scene.items():
                    if isinstance(item, TrackHeaderItem):
                        item.setSelected(False)
            self.setSelected(not self.is_selected)
        super().mousePressEvent(event)

    def setSelected(self, selected):
        self.is_selected = selected
        self.setBrush(QBrush(self.selected_color if selected else self.base_color))
        # Emetti il segnale attraverso la scena
        if self.scene():
            self.scene().track_selection_changed.emit(self.track_number, selected)

class TrackHeaderScene(QGraphicsScene):
    """Scena che contiene gli header delle tracce"""
    track_selection_changed = pyqtSignal(int, bool)  # (track_number, is_selected)

    def __init__(self):
        super().__init__()
        self.setBackgroundBrush(QBrush(QColor(240, 240, 240)))
        self.header_items = []

class TrackHeaderView(QGraphicsView):
    """Vista principale per gli header delle tracce"""
    def __init__(self, timeline_view=None):
        self.scene = TrackHeaderScene()
        super().__init__(self.scene)
        self.timeline_view = timeline_view  # Salviamo il riferimento alla timeline
        self.setFixedWidth(70)  # Larghezza fissa per gli header
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setRenderHint(QPainter.Antialiasing)
        self.setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)
        self.viewport().setContentsMargins(0, 0, 0, 0)
        self.scene.setSceneRect(0, 0, 70, 0)
        
    def set_timeline_view(self, timeline_view):
        """Imposta il riferimento alla timeline view"""
        self.timeline_view = timeline_view

    def update_tracks(self, num_tracks, track_height):
        """Aggiorna gli header delle tracce"""
        self.scene.clear()
        self.scene.header_items.clear()
        
        total_height = num_tracks * track_height
        self.scene.setSceneRect(0, 0, 70, total_height)
        
        for i in range(num_tracks):
            y_pos = i * track_height
            header = TrackHeaderItem(0, y_pos, 70, track_height, i)
            self.scene.addItem(header)
            self.scene.header_items.append(header)

    def wheelEvent(self, event):
        # Controlla se abbiamo un riferimento valido alla timeline view
        if self.timeline_view and self.timeline_view.verticalScrollBar().isVisible():
            # Calcola il valore di scroll basato sull'evento della rotella
            delta = event.angleDelta().y()
            # Aggiorna il valore della scrollbar della timeline view
            self.timeline_view.verticalScrollBar().setValue(
                self.timeline_view.verticalScrollBar().value() - delta
            )
            event.accept()
        else:
            super().wheelEvent(event)
