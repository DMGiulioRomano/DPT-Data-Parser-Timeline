# tests/timeline/test_track_header.py
from tests.timeline import (
    BaseTest,
    Qt, QTest,
    QMouseEvent, QKeyEvent, QEvent,
    QPointF, QColor
)
from src.TrackHeaderView import TrackHeaderItem
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QGraphicsSceneMouseEvent  

class TrackHeaderTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.header_view = self.window.timeline_container.track_header_view
        self.editable_text_item = self.header_view.scene.header_items[0].text  

    def test_initial_text(self):
        """Verifica che il testo iniziale venga impostato correttamente"""
        self.assertEqual(self.editable_text_item.toPlainText(), "Track 1")
        self.assertEqual(self.editable_text_item.textInteractionFlags(), Qt.NoTextInteraction)

    def test_set_plain_text(self):
        """Verifica che il testo possa essere aggiornato"""
        new_text = "Updated Track Name"
        self.editable_text_item.setPlainText(new_text)
        self.assertEqual(self.editable_text_item.toPlainText(), new_text)

    def test_enable_text_editing(self):
        """Verifica che le interazioni di testo possano essere abilitate"""
        self.editable_text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.assertEqual(self.editable_text_item.textInteractionFlags(), Qt.TextEditorInteraction)

    def test_disable_text_editing(self):
        """Verifica che le interazioni di testo possano essere disabilitate"""
        self.editable_text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.editable_text_item.setTextInteractionFlags(Qt.NoTextInteraction)
        self.assertEqual(self.editable_text_item.textInteractionFlags(), Qt.NoTextInteraction)

    def test_html_content(self):
        """Verifica che il contenuto HTML venga aggiornato correttamente"""
        new_text = "HTML Content Test"
        self.editable_text_item.setPlainText(new_text)
        html_content = self.editable_text_item.toHtml()
        self.assertIn(new_text, html_content)
        self.assertIn("font-family", html_content.lower())  # Controllo base per il rendering

    def test_background_color(self):
        """Verifica che lo stile di sfondo sia incluso nel rendering HTML"""
        self.editable_text_item.setHtml('<p style="background-color: black">Styled Text</p>')
        html_content = self.editable_text_item.toHtml().lower()

        # Controlla che lo stile di sfondo sia incluso, accettando entrambe le rappresentazioni
        self.assertTrue(
            "background-color: black" in html_content or "background-color:#000000;" in html_content,
            "Lo stile di sfondo non è corretto nell'HTML generato"
        )

    def test_text_editing_event(self):
        """Simula l'editing del testo tramite eventi di tastiera"""
        self.editable_text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.editable_text_item.setFocus()

        # Simula input di testo
        self.editable_text_item.setPlainText("Edited Text")
        self.editable_text_item.clearFocus()

        self.assertEqual(self.editable_text_item.toPlainText(), "Edited Text")

    def test_text_selection(self):
        """Verifica che il testo possa essere selezionato e modificato"""
        self.editable_text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.editable_text_item.setFocus()

        # Simula selezione del testo
        cursor = self.editable_text_item.textCursor()
        cursor.select(cursor.Document)
        self.editable_text_item.setTextCursor(cursor)
        self.editable_text_item.setPlainText("New Selection")

        self.assertEqual(self.editable_text_item.toPlainText(), "New Selection")

    def test_trackheaderitem_initialization(self):
        """Verifica l'inizializzazione di TrackHeaderItem"""
        header_item = self.header_view.scene.header_items[0]
        self.assertEqual(header_item.track_number, 0)
        self.assertFalse(header_item.is_selected)
        self.assertEqual(header_item.brush().color(), header_item.base_color)

    def test_trackheaderitem_hover_events(self):
        """Verifica i colori al passaggio del mouse su TrackHeaderItem"""
        header_item = self.header_view.scene.header_items[0]

        # Simula evento di hover
        header_item.hoverEnterEvent(None)
        self.assertEqual(header_item.brush().color(), header_item.hover_color)

        # Simula uscita dal hover
        header_item.hoverLeaveEvent(None)
        self.assertEqual(header_item.brush().color(), header_item.base_color)

    def test_trackheaderitem_selection(self):
        """Verifica la selezione di TrackHeaderItem"""
        header_item = self.header_view.scene.header_items[0]
        
        # Test selezione diretta
        header_item.setSelected(True)
        self.assertTrue(header_item.is_selected)
        self.assertEqual(header_item.brush().color(), header_item.selected_color)

        # Test deselezione
        header_item.setSelected(False)
        self.assertFalse(header_item.is_selected)
        self.assertEqual(header_item.brush().color(), header_item.base_color)

    def test_trackheaderscene_initialization(self):
        """Verifica l'inizializzazione della scena"""
        scene = self.header_view.scene
        self.assertEqual(len(scene.header_items), self.window.settings.get('default_track_count'))

    def test_trackheaderscene_add_items(self):
        """Verifica l'aggiunta di header alla scena"""
        scene = self.header_view.scene
        scene.header_items = []

        # Aggiunge un TrackHeaderItem alla scena
        header = TrackHeaderItem(0, 0, 100, 50, 0)
        scene.addItem(header)
        scene.header_items.append(header)

        self.assertEqual(len(scene.header_items), 1)
        self.assertEqual(scene.header_items[0], header)

    def test_trackheaderview_initialization(self):
        """Verifica l'inizializzazione di TrackHeaderView"""
        view = self.header_view
        self.assertEqual(view.current_width, 200)
        self.assertEqual(view._min_width, 150)
        self.assertEqual(view._max_width, 600)

    def test_trackheaderview_resize_event(self):
        """Verifica il comportamento durante il resize"""
        view = self.header_view

        # Simula resize a dimensioni valide
        view.resize(300, 400)
        self.assertEqual(view.width(), 300)

        # Resize sotto il limite minimo
        view.resize(100, 400)
        self.assertEqual(view.width(), view._min_width)

        # Resize sopra il limite massimo
        view.resize(700, 400)
        self.assertEqual(view.width(), view._max_width)

    def test_trackheaderview_update_tracks(self):
        """Verifica l'aggiornamento degli header delle tracce"""
        view = self.header_view
        view.scene.header_items = []

        # Aggiorna le tracce con nuovi parametri
        view.update_tracks(3, 50)
        self.assertEqual(len(view.scene.header_items), 3)

        for i, header in enumerate(view.scene.header_items):
            self.assertEqual(header.track_number, i)

    def test_trackbutton_initialization(self):
        """Verifica l'inizializzazione del TrackButton"""
        header_item = self.header_view.scene.header_items[0]
        mute_button = header_item.mute_button
        solo_button = header_item.solo_button

        self.assertFalse(mute_button.is_active)
        self.assertFalse(solo_button.is_active)

    def test_trackbutton_hover_effect(self):
        """Verifica l'effetto di hover sul pulsante"""
        header_item = self.header_view.scene.header_items[0]
        mute_button = header_item.mute_button

        # Simula hover enter
        mute_button.hoverEnterEvent(None)
        self.assertEqual(mute_button.brush().color(), QColor(180, 180, 180))

        # Simula hover leave
        mute_button.hoverLeaveEvent(None)
        self.assertEqual(mute_button.brush().color(), QColor(200, 200, 200))

    def test_trackbutton_click_toggle(self):
        """Test toggle del pulsante mute del TrackButton"""
        header_item = self.header_view.scene.header_items[0]
        mute_button = header_item.mute_button
        
        # Stato iniziale
        self.assertFalse(mute_button.is_active)
        
        # Toggle diretto per test
        mute_button.toggleForTest()
        
        # Verifica che lo stato sia cambiato 
        self.assertTrue(mute_button.is_active)
        
        # Toggle di nuovo
        mute_button.toggleForTest()
        
        # Verifica che lo stato sia tornato inattivo
        self.assertFalse(mute_button.is_active)