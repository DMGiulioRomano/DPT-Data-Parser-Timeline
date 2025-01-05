import sys
import yaml
from PyQt5.QtWidgets import (QGraphicsView, QWidget, QVBoxLayout, 
                           QHBoxLayout, QScrollBar)
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QBrush
from TimelineRuler import TimelineRuler
from MusicItem import MusicItem
from Timeline import *
class TimelineView(QGraphicsView):
    def __init__(self, scene):
        # Creiamo il widget container principale
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Container per il ruler con il suo margine
        ruler_container = QWidget()
        ruler_layout = QHBoxLayout(ruler_container)
        ruler_layout.setContentsMargins(70, 0, 0, 0)  # Aggiungiamo il margine qui
        ruler_layout.setSpacing(0)
        ruler_container.setContentsMargins(0, 0, 0, 0)  

        # Timeline ruler
        self.ruler_scene = TimelineRuler(scene.settings, scene)
        self.ruler_view = QGraphicsView(self.ruler_scene)
        self.ruler_view.setFixedHeight(70)
        self.ruler_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ruler_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Qui dobbiamo aggiungere il ruler alla ruler_layout (non al main_layout)
        ruler_layout.addWidget(self.ruler_view) 

        # Aggiungiamo il container del ruler al layout principale
        self.main_layout.addWidget(ruler_container)
    
        # Main timeline view
        super().__init__(scene)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setViewportMargins(70, 0, 0, 0)  # Manteniamo il margine qui
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)
        
        # Scroll synchronization
        self.horizontalScrollBar().valueChanged.connect(
            self.ruler_view.horizontalScrollBar().setValue)
            
        # Add main view to layout
        self.main_layout.addWidget(self)
        self.zoom_timer = QTimer()
        self.zoom_timer.setSingleShot(True)
        self.zoom_timer.setInterval(100)
        self.can_zoom = True

    def get_widget(self):
        return self.main_widget


    def mousePressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            self.setDragMode(QGraphicsView.RubberBandDrag)
            if not self.scene().selectedItems():
                super().mousePressEvent(event)
        else:
            self.setDragMode(QGraphicsView.NoDrag)
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setDragMode(QGraphicsView.NoDrag)

    def handleRubberBandSelection(self, rubberBandRect, fromScenePoint, toScenePoint):
        selectionRect = self.mapToScene(rubberBandRect).boundingRect()
        items = self.scene().items(selectionRect)
        
        for item in items:
            if isinstance(item, MusicItem):
                item.setSelected(True)
                            
    # Override wheelEvent per gestire lo zoom su entrambe le viste
    def wheelEvent(self, event):
        if not self.can_zoom:
            return
            
        if event.phase() == Qt.ScrollPhase.ScrollBegin:
            self.pinch_start = True
        elif event.phase() == Qt.ScrollPhase.ScrollEnd:
            self.pinch_start = False
            
        if hasattr(self, 'pinch_start') and self.pinch_start:
            factor = 1.1 if event.angleDelta().y() > 0 else 0.9
            self.scene().scale_scene(factor)
            self.ruler_scene.update_zoom(self.scene().zoom_level)
            self.can_zoom = False
            self.zoom_timer.timeout.connect(self.enable_zoom)
            self.zoom_timer.start()
        else:
            super().wheelEvent(event)

    def enable_zoom(self):
        self.can_zoom = True

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.AltModifier:
            if event.key() == Qt.Key_Left:
                self.horizontalScrollBar().setValue(
                    self.horizontalScrollBar().value() - 100)
            elif event.key() == Qt.Key_Right:
                self.horizontalScrollBar().setValue(
                    self.horizontalScrollBar().value() + 100)
            elif event.key() == Qt.Key_Up:
                self.scene().scale_scene(1.2)
            elif event.key() == Qt.Key_Down:
                self.scene().scale_scene(0.8)
            elif event.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
                # Cancellazione diretta della traccia con Alt+Delete
                main_window = self.window()
                if hasattr(main_window, 'delete_selected_track'):
                    main_window.delete_selected_track()
        elif (event.modifiers() & Qt.ControlModifier or event.modifiers() & Qt.MetaModifier) and event.key() == Qt.Key_D:
            selected_items = self.scene().selectedItems()
            new_items = []
            
            for item in selected_items:
                if isinstance(item, MusicItem):
                    new_item = MusicItem(0, 0, item.rect().width(), item.name, item.settings, item.rect().height())
                    new_item.params = item.params.copy()
                    new_pos = item.pos() + QPointF(item.rect().width(), 0)
                    new_item.setPos(new_pos)
                    new_item.params['cAttacco'] = new_pos.x() / (self.scene().pixels_per_beat * self.scene().zoom_level)
                    self.scene().addItem(new_item)
                    new_items.append(new_item)
            
            # Clear old selection and select new items
            for item in selected_items:
                item.setSelected(False)
            for item in new_items:
                item.setSelected(True)
        elif event.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
            # Ottieni il riferimento alla MainWindow
            main_window = self.window()
            
            # Prima controlla se c'è una traccia selezionata
            for item in self.scene().selectedItems():
                if isinstance(item, TrackItem):
                    if hasattr(main_window, 'delete_selected_track'):
                        main_window.delete_selected_track()
                    return
            
            # Se non ci sono tracce selezionate, procedi con la cancellazione degli item
            if hasattr(main_window, 'delete_selected_items'):
                main_window.delete_selected_items()
        else:
            super().keyPressEvent(event)