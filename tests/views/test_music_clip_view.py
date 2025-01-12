from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QGraphicsScene
import unittest
from unittest.mock import MagicMock, patch
from src.models.music_clip import MusicClipModel
from src.views.music_clip_view import MusicClipView

class TestMusicClipView(unittest.TestCase):
    def setUp(self):
        """Setup per ogni test"""
        self.scene = QGraphicsScene()
        self.scene.pixels_per_beat = 100
        self.scene.zoom_level = 1.0
        self.scene.track_height = 50
        self.scene.num_tracks = 8
        
        self.settings = {
            'item_text_size': 12,
            'text_color': '#000000'
        }
        
        self.model = MusicClipModel("Test Clip")
        self.view = MusicClipView(self.model, self.settings)
        self.scene.addItem(self.view)

    def test_initialization(self):
        """Test corretta inizializzazione della vista"""
        self.assertEqual(self.view.text.toPlainText(), "Test Clip")
        self.assertEqual(self.view.color, QColor(100, 150, 200))
        self.assertTrue(self.view.flags() & self.view.ItemIsMovable)
        self.assertTrue(self.view.flags() & self.view.ItemIsSelectable)

    def test_model_view_sync(self):
        """Test sincronizzazione tra modello e vista"""
        # Cambia nome nel modello
        self.model.name = "New Name"
        self.assertEqual(self.view.text.toPlainText(), "New Name")

        # Cambia durata
        self.model.set_param("durata", 10.0)
        expected_width = 10.0 * self.scene.pixels_per_beat * self.scene.zoom_level
        self.assertAlmostEqual(self.view.rect().width(), expected_width, places=1)

        # Cambia posizione
        self.model.position = (2.0, 100.0)
        expected_x = 2.0 * self.scene.pixels_per_beat * self.scene.zoom_level
        self.assertAlmostEqual(self.view.pos().x(), expected_x, places=1)
        self.assertAlmostEqual(self.view.pos().y(), 100.0, places=1)

    def test_grid_snapping(self):
        """Test snapping alla griglia"""
        # Simula movimento a posizione non allineata
        grid_size = (self.scene.pixels_per_beat * self.scene.zoom_level) / 16
        unaligned_pos = QPointF(grid_size * 1.3, self.scene.track_height * 1.3)
        
        # Ottiene la posizione dopo lo snapping
        new_pos = self.view.itemChange(
            self.view.ItemPositionChange,
            unaligned_pos
        )
        
        # Verifica allineamento alla griglia
        self.assertEqual(new_pos.x() % grid_size, 0)
        self.assertEqual(new_pos.y() % self.scene.track_height, 0)

    def test_hover_effects(self):
        """Test effetti hover"""
        # Verifica stato iniziale
        self.assertFalse(self.view.is_hovered)
        
        # Simula hover enter
        self.view.hoverEnterEvent(None)
        self.assertTrue(self.view.is_hovered)
        
        # Simula hover leave
        self.view.hoverLeaveEvent(None)
        self.assertFalse(self.view.is_hovered)

    def test_height_update(self):
        """Test aggiornamento altezza"""
        initial_height = self.view.rect().height()
        new_height = 80
        
        self.view.updateHeight(new_height)
        
        self.assertEqual(self.view.rect().height(), new_height)
        # Verifica che il testo sia centrato verticalmente
        text_pos = self.view.text.pos()
        text_height = self.view.text.boundingRect().height()
        expected_y = (new_height - text_height) / 2
        self.assertAlmostEqual(text_pos.y(), expected_y, places=1)

    def test_text_style_update(self):
        """Test aggiornamento stile testo"""
        # Modifica impostazioni
        self.settings['item_text_size'] = 16
        self.settings['text_color'] = '#FF0000'
        
        self.view.updateTextStyle()
        
        self.assertEqual(self.view.text.font().pointSize(), 16)
        self.assertEqual(
            self.view.text.defaultTextColor(),
            QColor(self.settings['text_color'])
        )

    def test_mouse_interaction(self):
        """Test interazioni mouse"""
        # Simula evento mouse con Meta modifier
        event = MagicMock()
        event.modifiers.return_value = Qt.MetaModifier
        
        # Mock della MainWindow
        mock_window = MagicMock()
        self.scene.views = MagicMock(return_value=[MagicMock(window=MagicMock(return_value=mock_window))])
        
        self.view.mousePressEvent(event)
        mock_window.showParamDialog.assert_called_once_with(self.model)

    def test_selection_highlight(self):
        """Test evidenziazione selezione"""
        # Verifica colore normale
        self.assertEqual(self.view.brush().color(), self.view.color)
        
        # Simula selezione
        self.view.setSelected(True)
        self.view.paint(MagicMock(), None, None)
        
        # Il colore durante la paint dovrebbe essere più chiaro
        expected_color = self.view.color.lighter(140)
        self.assertEqual(self.view.brush().color(), self.view.color)  # Torna al colore originale

    def test_paint(self):
        # Caso base: nessuna selezione, hover o evidenziazione
        self.view.paint(QPainter(), None, None)
        self.assertEqual(self.view.brush().color(), self.view.color)

        # Caso selezione
        self.view.setSelected(True)
        self.view.paint(QPainter(), None, None)
        self.assertEqual(self.view.brush().color(), self.view.color.lighter(140))
        self.view.setSelected(False)

        # Caso hover
        self.view.is_hovered = True
        self.view.paint(QPainter(), None, None)
        self.assertEqual(self.view.brush().color(), self.view.color.lighter(110))
        self.view.is_hovered = False

        # Caso evidenziazione
        self.view.highlighted = True
        
        # Verifica del colore di sfondo di evidenziazione
        highlight_color = QColor(255, 255, 0)
        with patch.object(self.view, 'setBrush') as mock_set_brush:
            self.view.paint(QPainter(), None, None)
            mock_set_brush.assert_any_call(highlight_color)
        
        # Verifica del rettangolo di evidenziazione
        with patch.object(QPainter, 'drawRect') as mock_draw_rect:
            painter = QPainter()
            self.view.paint(painter, None, None)
            mock_draw_rect.assert_called_once_with(self.view.rect())
        
        # Verifica del pennello di evidenziazione
        with patch.object(QPainter, 'setPen') as mock_set_pen:
            painter = QPainter()
            self.view.paint(painter, None, None)
            pen = QPen(QColor(255, 165, 0), 3)
            mock_set_pen.assert_called_once_with(pen)
        
        self.view.highlighted = False

        # Verificare che il pennello originale sia ripristinato dopo il disegno
        original_brush = self.view.brush()
        self.view.paint(QPainter(), None, None)
        self.assertEqual(self.view.brush().color(), original_brush.color())