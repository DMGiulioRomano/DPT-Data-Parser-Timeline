# Nuovo file: TimelineContainer.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QGraphicsView
from PyQt5.QtCore import Qt
from TimelineView import TimelineView
from TrackHeaderView import TrackHeaderView
from TimelineRuler import TimelineRuler


class TimelineRulerView(QGraphicsView):
    def __init__(self, scene, timeline_view=None):
        super().__init__(scene)
        self.timeline_view = timeline_view
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedHeight(70)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    
    def wheelEvent(self, event):
        if self.timeline_view:
            self.timeline_view.wheelEvent(event)
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        if self.parent():
            self.parent().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

class TimelineContainer(QWidget):
    """
    Container principale che gestisce il layout dell'intera timeline,
    inclusi ruler, track headers e la timeline principale
    """
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.timeline_view = None
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        # Layout principale
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 1. Ruler Section
        ruler_container = self.create_ruler_section()
        main_layout.addWidget(ruler_container)

        # 2. Timeline Section (Headers + Timeline)
        timeline_container = self.create_timeline_section()
        main_layout.addWidget(timeline_container)

    def setup_connections(self):
        """Configura le connessioni tra i vari componenti"""
        # Sincronizzazione scroll verticale
        self.timeline_view.verticalScrollBar().valueChanged.connect(
            self.track_header_view.verticalScrollBar().setValue)
        self.track_header_view.verticalScrollBar().valueChanged.connect(
            self.timeline_view.verticalScrollBar().setValue)

        # Sincronizzazione scroll orizzontale con gestione aggiuntiva per il ruler
        def handle_horizontal_scroll(value):
            self.ruler_view.horizontalScrollBar().setValue(value)
            # Forza l'aggiornamento del viewport
            self.ruler_view.viewport().update()
            self.track_header_view.viewport().update()
            
        self.timeline_view.horizontalScrollBar().valueChanged.connect(handle_horizontal_scroll)

        # Aggiorna la larghezza del ruler quando cambia la timeline
        self.scene.sceneRectChanged.connect(self.ruler_scene.update_width)

    def update_zoom(self, zoom_level):
        """Aggiorna lo zoom del ruler quando cambia nella timeline"""
        self.ruler_view.scene().update_zoom(zoom_level)

    def update_track_headers(self):
        """Aggiorna gli header quando cambiano le tracce"""
        self.track_header_view.update_tracks(
            self.scene.num_tracks,
            self.scene.track_height
        )

    def create_ruler_section(self):
        ruler_container = QWidget()
        ruler_layout = QHBoxLayout(ruler_container)
        ruler_layout.setSpacing(0)
        ruler_layout.setContentsMargins(0, 0, 0, 0)

        header_spacer = QWidget()
        header_spacer.setFixedWidth(70)
        ruler_layout.addWidget(header_spacer)

        self.ruler_scene = TimelineRuler(self.scene.settings, self.scene)
        self.timeline_view = TimelineView(self.scene)
        self.ruler_view = TimelineRulerView(self.ruler_scene, self.timeline_view) 
        ruler_layout.addWidget(self.ruler_view)

        return ruler_container

    def create_timeline_section(self):
        """Crea la sezione principale con track headers e timeline"""
        timeline_container = QWidget()
        timeline_layout = QHBoxLayout(timeline_container)
        timeline_layout.setSpacing(0)
        timeline_layout.setContentsMargins(0, 0, 0, 0)

        # Track Headers
        self.track_header_view = TrackHeaderView()
        timeline_layout.addWidget(self.track_header_view)

        # Timeline View
        timeline_layout.addWidget(self.timeline_view)
        # Imposta il riferimento alla timeline view nell'header
        self.track_header_view.set_timeline_view(self.timeline_view)

        return timeline_container

    def get_timeline_view(self):
        return self.timeline_view

    def get_ruler_view(self):
        return self.ruler_view

    def get_track_header_view(self):
        return self.track_header_view