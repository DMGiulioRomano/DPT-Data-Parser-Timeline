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
        print("\n=== Debug TimelineRulerView Initialization ===")
        super().__init__(scene)
        self.timeline_view = timeline_view
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedHeight(70)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Debug lo stato iniziale
        print(f"Timeline view reference exists: {timeline_view is not None}")
        h_scroll = self.horizontalScrollBar()
        print("\nRuler Scrollbar Initial State:")
        print(f"Exists: {h_scroll is not None}")
        print(f"Range: {h_scroll.minimum()} to {h_scroll.maximum()}")
        print(f"Page Step: {h_scroll.pageStep()}")
        print(f"Is Visible: {h_scroll.isVisible()}")
        print(f"Is Enabled: {h_scroll.isEnabled()}")

    def wheelEvent(self, event):
        print("\n=== Debug TimelineRulerView Wheel Event ===")
        if self.timeline_view:
            print("Delegating wheel event to timeline view")
            self.timeline_view.wheelEvent(event)
        else:
            print("No timeline view to delegate to, handling locally")
            super().wheelEvent(event)

    def update_zoom(self, zoom_level):
        """Delega l'aggiornamento dello zoom alla scena"""
        print(f"\n=== Debug TimelineRulerView Zoom Update: {zoom_level} ===")
        if isinstance(self.scene(), TimelineRuler):
            print("Updating ruler scene zoom")
            self.scene().update_zoom(zoom_level)
            print(f"Current horizontal scroll value: {self.horizontalScrollBar().value()}")
        else:
            print("Warning: Scene is not a TimelineRuler instance")
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
        self._scene = scene
        self._track_header_view = TrackHeaderView()
        self._timeline_view = TimelineView(self._scene)
        self._track_header_view.set_timeline_view(self._timeline_view)
        self._ruler_scene = TimelineRuler(self._scene.settings, self._scene)
        self._ruler_view = TimelineRulerView(self._ruler_scene, self._timeline_view)
        self._is_closing = False    
        # Imposta dimensioni minime
        self._track_header_view.setMinimumWidth(80)
        self._track_header_view.setMaximumWidth(200)
        self._timeline_view.setMinimumWidth(50)
        self.splitter_handle_width = 1

        self.setup_ui()
        QTimer.singleShot(10, self.setup_connections)

        # Aggiorna le tracce se la scena esiste
        if self._scene:
            self._track_header_view.update_tracks(
                self._scene.num_tracks,
                self._scene.track_height
            )
        QTimer.singleShot(0, self.initialize_views)

        QTimer.singleShot(100, self.setup_scroll_sync)  # Aggiungiamo questo

    def setup_scroll_sync(self):
        """Setup della sincronizzazione dello scroll dopo l'inizializzazione"""
        if self._timeline_view and self._ruler_view:
            timeline_scroll = self._timeline_view.horizontalScrollBar()
            ruler_scroll = self._ruler_view.horizontalScrollBar()
            
            # Sincronizza i range
            max_range = max(timeline_scroll.maximum(), ruler_scroll.maximum())
            page_step = max(timeline_scroll.pageStep(), ruler_scroll.pageStep())
            
            timeline_scroll.setMaximum(max_range)
            ruler_scroll.setMaximum(max_range)
            timeline_scroll.setPageStep(page_step)
            ruler_scroll.setPageStep(page_step)
            
            # Connetti gli scroll
            timeline_scroll.valueChanged.connect(
                lambda value: ruler_scroll.setValue(value))
            ruler_scroll.valueChanged.connect(
                lambda value: timeline_scroll.setValue(value))

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

    def closeEvent(self, event):
        """Gestisce la pulizia durante la chiusura"""
        self._is_closing = True
        super().closeEvent(event)

    def connect_scrollbars(self):
        """Connette le scrollbar tra timeline e ruler"""
        print("\n=== Connecting Scrollbars ===")
        print(f"Timeline view exists: {self._timeline_view is not None}")
        print(f"Ruler view exists: {hasattr(self, '_ruler_view')}")
        
        if not hasattr(self, '_ruler_view'):
            print("Ruler view not yet initialized, skipping connection")
            return
            
        if self._timeline_view and self._ruler_view:
            print("Both views exist, connecting scrollbars")
            # Connessione per lo scroll orizzontale con controllo di sicurezza
            def safe_scroll_sync(value):
                if hasattr(self, '_ruler_view') and self._ruler_view:
                    self._ruler_view.horizontalScrollBar().setValue(value)
                    
            self._timeline_view.horizontalScrollBar().valueChanged.connect(safe_scroll_sync)
            print("Horizontal scrollbar connection established")     

    def setup_ui(self):
        # Layout principale
        print("\n=== Setting up UI ===")
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        if self._scene:
            print("Creating ruler container")
            ruler_container = self.create_ruler_section()
            main_layout.addWidget(ruler_container)
            print("Creating timeline container")

            timeline_container = self.create_timeline_section()
            main_layout.addWidget(timeline_container)
            print("About to connect scrollbars")
            QTimer.singleShot(0, self.connect_scrollbars)
            
    def _safe_update_ruler(self):
        """Metodo sicuro per aggiornare il ruler"""
        if not self._is_closing and self._ruler_view:
            try:
                self._ruler_view.update_zoom(self._scene.zoom_level)
            except RuntimeError:
                pass

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
        print(f"Ruler view created: {self._ruler_view is not None}")
        
        """
        # Forza stesso viewport width tra ruler e timeline
        if self._timeline_view:
            viewport_width = self._timeline_view.viewport().width()
            self._ruler_view.setViewportMargins(0, 0, 0, 0)
            self._ruler_view.setFixedWidth(viewport_width)
            self._ruler_view.viewport().setFixedWidth(viewport_width)
            
            # Aggiorna il range della scrollbar per riflettere il nuovo viewport
            ruler_scrollbar = self._ruler_view.horizontalScrollBar()
            timeline_scrollbar = self._timeline_view.horizontalScrollBar()
            ruler_scrollbar.setRange(0, timeline_scrollbar.maximum())
            ruler_scrollbar.setPageStep(timeline_scrollbar.pageStep())
        """
        ruler_layout.addWidget(self._ruler_view)

        # Forza l'aggiornamento dopo la creazione
        QTimer.singleShot(0, lambda: self._ruler_view.viewport().update())

        return ruler_container

    def resizeEvent(self, event):
        """Gestisce il ridimensionamento della finestra"""
        super().resizeEvent(event)
        
        # Aggiorna la larghezza del ruler quando la timeline viene ridimensionata
        if self._timeline_view and self._ruler_view:
            viewport_width = self._timeline_view.viewport().width()
            self._ruler_view.setFixedWidth(viewport_width)
            self._ruler_view.viewport().setFixedWidth(viewport_width)
            
            # Ricalcola i range delle scrollbar
            ruler_scrollbar = self._ruler_view.horizontalScrollBar()
            timeline_scrollbar = self._timeline_view.horizontalScrollBar()
            ruler_scrollbar.setRange(0, timeline_scrollbar.maximum())
            ruler_scrollbar.setPageStep(timeline_scrollbar.pageStep())
            
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

    def setup_connections(self):
        """Configura le connessioni tra i vari componenti"""
        # Rimuovi le vecchie connessioni se esistono
        if hasattr(self, '_timeline_scroll_connection'):
            try:
                self._timeline_view.verticalScrollBar().valueChanged.disconnect(
                    self._timeline_scroll_connection)
            except TypeError:
                pass
                
        if hasattr(self, '_header_scroll_connection'):
            try:
                self._track_header_view.verticalScrollBar().valueChanged.disconnect(
                    self._header_scroll_connection)
            except TypeError:
                pass

        def on_timeline_scroll(value):
            if self._track_header_view and not self._is_closing:
                try:
                    header_scroll = self._track_header_view.verticalScrollBar()
                    header_scroll.setValue(value)
                except Exception as e:
                    print(f"Error in timeline scroll sync: {e}")

        def on_header_scroll(value):
            if self._timeline_view and not self._is_closing:
                try:
                    timeline_scroll = self._timeline_view.verticalScrollBar()
                    timeline_scroll.setValue(value)
                except Exception as e:
                    print(f"Error in header scroll sync: {e}")

        # Connetti i segnali
        self._timeline_scroll_connection = on_timeline_scroll
        self._header_scroll_connection = on_header_scroll
        
        self._timeline_view.verticalScrollBar().valueChanged.connect(on_timeline_scroll)
        self._track_header_view.verticalScrollBar().valueChanged.connect(on_header_scroll)

        def on_timeline_horizontal_scroll(value):
            if self._ruler_view and not self._is_closing:
                try:
                    ruler_scroll = self._ruler_view.horizontalScrollBar()
                    print(f"Current ruler scroll value: {ruler_scroll.value()}")
                    print(f"Setting ruler scroll to: {value}")
                    ruler_scroll.setValue(value)
                    print(f"Ruler scroll after set: {ruler_scroll.value()}")
                    print(f"Timeline horizontal scroll changed to: {value}")
                    self._ruler_view.horizontalScrollBar().setValue(value)
                    print(f"Ruler scroll value after update: {self._ruler_view.horizontalScrollBar().value()}")
                except RuntimeError as e:
                    print(f"Error in horizontal scroll sync: {e}")
        
        # Connetti lo scroll orizzontale
        self._timeline_view.horizontalScrollBar().valueChanged.connect(on_timeline_horizontal_scroll)

        # Sincronizza i range iniziali
        def sync_ranges():
            if self._timeline_view and self._track_header_view:
                timeline_scroll = self._timeline_view.verticalScrollBar()
                header_scroll = self._track_header_view.verticalScrollBar()
                max_value = max(timeline_scroll.maximum(), header_scroll.maximum())
                timeline_scroll.setMaximum(max_value)
                header_scroll.setMaximum(max_value)

        # Esegui la sincronizzazione dopo che l'interfaccia è stata renderizzata
        QTimer.singleShot(0, sync_ranges)

    def handle_horizontal_scroll(self, value):
        print("\n=== Debug Horizontal Scroll Sync ===")
        print(f"handle_horizontal_scroll called with value: {value}")
        
        # Debug timeline scrollbar
        timeline_scroll_value = self._timeline_view.horizontalScrollBar().value()
        print(f"Timeline scrollbar value: {timeline_scroll_value}")
        
        # Debug ruler view
        ruler_view = getattr(self, '_ruler_view', None)
        print(f"Ruler view exists: {ruler_view is not None}")
        
        if ruler_view:
            print(f"Before update - Ruler scrollbar value: {ruler_view.horizontalScrollBar().value()}")
            ruler_view.horizontalScrollBar().setValue(value)
            print(f"After update - Ruler scrollbar value: {ruler_view.horizontalScrollBar().value()}")
            print(f"Timeline scroll range: {self._timeline_view.horizontalScrollBar().minimum()} to {self._timeline_view.horizontalScrollBar().maximum()}")
            print(f"Ruler scroll range: {ruler_view.horizontalScrollBar().minimum()} to {ruler_view.horizontalScrollBar().maximum()}")
            ruler_view.viewport().update()
        else:
            print("No ruler_view found!")

    # In TimelineContainer.py
    def debug_scroll_state(self):
        """Debug helper per lo stato delle scrollbar"""
        print("\n=== Scroll State Debug ===")
        
        if self._timeline_view:
            timeline_scroll = self._timeline_view.horizontalScrollBar()
            print("Timeline Scrollbar:")
            print(f"  Value: {timeline_scroll.value()}")
            print(f"  Range: {timeline_scroll.minimum()} to {timeline_scroll.maximum()}")
            print(f"  Page Step: {timeline_scroll.pageStep()}")
            print(f"  Single Step: {timeline_scroll.singleStep()}")
        
        if self._ruler_view:
            ruler_scroll = self._ruler_view.horizontalScrollBar()
            print("Ruler Scrollbar:")
            print(f"  Value: {ruler_scroll.value()}")
            print(f"  Range: {ruler_scroll.minimum()} to {ruler_scroll.maximum()}")
            print(f"  Page Step: {ruler_scroll.pageStep()}")
            print(f"  Single Step: {ruler_scroll.singleStep()}")

    def initialize_views(self):
        """Inizializza e sincronizza le viste dopo la costruzione"""
        print("\n=== Debug View Initialization ===")
        
        if self._is_closing:
            print("View initialization aborted - container is closing")
            return
            
        # Debug dello stato delle viste
        print(f"Timeline view exists: {self._timeline_view is not None}")
        print(f"Ruler view exists: {self._ruler_view is not None}")
        print(f"Track header view exists: {self._track_header_view is not None}")

        # Sincronizza i range orizzontali
        if self._timeline_view and self._ruler_view:
            timeline_scroll = self._timeline_view.horizontalScrollBar()
            ruler_scroll = self._ruler_view.horizontalScrollBar()
            
            # Debug stato iniziale
            print("\nInitial Scroll State:")
            print(f"Timeline scroll - Range: {timeline_scroll.minimum()} to {timeline_scroll.maximum()}, Page Step: {timeline_scroll.pageStep()}")
            print(f"Ruler scroll - Range: {ruler_scroll.minimum()} to {ruler_scroll.maximum()}, Page Step: {ruler_scroll.pageStep()}")
            
            # Usa il range più grande tra i due
            max_range = max(timeline_scroll.maximum(), ruler_scroll.maximum())
            page_step = max(timeline_scroll.pageStep(), ruler_scroll.pageStep())
            
            print(f"\nSynchronizing horizontal scroll ranges to max: {max_range}, page step: {page_step}")
            
            # Imposta gli stessi valori per entrambe le scrollbar
            timeline_scroll.setMaximum(max_range)
            ruler_scroll.setMaximum(max_range)
            timeline_scroll.setPageStep(page_step)
            ruler_scroll.setPageStep(page_step)
            
            # Sincronizza il valore iniziale
            current_value = timeline_scroll.value()
            ruler_scroll.setValue(current_value)
            
            print(f"Initial sync complete - Timeline: {timeline_scroll.value()}, Ruler: {ruler_scroll.value()}")

        # Sincronizza i range verticali
        if self._timeline_view and self._track_header_view:
            timeline_v_scroll = self._timeline_view.verticalScrollBar()
            header_v_scroll = self._track_header_view.verticalScrollBar()
            
            # Debug stato verticale iniziale
            print("\nInitial Vertical Scroll State:")
            print(f"Timeline vertical scroll - Range: {timeline_v_scroll.minimum()} to {timeline_v_scroll.maximum()}")
            print(f"Header vertical scroll - Range: {header_v_scroll.minimum()} to {header_v_scroll.maximum()}")
            
            max_v_range = max(timeline_v_scroll.maximum(), header_v_scroll.maximum())
            v_page_step = max(timeline_v_scroll.pageStep(), header_v_scroll.pageStep())
            
            # Imposta gli stessi valori per le scrollbar verticali
            timeline_v_scroll.setMaximum(max_v_range)
            header_v_scroll.setMaximum(max_v_range)
            timeline_v_scroll.setPageStep(v_page_step)
            header_v_scroll.setPageStep(v_page_step)
            
            # Sincronizza il valore verticale iniziale
            v_current_value = timeline_v_scroll.value()
            header_v_scroll.setValue(v_current_value)
            
            print(f"Vertical sync complete - Timeline: {timeline_v_scroll.value()}, Header: {header_v_scroll.value()}")

        # Aggiorna il ruler con il livello di zoom corrente
        if self._ruler_view and not self._is_closing:
            try:
                self._ruler_view.update_zoom(self._scene.zoom_level)
                self._ruler_view.viewport().update()
                print(f"\nRuler zoom updated to: {self._scene.zoom_level}")
            except RuntimeError as e:
                print(f"Error updating ruler zoom: {e}")

        # Sincronizza lo scroll orizzontale iniziale
        if self._timeline_view and self._ruler_view and not self._is_closing:
            try:
                current_scroll = self._timeline_view.horizontalScrollBar().value()
                self._ruler_view.horizontalScrollBar().setValue(current_scroll)
                print(f"\nInitial horizontal scroll sync - Value: {current_scroll}")
            except RuntimeError as e:
                print(f"Error in initial horizontal scroll sync: {e}")
        # Imposta il valore iniziale delle scrollbar verticali a 0
        if self._timeline_view and not self._is_closing:
            self._timeline_view.verticalScrollBar().setValue(0)
            print("\nTimeline vertical scroll reset to 0")
                
        if self._track_header_view and not self._is_closing:
            self._track_header_view.verticalScrollBar().setValue(0)
            print("Track header vertical scroll reset to 0")

        # Verifica finale dello stato
        if self._timeline_view and self._ruler_view:
            print("\nFinal Scroll State:")
            print(f"Timeline horizontal value: {self._timeline_view.horizontalScrollBar().value()}")
            print(f"Ruler horizontal value: {self._ruler_view.horizontalScrollBar().value()}")
            if self._track_header_view:
                print(f"Header vertical value: {self._track_header_view.verticalScrollBar().value()}")