class AdvancedFileTest(BaseTest):
    def test_file_state_recovery(self):
        """Test recupero stato file"""
        # Crea stato iniziale
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        item.params['custom_param'] = 42
        
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as tmp:
            self.window.current_file = tmp.name
            self.window.save_to_yaml()
            
            # Modifica stato
            item.params['custom_param'] = 24
            
            # Ricarica file
            self.window.load_from_yaml()
            
            # Verifica recupero stato
            loaded_items = [i for i in self.timeline.items() if isinstance(i, MusicItem)]
            self.assertEqual(loaded_items[0].params['custom_param'], 42)

    def test_autosave_behavior(self):
        """Test comportamento autosave"""
        # Simula chiusura con modifiche non salvate
        self.window.current_file = "test.yaml"
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        
        with patch('PyQt5.QtWidgets.QMessageBox.question') as mock_question:
            mock_question.return_value = QMessageBox.Yes
            self.window.closeEvent(QCloseEvent())
            mock_question.assert_called_once()