from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter

"""
from MusicItem import MusicItem
from Timeline import TrackItem
"""
from src.MusicItem import MusicItem
from src.Timeline import TrackItem

class TimelineView(QGraphicsView):
    """
    Vista principale della timeline che gestisce la visualizzazione 
    e l'interazione con gli elementi musicali
    """
    def __init__(self, scene):
        super().__init__(scene)
        self.setup_view()
        self.setup_appearance()
        self.setup_selection()
        self.setup_zoom()

    def setup_appearance(self):
        """Configura le impostazioni di rendering"""
        self.setRenderHint(QPainter.Antialiasing)

    def setup_selection(self):
        """Configura le impostazioni di selezione"""
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(Qt.IntersectsItemShape)

    def setup_zoom(self):
        """Configura le impostazioni dello zoom"""
        self.zoom_timer = QTimer()
        self.zoom_timer.setSingleShot(True)
        self.zoom_timer.setInterval(100)
        self.can_zoom = True

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
            event.accept()
            return
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



    def setup_view(self):
        """Configura le impostazioni base della view"""
        print("\n=== Debug TimelineView Setup ===")
        
        # Debug allineamento
        print("Setting alignment...")
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        # Debug scrollbar policies
        print("Setting scrollbar policies...")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Debug margins
        print("Setting margins...")
        self.setViewportMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        print(f"Viewport margins: {self.viewportMargins()}")
        print(f"Contents margins: {self.contentsMargins()}")
        
        # Debug viewport margins
        print("Checking viewport...")
        if self.viewport():
            self.viewport().setContentsMargins(0, 0, 0, 0)
            print(f"Viewport content margins: {self.viewport().contentsMargins()}")
        else:
            print("Warning: Viewport not available")
        
        # Debug scrollbar state
        h_scrollbar = self.horizontalScrollBar()
        v_scrollbar = self.verticalScrollBar()
        
        print("\nHorizontal Scrollbar State:")
        print(f"Exists: {h_scrollbar is not None}")
        print(f"Range: {h_scrollbar.minimum()} to {h_scrollbar.maximum()}")
        print(f"Page Step: {h_scrollbar.pageStep()}")
        print(f"Is Visible: {h_scrollbar.isVisible()}")
        print(f"Is Enabled: {h_scrollbar.isEnabled()}")
        
        print("\nVertical Scrollbar State:")
        print(f"Exists: {v_scrollbar is not None}")
        print(f"Range: {v_scrollbar.minimum()} to {v_scrollbar.maximum()}")
        print(f"Page Step: {v_scrollbar.pageStep()}")
        print(f"Is Visible: {v_scrollbar.isVisible()}")
        print(f"Is Enabled: {v_scrollbar.isEnabled()}")
        
        # Debug scene rect if scene exists
        if self.scene():
            print("\nScene Information:")
            print(f"Scene Rect: {self.scene().sceneRect()}")
            print(f"View Rect: {self.rect()}")
            print(f"Viewport Rect: {self.viewport().rect()}")
        else:
            print("\nWarning: No scene set yet")
            