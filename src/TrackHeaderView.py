from PyQt5.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, 
    QGraphicsTextItem, QGraphicsItem, QLineEdit
)
from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QPen, QColor, QBrush, QFont, QPainter
from Timeline import MIN_SCENE_HEIGHT

class EditableTextItem(QGraphicsTextItem):
    """Testo editabile per l'header della traccia"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        # Ora impostiamo il testo e aggiorniamo le dimensioni
        self.setDefaultTextColor(Qt.black)
        self.setTextWidth(60)
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.setAcceptHoverEvents(True)
        # Usa HTML per avere testo bianco su sfondo nero
        self.setHtml(f'<div style="background-color: black; color: white; padding: 0px;">{text}</div>')

    def mousePressEvent(self, event):
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setFocus()
        cursor = self.textCursor()
        cursor.select(cursor.Document)
        self.setTextCursor(cursor)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.clearFocus()
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        super().focusOutEvent(event)


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
        
        self.text = EditableTextItem(f"Track {track_number + 1}", self)
        text_y = ((height - self.text.boundingRect().height()) / 2) + y
        self.text.setPos(10, text_y)
        
        # Aggiungi i pulsanti Mute e Solo
        button_y = text_y
        button_width = 20
        button_margin = 5
        self.mute_button = TrackButton("M", self)
        self.solo_button = TrackButton("S", self)
        # Posiziona i pulsanti nell'angolo destro della traccia corrente
        self.mute_button.setPos(width - (2 * button_width + button_margin), button_y)
        self.solo_button.setPos(width - button_width - button_margin, button_y)

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
        self.setMinimumWidth(150)
        self.setMaximumWidth(600)
        self.current_width = 200
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setRenderHint(QPainter.Antialiasing)
        self.setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)
        self.viewport().setContentsMargins(0, 0, 0, 0)
        self.scene.setSceneRect(0, 0, self.current_width, MIN_SCENE_HEIGHT)

    def keyPressEvent(self, event):
        """Gestisce gli eventi da tastiera per la TrackHeaderView"""
        if event.modifiers() & Qt.AltModifier and event.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
            # Trova gli header selezionati
            selected_headers = [item for item in self.scene.items() 
                            if isinstance(item, TrackHeaderItem) and item.is_selected]
            
            # Se ci sono header selezionati, elimina le tracce corrispondenti
            if selected_headers:
                main_window = self.window()
                if hasattr(main_window, 'delete_selected_track'):
                    for header in selected_headers:
                        main_window.delete_selected_track()
                event.accept()
                return
        super().keyPressEvent(event)
    def resizeEvent(self, event):
        """Gestisce il ridimensionamento della view"""
        super().resizeEvent(event)
        new_width = event.size().width()
        if new_width != self.current_width:
            self.current_width = new_width
            self.scene.setSceneRect(0, 0, new_width, self.scene.height())
            self.update_tracks_width()

    def set_timeline_view(self, timeline_view):
        """Imposta il riferimento alla timeline view"""
        self.timeline_view = timeline_view

    def update_tracks_width(self):
        """Aggiorna la larghezza di tutti gli header delle tracce"""
        for header in self.scene.header_items:
            if isinstance(header, TrackHeaderItem):
                # Aggiorna il rettangolo principale
                header.setRect(0, header.rect().y(), self.current_width, header.rect().height())
                # Aggiorna la posizione dei pulsanti
                button_width = 20
                button_margin = 5
                header.mute_button.setPos(self.current_width - (2 * button_width + button_margin), 
                                        header.mute_button.pos().y())
                header.solo_button.setPos(self.current_width - button_width - button_margin, 
                                        header.solo_button.pos().y())

    def update_tracks(self, num_tracks, track_height):
        """Aggiorna gli header delle tracce"""
        self.scene.clear()
        self.scene.header_items.clear()
        
        total_height = max(MIN_SCENE_HEIGHT, num_tracks * track_height)
        self.scene.setSceneRect(0, 0, self.current_width, total_height)
        
        for i in range(num_tracks):
            y_pos = i * track_height
            header = TrackHeaderItem(0, y_pos, self.current_width, track_height, i)
            self.scene.addItem(header)
            self.scene.header_items.append(header)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier and self.timeline_view:
            # Redirect horizontal scrolling to timeline
            delta = event.angleDelta().x() if event.angleDelta().x() != 0 else event.angleDelta().y()
            self.timeline_view.horizontalScrollBar().setValue(
                self.timeline_view.horizontalScrollBar().value() - delta
            )
            event.accept()
            return
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

class TrackButton(QGraphicsRectItem):
    """Pulsante per mute/solo"""
    def __init__(self, text, parent=None):
        super().__init__(0, 0, 20, 20, parent)
        self.setAcceptHoverEvents(True)
        self.setBrush(QBrush(QColor(200, 200, 200)))
        self.setPen(QPen(Qt.black))
        self.is_active = False
        
        # Aggiungi il testo del pulsante
        self.text_item = QGraphicsTextItem(text, self)
        self.text_item.setDefaultTextColor(Qt.black)
        # Centra il testo nel pulsante
        text_rect = self.text_item.boundingRect()
        text_x = (20 - text_rect.width()) / 2
        text_y = (20 - text_rect.height()) / 2
        self.text_item.setPos(text_x, text_y)
        
    def mousePressEvent(self, event):
        self.is_active = not self.is_active
        self.setBrush(QBrush(QColor(150, 150, 150) if self.is_active else QColor(200, 200, 200)))
        super().mousePressEvent(event)
        
    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(QColor(180, 180, 180)))
        super().hoverEnterEvent(event)
        
    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(QColor(150, 150, 150) if self.is_active else QColor(200, 200, 200)))
        super().hoverLeaveEvent(event)