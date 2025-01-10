from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QGraphicsView, QSplitter
from PyQt5.QtCore import Qt, QTimer

"""from TimelineView import TimelineView
from TrackHeaderView import TrackHeaderView
from TimelineRuler import TimelineRuler
"""
from src.TimelineView import TimelineView
from src.TrackHeaderView import TrackHeaderView
from src.TimelineRuler import TimelineRuler


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
        self._scene = scene
        self._timeline_view = None
        self._track_header_view = TrackHeaderView()
        self._timeline_view = TimelineView(self._scene)
        self._track_header_view.set_timeline_view(self._timeline_view)
        self._ruler_view = None
        self._ruler_scene = None
        
        # Imposta dimensioni minime
        self._track_header_view.setMinimumWidth(80)
        self._track_header_view.setMaximumWidth(200)
        self._timeline_view.setMinimumWidth(50)
        self.splitter_handle_width = 1

        self.setup_ui()
        self.setup_connections()

        # Aggiorna le tracce se la scena esiste
        if self._scene:
            self._track_header_view.update_tracks(
                self._scene.num_tracks,
                self._scene.track_height
            )
        QTimer.singleShot(0, self.initialize_views)

    @property
    def scene(self):
        return self._scene

    @property
    def timeline_view(self):
        return self._timeline_view

    @property
    def track_header_view(self):
        return self._track_header_view

    @property
    def ruler_view(self):
        return self._ruler_view

    @property
    def ruler_scene(self):
        return self._ruler_scene

    def initialize_views(self):
        """Inizializza e sincronizza le viste dopo la costruzione"""
        if self._ruler_view:
            self._ruler_view.update_zoom(self._scene.zoom_level)
            self._ruler_view.viewport().update()
            
        # Sincronizza lo scroll orizzontale
        if self._timeline_view:
            current_scroll = self._timeline_view.horizontalScrollBar().value()
            self._ruler_view.horizontalScrollBar().setValue(current_scroll)

        self._timeline_view.verticalScrollBar().setValue(0)  
        self._track_header_view.verticalScrollBar().setValue(0)

    def setup_ui(self):
        # Layout principale
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        if self._scene:
            ruler_container = self.create_ruler_section()
            main_layout.addWidget(ruler_container)

            timeline_container = self.create_timeline_section()
            main_layout.addWidget(timeline_container)

    def setup_connections(self):
        """Configura le connessioni tra i vari componenti"""
        # Sincronizzazione scroll verticale
        self._timeline_view.verticalScrollBar().valueChanged.connect(
            lambda value: self.track_header_view.verticalScrollBar().setValue(value) if self.track_header_view else None)
        if self.track_header_view:
            self.track_header_view.verticalScrollBar().valueChanged.connect(
                self._timeline_view.verticalScrollBar().setValue)

        self._timeline_view.horizontalScrollBar().valueChanged.connect(
            self.handle_horizontal_scroll)

        if self._scene:
            self._scene.sceneRectChanged.connect(lambda: 
                self._ruler_scene.update_width() if self._ruler_scene else None)
        
        splitter = self.findChild(QSplitter)
        if splitter:
            splitter.splitterMoved.connect(self.on_splitter_moved)

        # Forza un aggiornamento iniziale dopo un breve delay
        QTimer.singleShot(100, lambda: 
            self._ruler_view.update_zoom(self._scene.zoom_level) if self._ruler_view else None)

    def handle_horizontal_scroll(self, value):
        ruler_view = getattr(self, '_ruler_view', None)  # Accesso più sicuro
        if ruler_view:
            ruler_view.horizontalScrollBar().setValue(value)
            ruler_view.viewport().update()
        track_header_view = getattr(self, 'track_header_view', None)
        if track_header_view:
            track_header_view.viewport().update()

    def update_zoom(self, zoom_level):
        """Aggiorna lo zoom del ruler quando cambia nella timeline"""
        if self._ruler_view:
            self._ruler_view.scene().update_zoom(zoom_level)

    def update_track_headers(self):
        """Aggiorna gli header quando cambiano le tracce"""
        if self.track_header_view:
            self.track_header_view.update_tracks(
                self._scene.num_tracks,
                self._scene.track_height
            )

    def create_ruler_section(self):
        ruler_container = QWidget()
        ruler_layout = QHBoxLayout(ruler_container)
        ruler_layout.setSpacing(0)
        ruler_layout.setContentsMargins(0, 0, 0, 0)

        # Header spacer con stessa larghezza del track header
        self.header_spacer = QWidget()
        initial_width = self._track_header_view.width() + self.splitter_handle_width
        self.header_spacer.setFixedWidth(initial_width)
        ruler_layout.addWidget(self.header_spacer)

        self._ruler_scene = TimelineRuler(self._scene.settings, self._scene)
        self._ruler_view = TimelineRulerView(self._ruler_scene, self._timeline_view)
        
        # Imposta margini e contenuti a zero per allineamento preciso
        self._ruler_view.setViewportMargins(0, 0, 0, 0)
        self._ruler_view.setContentsMargins(0, 0, 0, 0)
        self._ruler_view.viewport().setContentsMargins(0, 0, 0, 0)
        
        ruler_layout.addWidget(self._ruler_view)

        # Forza l'aggiornamento dopo la creazione
        QTimer.singleShot(0, lambda: self._ruler_view.viewport().update())

        return ruler_container

    def create_timeline_section(self):
        timeline_container = QWidget()
        timeline_layout = QHBoxLayout(timeline_container)
        timeline_layout.setSpacing(0)
        timeline_layout.setContentsMargins(0, 0, 0, 0)

        # Crea splitter e aggiungi le view
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(self.splitter_handle_width)
        
        # Imposta le policy prima di aggiungere al splitter
        self._track_header_view.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        
        # Aggiungi i widget
        splitter.addWidget(self._track_header_view)
        splitter.addWidget(self._timeline_view)
        
        # Imposta i fattori di stretch
        splitter.setStretchFactor(0, 0)  # header view non si estende
        splitter.setStretchFactor(1, 1)  # timeline view si estende
        
        timeline_layout.addWidget(splitter)
        return timeline_container

    def on_splitter_moved(self, pos, index):
        """Gestisce il movimento dello splitter"""
        self.header_spacer.setFixedWidth(pos)
        if self.track_header_view:
            self.track_header_view.current_width = pos
            self.track_header_view.update_tracks_width()