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
        #")
        super().__init__(scene)
        self.timeline_view = timeline_view
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedHeight(70)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        if timeline_view:
            # Impostiamo stessa larghezza iniziale della timeline view
            viewport_width = timeline_view.viewport().width()
            self.setMinimumWidth(viewport_width)
            
            # Impostiamo la scena per occupare tutta la larghezza disponibile 
            scene_width = max(timeline_view.scene().width(), viewport_width)
            self.scene().setSceneRect(0, 0, scene_width, self.scene().sceneRect().height())
            
            # Connettiamo il segnale di resize della timeline view
            #timeline_view.installEventFilter(self)        
        # Debug lo stato iniziale
        """print(f"Timeline view reference exists: {timeline_view is not None}")
        h_scroll = self.horizontalScrollBar()
        print("\nRuler Scrollbar Initial State:")
        print(f"Exists: {h_scroll is not None}")
        print(f"Range: {h_scroll.minimum()} to {h_scroll.maximum()}")
        print(f"Page Step: {h_scroll.pageStep()}")
        print(f"Is Visible: {h_scroll.isVisible()}")
        print(f"Is Enabled: {h_scroll.isEnabled()}")
"""
    def debug_scroll_state(self, event_type=""):
        """Debug helper per lo stato della scrollbar del ruler"""
        print(f"\n=== TimelineRulerView Scroll State ({event_type}) ===")
        h_scroll = self.horizontalScrollBar()
        print(f"Value: {h_scroll.value()}")
        print(f"Range: {h_scroll.minimum()} to {h_scroll.maximum()}")
        print(f"Page Step: {h_scroll.pageStep()}")
        if self.timeline_view:
            timeline_scroll = self.timeline_view.horizontalScrollBar()
            print("\nTimeline reference scrollbar state:")
            print(f"Value: {timeline_scroll.value()}")
            print(f"Range: {timeline_scroll.minimum()} to {timeline_scroll.maximum()}")

    def wheelEvent(self, event):
        self.debug_scroll_state("Before Wheel Event")
        #print("\n=== Debug TimelineRulerView Wheel Event ===")
        if self.timeline_view:
            #print("Delegating wheel event to timeline view")
            self.timeline_view.wheelEvent(event)
        else:
            #print("No timeline view to delegate to, handling locally")
            super().wheelEvent(event)
        self.debug_scroll_state("After Wheel Event")

    def update_zoom(self, zoom_level):
        """Delega l'aggiornamento dello zoom alla scena"""
        #print(f"\n=== Debug TimelineRulerView Zoom Update: {zoom_level} ===")
        if isinstance(self.scene(), TimelineRuler):
            #print("Updating ruler scene zoom")
            self.scene().update_zoom(zoom_level)
            #print(f"Current horizontal scroll value: {self.horizontalScrollBar().value()}")
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
        """print("\n=== Connecting Scrollbars ===")
        print(f"Timeline view exists: {self._timeline_view is not None}")
        print(f"Ruler view exists: {hasattr(self, '_ruler_view')}")
        
        if not hasattr(self, '_ruler_view'):
            print("Ruler view not yet initialized, skipping connection")
            return
        """    
        if self._timeline_view and self._ruler_view:
            #print("Both views exist, connecting scrollbars")
            # Connessione per lo scroll orizzontale con controllo di sicurezza
            def safe_scroll_sync(value):
                if hasattr(self, '_ruler_view') and self._ruler_view:
                    self._ruler_view.horizontalScrollBar().setValue(value)
                    
            self._timeline_view.horizontalScrollBar().valueChanged.connect(safe_scroll_sync)
            print("Horizontal scrollbar connection established")     

    def debug_view_state(self):
        """Debug helper per lo stato completo delle viste"""
        """print("\n=== Complete View State Debug ===")
        
        # Timeline State
        print("Timeline View:")
        print(f"Scene Width: {self._timeline_view.scene().width()}")
        print(f"Viewport Width: {self._timeline_view.viewport().width()}")
        print(f"H-Scroll Value: {self._timeline_view.horizontalScrollBar().value()}")
        print(f"V-Scroll Value: {self._timeline_view.verticalScrollBar().value()}")
        
        # Ruler State
        print("\nRuler View:")
        print(f"Scene Width: {self._ruler_view.scene().width()}")
        print(f"Viewport Width: {self._ruler_view.viewport().width()}")
        print(f"H-Scroll Value: {self._ruler_view.horizontalScrollBar().value()}")
        
        # Header State
        print("\nHeader View:")
        print(f"Width: {self._track_header_view.width()}")
        print(f"V-Scroll Value: {self._track_header_view.verticalScrollBar().value()}")
        
        # Geometry
        print("\nGeometry:")
        print(f"Container Size: {self.size()}")
        print(f"Timeline Rect: {self._timeline_view.geometry()}")
        print(f"Ruler Rect: {self._ruler_view.geometry()}")
"""
    def setup_ui(self):
        # Layout principale
        #print("\n=== Setting up UI ===")
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        if self._scene:
            #print("Creating ruler container")
            ruler_container = self.create_ruler_section()
            main_layout.addWidget(ruler_container)
            #print("Creating timeline container")

            timeline_container = self.create_timeline_section()
            main_layout.addWidget(timeline_container)
            #print("About to connect scrollbars")
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
        #print(f"Ruler view created: {self._ruler_view is not None}")
        
        self._ruler_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Forza stesso viewport width tra ruler e timeline
        if self._timeline_view:
            self._ruler_view.setMinimumWidth(self._timeline_view.viewport().width())
            self._ruler_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            
            # Sincronizza viewport
            self._ruler_view.setViewportMargins(0, 0, 0, 0)
            self._ruler_view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            # Impostiamo una policy di sizing che permetta l'espansione orizzontale
            
            # Imposta la scena del ruler alla stessa larghezza della timeline
            self._ruler_scene.setSceneRect(0, 0, self._scene.sceneRect().width(), self._ruler_scene.height())
         
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

        # Crea splitter e configura le proprietà base
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(self.splitter_handle_width)
        self.splitter.setChildrenCollapsible(False)
        
        # Configura il TrackHeaderView con widget wrapper
        header_wrapper = QWidget()
        header_layout = QHBoxLayout(header_wrapper)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        header_layout.addWidget(self._track_header_view)
        
        # Configura il TimelineView
        self._timeline_view.setMinimumWidth(100)
        
        # Configura le policy di sizing
        self._track_header_view.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._timeline_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # Aggiungi i widget al splitter
        self.splitter.addWidget(header_wrapper)
        self.splitter.addWidget(self._timeline_view)
        
        # Imposta le proporzioni dello splitter
        self.splitter.setStretchFactor(0, 0)  # header non si espande
        self.splitter.setStretchFactor(1, 1)  # timeline si espande
        
        # Imposta le dimensioni iniziali
        self.splitter.setSizes([200, 800])
        
        # Connetti il segnale
        self.splitter.splitterMoved.connect(self.on_splitter_moved)
        
        timeline_layout.addWidget(self.splitter)
        return timeline_container

    def on_splitter_moved(self, pos, index):
        """Gestisce il movimento dello splitter"""
        # Applica i limiti
        if pos < 150:
            QTimer.singleShot(0, lambda: self.splitter.moveSplitter(150, index))
            pos = 150
        elif pos > 600:
            QTimer.singleShot(0, lambda: self.splitter.moveSplitter(600, index))
            pos = 600
        
        # Aggiorna header spacer
        if hasattr(self, 'header_spacer'):
            self.header_spacer.setFixedWidth(pos + self.splitter_handle_width)
        
        # Aggiorna track header
        if self._track_header_view:
            self._track_header_view.current_width = pos
            self._track_header_view.update_tracks_width()
        
        # Forza aggiornamento delle viste
        if self._ruler_view:
            self._ruler_view.viewport().update()
            

    def handle_horizontal_scroll(self, value):
        #print("\n=== Debug Horizontal Scroll Sync ===")
        #print(f"handle_horizontal_scroll called with value: {value}")
        
        # Debug timeline scrollbar
        timeline_scroll_value = self._timeline_view.horizontalScrollBar().value()
        #print(f"Timeline scrollbar value: {timeline_scroll_value}")
        
        # Debug ruler view
        ruler_view = getattr(self, '_ruler_view', None)
        #print(f"Ruler view exists: {ruler_view is not None}")
        
        """if ruler_view:
            print(f"Before update - Ruler scrollbar value: {ruler_view.horizontalScrollBar().value()}")
            ruler_view.horizontalScrollBar().setValue(value)
            print(f"After update - Ruler scrollbar value: {ruler_view.horizontalScrollBar().value()}")
            print(f"Timeline scroll range: {self._timeline_view.horizontalScrollBar().minimum()} to {self._timeline_view.horizontalScrollBar().maximum()}")
            print(f"Ruler scroll range: {ruler_view.horizontalScrollBar().minimum()} to {ruler_view.horizontalScrollBar().maximum()}")
            
            ruler_view.viewport().update()
        else:
            print("No ruler_view found!")
"""
            
    # In TimelineContainer.py
    def debug_scroll_state(self):
        """Debug helper per lo stato delle scrollbar"""
        #print("\n=== Scroll State Debug ===")
        
        if self._timeline_view:
            timeline_scroll = self._timeline_view.horizontalScrollBar()
            """print("Timeline Scrollbar:")
            print(f"  Value: {timeline_scroll.value()}")
            print(f"  Range: {timeline_scroll.minimum()} to {timeline_scroll.maximum()}")
            print(f"  Page Step: {timeline_scroll.pageStep()}")
            print(f"  Single Step: {timeline_scroll.singleStep()}")
        """
        if self._ruler_view:
            ruler_scroll = self._ruler_view.horizontalScrollBar()
            """print("Ruler Scrollbar:")
            print(f"  Value: {ruler_scroll.value()}")
            print(f"  Range: {ruler_scroll.minimum()} to {ruler_scroll.maximum()}")
            print(f"  Page Step: {ruler_scroll.pageStep()}")
            print(f"  Single Step: {ruler_scroll.singleStep()}")
"""
    def initialize_views(self):
        """Inizializza e sincronizza le viste dopo la costruzione"""
        """
        print("\n=== Debug View Initialization ===")
        
        if self._is_closing:
            print("View initialization aborted - container is closing")
            return
            
        # Debug dello stato delle viste
        print(f"Timeline view exists: {self._timeline_view is not None}")
        print(f"Ruler view exists: {self._ruler_view is not None}")
        print(f"Track header view exists: {self._track_header_view is not None}")
"""
        # Sincronizza i range orizzontali
        if self._timeline_view and self._ruler_view:
            timeline_scroll = self._timeline_view.horizontalScrollBar()
            ruler_scroll = self._ruler_view.horizontalScrollBar()
            
            # Debug stato iniziale
            #print("\nInitial Scroll State:")
            #print(f"Timeline scroll - Range: {timeline_scroll.minimum()} to {timeline_scroll.maximum()}, Page Step: {timeline_scroll.pageStep()}")
            #print(f"Ruler scroll - Range: {ruler_scroll.minimum()} to {ruler_scroll.maximum()}, Page Step: {ruler_scroll.pageStep()}")
            
            # Usa il range più grande tra i due
            max_range = max(timeline_scroll.maximum(), ruler_scroll.maximum())
            page_step = max(timeline_scroll.pageStep(), ruler_scroll.pageStep())
            
            #print(f"\nSynchronizing horizontal scroll ranges to max: {max_range}, page step: {page_step}")
            
            # Imposta gli stessi valori per entrambe le scrollbar
            timeline_scroll.setMaximum(max_range)
            ruler_scroll.setMaximum(max_range)
            timeline_scroll.setPageStep(page_step)
            ruler_scroll.setPageStep(page_step)
            
            # Sincronizza il valore iniziale
            current_value = timeline_scroll.value()
            ruler_scroll.setValue(current_value)
            
            #print(f"Initial sync complete - Timeline: {timeline_scroll.value()}, Ruler: {ruler_scroll.value()}")

        # Sincronizza i range verticali
        if self._timeline_view and self._track_header_view:
            timeline_v_scroll = self._timeline_view.verticalScrollBar()
            header_v_scroll = self._track_header_view.verticalScrollBar()
            
            # Debug stato verticale iniziale
            #print("\nInitial Vertical Scroll State:")
            #print(f"Timeline vertical scroll - Range: {timeline_v_scroll.minimum()} to {timeline_v_scroll.maximum()}")
            #print(f"Header vertical scroll - Range: {header_v_scroll.minimum()} to {header_v_scroll.maximum()}")
            
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
            
            #print(f"Vertical sync complete - Timeline: {timeline_v_scroll.value()}, Header: {header_v_scroll.value()}")

        # Aggiorna il ruler con il livello di zoom corrente
        if self._ruler_view and not self._is_closing:
            try:
                self._ruler_view.update_zoom(self._scene.zoom_level)
                self._ruler_view.viewport().update()
                #print(f"\nRuler zoom updated to: {self._scene.zoom_level}")
            except RuntimeError as e:
                print(f"Error updating ruler zoom: {e}")

        # Sincronizza lo scroll orizzontale iniziale
        if self._timeline_view and self._ruler_view and not self._is_closing:
            try:
                current_scroll = self._timeline_view.horizontalScrollBar().value()
                self._ruler_view.horizontalScrollBar().setValue(current_scroll)
                #print(f"\nInitial horizontal scroll sync - Value: {current_scroll}")
            except RuntimeError as e:
                print(f"Error in initial horizontal scroll sync: {e}")
        # Imposta il valore iniziale delle scrollbar verticali a 0
        if self._timeline_view and not self._is_closing:
            self._timeline_view.verticalScrollBar().setValue(0)
            #print("\nTimeline vertical scroll reset to 0")
                
        if self._track_header_view and not self._is_closing:
            self._track_header_view.verticalScrollBar().setValue(0)
            #print("Track header vertical scroll reset to 0")

        if self._timeline_view and self._ruler_view:
            current_scroll = self._timeline_view.horizontalScrollBar().value()
            self._ruler_view.horizontalScrollBar().setValue(current_scroll)
        """# Verifica finale dello stato
        if self._timeline_view and self._ruler_view:
            print("\nFinal Scroll State:")
            print(f"Timeline horizontal value: {self._timeline_view.horizontalScrollBar().value()}")
            print(f"Ruler horizontal value: {self._ruler_view.horizontalScrollBar().value()}")
            if self._track_header_view:
                print(f"Header vertical value: {self._track_header_view.verticalScrollBar().value()}")
"""
    def setup_connections(self):
        """Configura le connessioni tra i vari componenti"""
        # Verifica presenza delle view necessarie
        """if not hasattr(self, '_timeline_view') or not hasattr(self, '_track_header_view'):
            print("Views non inizializzate, skip connessioni")
            return
"""
        # 1. Configurazione scrollbar verticali
        timeline_scroll = self._timeline_view.verticalScrollBar()
        header_scroll = self._track_header_view.verticalScrollBar()

        # Sincronizza i range
        max_value = max(timeline_scroll.maximum(), header_scroll.maximum())
        page_step = max(timeline_scroll.pageStep(), header_scroll.pageStep())
        
        timeline_scroll.setMaximum(max_value)
        header_scroll.setMaximum(max_value)
        timeline_scroll.setPageStep(page_step)
        header_scroll.setPageStep(page_step)

        # 2. Connessione bidirezionale delle scrollbar
        # Da timeline a header
        timeline_scroll.valueChanged.connect(header_scroll.setValue)
        # Da header a timeline
        header_scroll.valueChanged.connect(timeline_scroll.setValue)

        # 3. Configurazione scrollbar orizzontali per ruler
        if hasattr(self, '_ruler_view'):
            timeline_h_scroll = self._timeline_view.horizontalScrollBar()
            ruler_h_scroll = self._ruler_view.horizontalScrollBar()

            # Sincronizza range orizzontali
            h_max = max(timeline_h_scroll.maximum(), ruler_h_scroll.maximum())
            h_page = max(timeline_h_scroll.pageStep(), ruler_h_scroll.pageStep())
            
            timeline_h_scroll.setMaximum(h_max)
            ruler_h_scroll.setMaximum(h_max)
            timeline_h_scroll.setPageStep(h_page)
            ruler_h_scroll.setPageStep(h_page)

            # Connessione bidirezionale orizzontale
            timeline_h_scroll.valueChanged.connect(ruler_h_scroll.setValue)
            ruler_h_scroll.valueChanged.connect(timeline_h_scroll.setValue)

        # 4. Connessione track header view alla timeline
        self._track_header_view.set_timeline_view(self._timeline_view)
        """
        # 5. Debug output
        print(f"Connections setup complete")
        print(f"Vertical range: max={max_value}, page_step={page_step}")
        if hasattr(self, '_ruler_view'):
            print(f"Horizontal range: max={h_max}, page_step={h_page}")"""
    
        if hasattr(self, '_ruler_view'):
            timeline_h_scroll = self._timeline_view.horizontalScrollBar()
            ruler_h_scroll = self._ruler_view.horizontalScrollBar()

            # Sincronizza i range
            h_max = max(timeline_h_scroll.maximum(), ruler_h_scroll.maximum())
            h_page = max(timeline_h_scroll.pageStep(), ruler_h_scroll.pageStep())
            
            timeline_h_scroll.setMaximum(h_max)
            ruler_h_scroll.setMaximum(h_max)
            timeline_h_scroll.setPageStep(h_page)
            ruler_h_scroll.setPageStep(h_page)

            # Connetti gli scroll
            timeline_h_scroll.valueChanged.connect(ruler_h_scroll.setValue)
            ruler_h_scroll.valueChanged.connect(timeline_h_scroll.setValue)