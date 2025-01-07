# Nuovo file: TimelineContainer.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QGraphicsView, QSplitter
from PyQt5.QtCore import Qt, QTimer
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

    def update_zoom(self, zoom_level):
        """Delega l'aggiornamento dello zoom alla scena"""
        if isinstance(self.scene(), TimelineRuler):
            self.scene().update_zoom(zoom_level)

class TimelineContainer(QWidget):
    """
    Container principale che gestisce il layout dell'intera timeline,
    inclusi ruler, track headers e la timeline principale
    """
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.timeline_view = None
        self.track_header_view = TrackHeaderView()
        self.timeline_view = TimelineView(self.scene)
        self.track_header_view.set_timeline_view(self.timeline_view)
        # Imposta dimensioni minime
        self.track_header_view.setMinimumWidth(80)
        self.track_header_view.setMaximumWidth(200)  # Nuovo
        self.timeline_view.setMinimumWidth(50)
        self.splitter_handle_width = 1  
        self.setup_ui()
        self.setup_connections()

        # Aggiungere qui:
        if self.scene:
            self.track_header_view.update_tracks(
                self.scene.num_tracks,
                self.scene.track_height
            )
        QTimer.singleShot(0, self.initialize_views)

    def initialize_views(self):
        """Inizializza e sincronizza le viste dopo la costruzione"""
        if hasattr(self, 'ruler_view') and self.ruler_view:
            self.ruler_view.update_zoom(self.scene.zoom_level)
            self.ruler_view.viewport().update()
            
        # Sincronizza lo scroll orizzontale
        if hasattr(self, 'timeline_view') and self.timeline_view:
            current_scroll = self.timeline_view.horizontalScrollBar().value()
            self.ruler_view.horizontalScrollBar().setValue(current_scroll)

        self.timeline_view.verticalScrollBar().setValue(0)  
        self.track_header_view.verticalScrollBar().setValue(0)


    def setup_ui(self):
        # Layout principale
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Prima creiamo la timeline view
        # 1. Ruler Section
        if self.scene:
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

        def handle_horizontal_scroll(value):
            if hasattr(self, 'ruler_view') and self.ruler_view:
                self.ruler_view.horizontalScrollBar().setValue(value)
                # Forza l'aggiornamento del viewport
                self.ruler_view.viewport().update()
            self.track_header_view.viewport().update()
            
        self.timeline_view.horizontalScrollBar().valueChanged.connect(handle_horizontal_scroll)

        if self.scene:
            self.scene.sceneRectChanged.connect(lambda: 
                self.ruler_scene.update_width() if hasattr(self, 'ruler_scene') else None)
        
        splitter = self.findChild(QSplitter)
        if splitter:
            splitter.splitterMoved.connect(self.on_splitter_moved)

        # Forza un aggiornamento iniziale dopo un breve delay
        QTimer.singleShot(100, lambda: self.ruler_view.update_zoom(self.scene.zoom_level) if hasattr(self, 'ruler_view') else None)


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

        # Header spacer ha la stessa larghezza del track header
        self.header_spacer = QWidget()
        initial_width = self.track_header_view.width() + self.splitter_handle_width
        self.header_spacer.setFixedWidth(initial_width)
        ruler_layout.addWidget(self.header_spacer)

        self.ruler_scene = TimelineRuler(self.scene.settings, self.scene)
        self.ruler_view = TimelineRulerView(self.ruler_scene, self.timeline_view) 
        # Imposta margini e contenuti a zero per allineamento preciso
        self.ruler_view.setViewportMargins(0, 0, 0, 0)
        self.ruler_view.setContentsMargins(0, 0, 0, 0)
        self.ruler_view.viewport().setContentsMargins(0, 0, 0, 0)
        
        ruler_layout.addWidget(self.ruler_view)

        # Forza l'aggiornamento dopo la creazione
        QTimer.singleShot(0, lambda: self.ruler_view.viewport().update())

        return ruler_container

    def create_timeline_section(self):
        """Crea la sezione principale con track headers e timeline"""
        timeline_container = QWidget()
        timeline_layout = QHBoxLayout(timeline_container)
        timeline_layout.setSpacing(0)
        timeline_layout.setContentsMargins(0, 0, 0, 0)

        # Crea splitter e aggiungi le view
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(self.splitter_handle_width) 
        splitter.addWidget(self.track_header_view)
        splitter.addWidget(self.timeline_view)
        
        timeline_layout.addWidget(splitter)
        return timeline_container

    def on_splitter_moved(self, pos, index):
        """Gestisce il movimento dello splitter"""
        self.header_spacer.setFixedWidth(pos)
        if hasattr(self, 'track_header_view'):
            # Forza l'aggiornamento della larghezza degli header
            self.track_header_view.current_width = pos
            self.track_header_view.update_tracks_width()

    def get_timeline_view(self):
        return self.timeline_view

    def get_ruler_view(self):
        return self.ruler_view

    def get_track_header_view(self):
        return self.track_header_view