import unittest
from PyQt5.QtCore import QObject
from src.models.music_clip import MusicClipModel, MusicClipParams

class TestMusicClipModel(unittest.TestCase):
    def setUp(self):
        self.clip = MusicClipModel("Test Clip")
        self.signal_received = False
        self.signal_data = None

    def test_initialization(self):
        """Test corretta inizializzazione del modello"""
        self.assertEqual(self.clip.name, "Test Clip")
        self.assertEqual(self.clip.params.cAttacco, 0.0)
        self.assertEqual(self.clip.params.durataArmonica, 26)
        self.assertEqual(self.clip.params.ritmo, [7, 15])
        self.assertEqual(self.clip.params.durata, 5.0)
        self.assertEqual(self.clip.params.ampiezza, [-30, -0.25])
        self.assertEqual(self.clip.params.frequenza, [6, 1])
        self.assertEqual(self.clip.params.posizione, -8)

    def test_name_validation(self):
        """Test validazione del nome"""
        with self.assertRaises(ValueError):
            self.clip.name = ""
        with self.assertRaises(ValueError):
            self.clip.name = "   "
        
        # Test nome valido
        self.clip.name = "New Name"
        self.assertEqual(self.clip.name, "New Name")

    def test_param_validation(self):
        """Test validazione dei parametri"""
        # Test valore numerico valido
        self.clip.set_param("cAttacco", 1.5)
        self.assertEqual(self.clip.params.cAttacco, 1.5)

        # Test conversione tipo
        self.clip.set_param("durataArmonica", 20.0)
        self.assertEqual(self.clip.params.durataArmonica, 20)
        self.assertIsInstance(self.clip.params.durataArmonica, int)

        # Test lista valida
        self.clip.set_param("ritmo", [8, 16])
        self.assertEqual(self.clip.params.ritmo, [8, 16])

        # Test errori
        with self.assertRaises(ValueError):
            self.clip.set_param("invalid_param", 1.0)
        with self.assertRaises(ValueError):
            self.clip.set_param("ritmo", [1])  # Lista lunghezza errata

    def test_signals(self):
        """Test emissione corretta dei segnali"""
        def on_param_changed(param_name, value):
            self.signal_received = True
            self.signal_data = (param_name, value)

        def on_name_changed(new_name):
            self.signal_received = True
            self.signal_data = new_name

        # Test segnale cambio parametro
        self.clip.params_changed.connect(on_param_changed)
        self.clip.set_param("cAttacco", 2.0)
        self.assertTrue(self.signal_received)
        self.assertEqual(self.signal_data, ("cAttacco", 2.0))

        # Reset e test segnale cambio nome
        self.signal_received = False
        self.signal_data = None
        self.clip.name_changed.connect(on_name_changed)
        self.clip.name = "New Name"
        self.assertTrue(self.signal_received)
        self.assertEqual(self.signal_data, "New Name")

    def test_position_tracking(self):
        """Test tracking della posizione"""
        # Test posizione iniziale
        self.assertEqual(self.clip.position, (0.0, 0.0))
        
        # Test aggiornamento posizione
        self.clip.position = (10.5, 20.0)
        self.assertEqual(self.clip.position, (10.5, 20.0))

        # Test segnale posizione
        def on_position_changed(x, y):
            self.signal_received = True
            self.signal_data = (x, y)

        self.clip.position_changed.connect(on_position_changed)
        self.clip.position = (30.0, 40.0)
        self.assertTrue(self.signal_received)
        self.assertEqual(self.signal_data, (30.0, 40.0))

    def test_track_index(self):
        """Test gestione track index"""
        self.assertEqual(self.clip.track_index, 0)
        
        self.clip.track_index = 2
        self.assertEqual(self.clip.track_index, 2)
        
        with self.assertRaises(ValueError):
            self.clip.track_index = -1

    def test_serialization(self):
        """Test serializzazione/deserializzazione"""
        # Modifica alcuni valori
        self.clip.name = "Test Serialization"
        self.clip.set_param("cAttacco", 1.5)
        self.clip.set_param("ritmo", [10, 20])

        # Serializza
        data = self.clip.to_dict()
        
        # Verifica dati serializzati
        self.assertEqual(data["name"], "Test Serialization")
        self.assertEqual(data["cAttacco"], 1.5)
        self.assertEqual(data["ritmo"], [10, 20])

        # Deserializza in nuovo oggetto
        new_clip = MusicClipModel.from_dict(data)
        
        # Verifica valori
        self.assertEqual(new_clip.name, self.clip.name)
        self.assertEqual(new_clip.params.cAttacco, self.clip.params.cAttacco)
        self.assertEqual(new_clip.params.ritmo, self.clip.params.ritmo)