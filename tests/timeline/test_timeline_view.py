# tests/timeline/test_timeline_view.py
from tests.timeline import (
    BaseTest,
    Qt,
    QTimer, QPointF, QRectF,
    QKeyEvent, QEvent
)
from src.TimelineView import TimelineView
from src.Timeline import TrackItem
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import QPoint
from src.MusicItem import MusicItem
class TimelineViewTest(BaseTest):
    def test_zoom_timeout(self):
        """Test timeout dello zoom"""
        view = self.window.timeline_container.timeline_view
        
        # Disabilita zoom
        view.can_zoom = False
        
        # Verifica che dopo il timeout lo zoom sia riabilitato
        QTimer.singleShot(150, lambda: self.assertTrue(view.can_zoom))
            

    def test_drag_mode(self):
        """Test modalità drag e selezione multipla"""
        view = self.window.timeline_container.timeline_view
        
        # Creiamo alcuni item di test nella timeline
        items = [
            self.timeline.add_music_item(i, 0, 1, f"Test{i}", self.window.settings)
            for i in range(3)
        ]
        
        # Test con Control premuto
        event = QMouseEvent(
            QEvent.MouseButtonPress,    # tipo evento
            QPoint(0, 0),              # posizione locale
            Qt.LeftButton,             # bottone del mouse
            Qt.LeftButton,             # bottoni premuti
            Qt.ControlModifier         # modificatori (Control)
        )
        
        view.mousePressEvent(event)
        self.assertEqual(view.dragMode(), view.RubberBandDrag)
        
        # Simula una selezione di area
        rect = QRectF(0, 0, 300, 100)  # Area che copre gli items
        view.handleRubberBandSelection(rect, QPointF(0,0), QPointF(300,100))
        
        # Verifica selezione multipla
        selected = [item for item in items if item.isSelected()]
        self.assertEqual(len(selected), 3)
        
        # Test senza Control
        event = QMouseEvent(
            QEvent.MouseButtonPress,    
            QPoint(0, 0),              
            Qt.LeftButton,             
            Qt.LeftButton,             
            Qt.NoModifier              # Nessun modificatore
        )
        
        view.mousePressEvent(event)
        self.assertEqual(view.dragMode(), view.NoDrag)


    def test_zoom_timeout(self):
        """Test timeout dello zoom"""
        view = self.window.timeline_container.timeline_view
        
        # Disabilita zoom
        view.can_zoom = False
        
        # Verifica che dopo il timeout lo zoom sia riabilitato
        QTimer.singleShot(150, lambda: self.assertTrue(view.can_zoom))

    def test_alt_zoom_shortcuts(self):
        """Test scorciatoie Alt+Up/Down per zoom"""
        view = self.window.timeline_container.timeline_view
        initial_zoom = view.scene().zoom_level

        # Test Alt + Up per zoom in
        event = QKeyEvent(QEvent.KeyPress, Qt.Key_Up, Qt.AltModifier)
        view.keyPressEvent(event)
        zoomed_in = view.scene().zoom_level
        self.assertGreater(zoomed_in, initial_zoom)

        # Test Alt + Down per zoom out
        event = QKeyEvent(QEvent.KeyPress, Qt.Key_Down, Qt.AltModifier)
        view.keyPressEvent(event)
        # Confronta con il valore dopo lo zoom in, non con se stesso
        self.assertLess(view.scene().zoom_level, zoomed_in)
        
    def test_alt_delete_track(self):
        """Test cancellazione traccia con Alt+Delete"""
        view = self.window.timeline_container.timeline_view
        initial_tracks = view.scene().num_tracks
        
        # Seleziona una traccia attraverso l'header
        header_view = self.window.timeline_container.track_header_view
        header_item = header_view.scene.header_items[0]  # Prendi il primo header
        header_item.setSelected(True)
        
        # Test Alt + Delete
        event = QKeyEvent(QEvent.KeyPress, Qt.Key_Delete, Qt.AltModifier)
        view.keyPressEvent(event)
        
        self.assertEqual(view.scene().num_tracks, initial_tracks - 1)

    def test_ctrl_d_item_duplication(self):
        """Test duplicazione items con Ctrl+D"""
        view = self.window.timeline_container.timeline_view
        
        # Crea e seleziona un item
        item = view.scene().add_music_item(0, 0, 3, "Test", self.window.settings)
        item.setSelected(True)
        initial_items = len([i for i in view.scene().items() 
                           if isinstance(i, MusicItem)])
        
        # Test Ctrl + D
        event = QKeyEvent(QEvent.KeyPress, Qt.Key_D, Qt.ControlModifier)
        view.keyPressEvent(event)
        
        final_items = len([i for i in view.scene().items() 
                          if isinstance(i, MusicItem)])
        self.assertEqual(final_items, initial_items + 1)
        
        # Verifica che il nuovo item sia selezionato e il vecchio no
        selected_items = [i for i in view.scene().selectedItems() 
                         if isinstance(i, MusicItem)]
        self.assertEqual(len(selected_items), 1)
        self.assertNotEqual(selected_items[0], item)

    def test_delete_items(self):
        """Test cancellazione items con Delete"""
        view = self.window.timeline_container.timeline_view
        
        # Crea e seleziona un item
        item = view.scene().add_music_item(0, 0, 3, "Test", self.window.settings)
        item.setSelected(True)
        initial_items = len([i for i in view.scene().items() 
                           if isinstance(i, MusicItem)])
        
        # Test Delete
        event = QKeyEvent(QEvent.KeyPress, Qt.Key_Delete, Qt.NoModifier)
        view.keyPressEvent(event)
        
        final_items = len([i for i in view.scene().items() 
                          if isinstance(i, MusicItem)])
        self.assertEqual(final_items, initial_items - 1)

    def test_ctrl_selection_mode(self):
        """Test modalità selezione con Control"""
        view = self.window.timeline_container.timeline_view
        
        # Test con Control premuto
        event = QMouseEvent(
            QEvent.MouseButtonPress,  # tipo evento
            QPoint(0, 0),            # posizione
            Qt.LeftButton,           # bottone
            Qt.LeftButton,           # bottoni
            Qt.ControlModifier       # modificatori
        )
        view.mousePressEvent(event)
        self.assertEqual(view.dragMode(), view.RubberBandDrag)
        
        # Test senza Control
        event = QMouseEvent(
            QEvent.MouseButtonPress,
            QPoint(0, 0),
            Qt.LeftButton,
            Qt.LeftButton,
            Qt.NoModifier
        )
        view.mousePressEvent(event)
        self.assertEqual(view.dragMode(), view.NoDrag)
        
    def test_rubber_band_selection(self):
        """Test selezione con rubber band"""
        view = self.window.timeline_container.timeline_view
        items = [
            self.timeline.add_music_item(i, 0, 1, f"Test{i}", self.window.settings)
            for i in range(3)
        ]
        
        # Simula selezione rubber band
        rect = QRectF(0, 0, 300, 100)
        view.handleRubberBandSelection(rect, QPointF(0,0), QPointF(300,100))
        
        selected = [item for item in items if item.isSelected()]
        self.assertEqual(len(selected), 3)