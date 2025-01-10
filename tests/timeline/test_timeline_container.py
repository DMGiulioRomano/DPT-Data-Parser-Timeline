# tests/timeline/test_timeline_container.py
from tests.timeline import (
    BaseTest,
    Qt, QTest,
        QPointF, QRectF,
    QKeyEvent, QEvent

)
from PyQt5.QtWidgets import QApplication, QSplitter
from src.TimelineContainer import TimelineContainer
class TimelineContainerTest(BaseTest):
    def test_ruler_update(self):
        """Test aggiornamento ruler"""
        container = self.window.timeline_container
        
        # Cambia zoom
        self.timeline.scale_scene(1.5)
        
        # Verifica che il ruler sia aggiornato
        self.assertEqual(
            container.ruler_view.scene().zoom_level,
            self.timeline.zoom_level
        )
        
    def test_viewport_margins(self):
        """Test margins dei viewport"""
        container = self.window.timeline_container
        
        # Verifica margins
        margins = container.timeline_view.viewportMargins()
        self.assertEqual((margins.left(), margins.top(), margins.right(), margins.bottom()), (0,0,0,0))
        self.assertEqual((container.track_header_view.viewportMargins().left(),
                        container.track_header_view.viewportMargins().top(),
                        container.track_header_view.viewportMargins().right(), 
                        container.track_header_view.viewportMargins().bottom()), (0,0,0,0))
        
    def test_keyboard_events(self):
        """Test eventi tastiera"""
        container = self.window.timeline_container
        
        # Creiamo un evento tastiera appropriato usando QKeyEvent invece di un mock
        event = QKeyEvent(QEvent.KeyPress, Qt.Key_A, Qt.NoModifier)
        container.timeline_view.keyPressEvent(event)

    def test_view_synchronization(self):
        """Test sincronizzazione views"""
        container = self.window.timeline_container
        
        # Scroll verticale
        timeline_view = container.timeline_view
        header_view = container.track_header_view
        
        timeline_view.verticalScrollBar().setValue(100)
        self.assertEqual(
            header_view.verticalScrollBar().value(),
            timeline_view.verticalScrollBar().value()
        )

    def test_splitter_movement(self):
        """Test movimento splitter"""
        container = self.window.timeline_container
        initial_width = container.track_header_view.width()
        
        # Simula movimento splitter
        container.on_splitter_moved(initial_width + 50, 0)
        
        self.assertEqual(
            container.track_header_view.width(),
            initial_width + 50
        )

    def test_views_initialization(self):
        """Test inizializzazione viste"""
        container = self.window.timeline_container
        self.assertIsNotNone(container.timeline_view)
        self.assertIsNotNone(container.track_header_view)
        self.assertIsNotNone(container.ruler_view)
            

    def test_header_width_update(self):
        """Test aggiornamento larghezza header"""
        container = self.window.timeline_container
        view = container.track_header_view        
        # Get the splitter
        splitter = None
        for child in container.children():
            if isinstance(child, QSplitter):
                splitter = child
                break        
        old_width = view.width()
        new_width = 300
        # Process events before change
        QApplication.processEvents()
        view.current_width = new_width
        view.update_tracks_width()
        # Forza l'aggiornamento del layout
        container.adjustSize()              
        # Let Qt process the resize events
        QApplication.processEvents()
        QApplication.processEvents()      
        # Try to force splitter resize
        if splitter:
            sizes = splitter.sizes()
            sizes[splitter.indexOf(view)] = new_width
            splitter.setSizes(sizes)
            QApplication.processEvents()
        self.assertEqual(view.width(), new_width, 
                        "Header width not updated correctly")
                

    def test_scroll_synchronization(self):
        """Test sincronizzazione scroll completa"""
        container = self.window.timeline_container
        
        # Test scroll orizzontale
        container.timeline_view.horizontalScrollBar().setValue(100)
        self.assertEqual(
            container.ruler_view.horizontalScrollBar().value(),
            100
        )
        
        # Test scroll verticale
        container.timeline_view.verticalScrollBar().setValue(50)
        self.assertEqual(
            container.track_header_view.verticalScrollBar().value(),
            50
        )

    def test_initialize_views(self):
        """Test inizializzazione completa viste"""
        container = self.window.timeline_container
        
        # Assicuriamoci che il container esista
        self.assertIsNotNone(container)
        
        # Attendiamo il processamento degli eventi
        QApplication.processEvents()
        
        # Verifichiamo che le view esistano prima di usarle
        self.assertIsNotNone(container.ruler_view)
        self.assertIsNotNone(container.timeline_view)
        
        # Test sincronizzazione zoom
        ruler_scene = container.ruler_view.scene()
        self.assertIsNotNone(ruler_scene)
        
        self.assertEqual(
            ruler_scene.zoom_level,
            self.timeline.zoom_level,
            "Zoom levels should match"
        )
        
        # Test scroll iniziale
        scrollbar = container.timeline_view.verticalScrollBar()
        self.assertIsNotNone(scrollbar)
        self.assertEqual(
            scrollbar.value(),
            0,
            "Initial scroll should be 0"
        )
        
        # Forza il processamento di eventi in sospeso
        QApplication.processEvents()
                
    def test_splitter_constraints(self):
        """Test vincoli splitter"""
        container = self.window.timeline_container
        header_view = container.track_header_view
        
        # Verifica limiti width
        self.assertGreaterEqual(header_view.width(), header_view.minimumWidth())
        self.assertLessEqual(header_view.width(), header_view.maximumWidth())