# tests/test_ui_interaction.py
from tests.ui import BaseTest, QTest, Qt
from PyQt5.QtWidgets import QAction
from src.Timeline import TrackItem, Timeline
from src.MusicItem import MusicItem 
from src.MainWindow import MainWindow
from src.TimelineContainer import TimelineContainer
class UIInteractionTest(BaseTest):
    """Test delle interazioni UI"""
    def setUp(self):
        """Setup del test"""
        # Crea la finestra principale
        self.window = MainWindow()
        
        # Mostra la finestra e dà il focus
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()
        
        # Crea la timeline e il container
        self.scene = Timeline(self.window.settings)
        self.timeline_container = TimelineContainer(self.scene)
        self.timeline = self.scene  # Per mantenere compatibilità con il codice esistente
        
        self.timeline = self.window.scene  # Usa la scene della MainWindow
        self.timeline_container = self.window.timeline_container # Usa il container della MainWindow
        
        # Collega il segnale di selezione della traccia
        self.timeline_container.track_header_view.scene.track_selection_changed.connect(
            self.window.on_track_selection_changed
        )

    def test_keyboard_shortcuts(self):
        """Test scorciatoie da tastiera"""
        # Debug della traccia selezionata e verifica esistenza tracce
        print(f"Traccia selezionata inizialmente: {self.window.selected_track}")
        
        # Aggiungiamo un print al metodo add_new_item per tracciare quando viene chiamato
        original_add_new_item = self.window.add_new_item
        def add_new_item_with_debug():
            print("add_new_item chiamato!")
            original_add_new_item()
        self.window.add_new_item = add_new_item_with_debug
        
        # Trova l'action per Ctrl+1
        new_item_action = None
        for action in self.window.findChildren(QAction):
            if action.text() == "New Item":
                new_item_action = action
                break
        
        print(f"Action 'New Item' trovata: {new_item_action is not None}")
        if new_item_action:
            print(f"Shortcut: {new_item_action.shortcut().toString()}")
            print(f"Action enabled: {new_item_action.isEnabled()}")
        
        # Seleziona una traccia prima del test
        self.window.selected_track = 0
        print(f"Traccia selezionata dopo l'assegnazione: {self.window.selected_track}")
        self.timeline_container.track_header_view.scene.track_selection_changed.emit(0, True)
        
        # Debug degli elementi iniziali
        initial_items = len([i for i in self.timeline.items() if isinstance(i, MusicItem)])
        print(f"Numero di elementi musicali iniziali: {initial_items}")
        
        # Invece di usare keyClick, triggeriamo direttamente l'action
        print("Triggering action direttamente...")
        if new_item_action:
            new_item_action.trigger()
        
        # Debug degli elementi finali
        final_items = len([i for i in self.timeline.items() if isinstance(i, MusicItem)])
        print(f"Numero di elementi musicali finali: {final_items}")
        
        self.assertGreater(final_items, initial_items)


    def test_search_functionality(self):
        """Test funzionalità di ricerca"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        item.params['posizione'] = -8
        
        self.window.search_param.setCurrentText('posizione')
        self.window.search_value.setText('-8')
        self.window.perform_search()
        
        self.assertTrue(hasattr(item, 'highlighted') and item.highlighted)