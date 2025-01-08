# tests/test_timeline_container.py
from base_test import BaseTest
from TimelineContainer import TimelineContainer

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
        self.assertEqual(container.timeline_view.viewportMargins(), (0,0,0,0))
        self.assertEqual(container.track_header_view.viewportMargins(), (0,0,0,0))
        
    def test_keyboard_events(self):
        """Test eventi tastiera"""
        container = self.window.timeline_container
        
        # Test propagazione eventi tastiera al parent
        # Simuliamo un evento tastiera
        event = type('TestKeyEvent', (), {'key': lambda: Qt.Key_A, 'modifiers': lambda: Qt.NoModifier})()
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
        new_width = 300
        container.track_header_view.current_width = new_width
        container.track_header_view.update_tracks_width()
        self.assertEqual(container.track_header_view.width(), new_width)

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
        QTest.qWait(200)  # Attendi inizializzazione
        
        # Test sincronizzazione zoom
        self.assertEqual(
            container.ruler_view.scene().zoom_level,
            self.timeline.zoom_level
        )
        
        # Test scroll iniziale
        self.assertEqual(
            container.timeline_view.verticalScrollBar().value(),
            0
        )
        
    def test_splitter_constraints(self):
        """Test vincoli splitter"""
        container = self.window.timeline_container
        header_view = container.track_header_view
        
        # Verifica limiti width
        self.assertGreaterEqual(header_view.width(), header_view.minimumWidth())
        self.assertLessEqual(header_view.width(), header_view.maximumWidth())