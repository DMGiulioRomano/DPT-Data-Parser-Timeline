# tests/timeline/test_track_header.py
from tests.timeline import (
    BaseTest,
    Qt,
    QMouseEvent, QKeyEvent, QEvent,
    QPointF
)
from src.TrackHeaderView import TrackHeaderItem
class TrackHeaderTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.header_view = self.window.timeline_container.track_header_view

    def test_track_header_creation(self):
        """Test creazione header tracce"""
        initial_tracks = len(self.header_view.scene.header_items)
        self.window.add_new_track()
        self.assertEqual(
            len(self.header_view.scene.header_items), 
            initial_tracks + 1
        )

    def test_track_selection(self):
        """Test selezione tracce"""
        # Seleziona prima traccia
        first_header = self.header_view.scene.header_items[0]
        first_header.mousePressEvent(None)  # Simula click
        self.assertTrue(first_header.is_selected)
        
        # Verifica che la selezione sia propagata
        self.assertEqual(self.window.selected_track, 0)

    def test_mute_solo_buttons(self):
        """Test pulsanti mute/solo"""
        header = self.header_view.scene.header_items[0]
        
        # Test mute
        header.mute_button.mousePressEvent(None)  # Simula click
        self.assertTrue(header.mute_button.is_active)
        
        # Test solo
        header.solo_button.mousePressEvent(None)  # Simula click
        self.assertTrue(header.solo_button.is_active)

    def test_track_renaming(self):
        """Test rinomina traccia"""
        header = self.window.timeline_container.track_header_view.scene.header_items[0]
        header.text.setPlainText("New Track Name")
        
        # Simula pressione Enter
        event = type('TestKeyEvent', (), {'key': lambda: Qt.Key_Return})()
        header.text.keyPressEvent(event)
        
        self.assertEqual(header.text.toPlainText(), "New Track Name")
        
    def test_button_states(self):
        """Test stati pulsanti mute/solo"""
        header = self.window.timeline_container.track_header_view.scene.header_items[0]
        
        # Test toggle mute
        header.mute_button.mousePressEvent(None)
        self.assertTrue(header.mute_button.is_active)
        header.mute_button.mousePressEvent(None)
        self.assertFalse(header.mute_button.is_active)
        
        # Test hover
        header.mute_button.hoverEnterEvent(None)
        self.assertNotEqual(
            header.mute_button.brush().color(),
            header.mute_button._default_color
        )

    def test_editable_text(self):
        """Test testo editabile header"""
        header = self.window.timeline_container.track_header_view.scene.header_items[0]
        text_item = header.text
        
        # Test inizio editing
        mouse_event = QMouseEvent(
            QEvent.MouseButtonPress, QPointF(0,0), 
            Qt.LeftButton, Qt.LeftButton, Qt.NoModifier
        )
        text_item.mousePressEvent(mouse_event)
        self.assertEqual(
            text_item.textInteractionFlags(),
            Qt.TextEditorInteraction
        )

        # Test fine editing
        key_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
        text_item.keyPressEvent(key_event)
        self.assertEqual(
            text_item.textInteractionFlags(),
            Qt.NoTextInteraction
        )