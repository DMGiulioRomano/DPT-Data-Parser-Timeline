# tests/timeline/test_timeline_view.py
from timeline import (
    BaseTest,
    TimelineView,
    Qt, QTest,
    QTimer, QPointF, QRectF,
    QKeyEvent, QEvent
)

class TimelineViewTest(BaseTest):
    def test_zoom_timeout(self):
        """Test timeout dello zoom"""
        view = self.window.timeline_container.timeline_view
        
        # Disabilita zoom
        view.can_zoom = False
        
        # Verifica che dopo il timeout lo zoom sia riabilitato
        QTimer.singleShot(150, lambda: self.assertTrue(view.can_zoom))
        
    def test_drag_mode(self):
        """Test modalità drag"""
        view = self.window.timeline_container.timeline_view
        
        # Test con Control premuto
        event = type('TestMouseEvent', (), {
            'modifiers': lambda: Qt.ControlModifier,
            'buttons': lambda: Qt.NoButton
        })()
        view.mousePressEvent(event)
        self.assertEqual(view.dragMode(), view.RubberBandDrag)
        
        # Test senza Control
        event = type('TestMouseEvent', (), {
            'modifiers': lambda: Qt.NoModifier,
            'buttons': lambda: Qt.NoButton
        })()
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

    def test_keyboard_shortcuts(self):
        """Test scorciatoie tastiera complete"""
        view = self.window.timeline_container.timeline_view
        
        # Test Alt + tasti freccia
        for key, expected_value in [
            (Qt.Key_Left, -100),
            (Qt.Key_Right, 100)
        ]:
            event = QKeyEvent(QEvent.KeyPress, key, Qt.AltModifier)
            view.keyPressEvent(event)
            self.assertEqual(
                view.horizontalScrollBar().value(),
                expected_value
            )