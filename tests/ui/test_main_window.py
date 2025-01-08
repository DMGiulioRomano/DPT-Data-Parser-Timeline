# tests/test_main_window.py
class MainWindowTest(BaseTest):
    def test_menu_actions(self):
        """Test azioni menu"""
        # Test File Menu
        self.window._setup_file_menu(self.window.menuBar())
        # Simula New File
        self.window.new_file()
        self.assertIsNone(self.window.current_file)
        
    def test_grid_operations(self):
        """Test operazioni griglia"""
        initial_grid = self.window.scene.grid_division
        self.window.increase_grid()
        self.assertEqual(self.window.scene.grid_division, initial_grid * 2)
        
    def test_window_title_update(self):
        """Test aggiornamento titolo finestra"""
        self.window.current_file = "test.yaml"
        self.window.update_window_title()
        self.assertTrue(self.window.windowTitle().endswith("test.yaml"))

    def test_log_message(self):
        """Test messaggi log"""
        test_message = "Test log message"
        self.window.log_message(test_message)
        self.assertIn(test_message, self.window.log_window.toPlainText())
        
    def test_make_command(self):
        """Test comando make"""
        self.window.current_file = "test.yaml"
        # Mock subprocess.run
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "Success"
            self.window.run_make_command()
            mock_run.assert_called_once()

    def test_search_functionality(self):
        """Test completo funzionalità di ricerca"""
        # Test ricerca numerica
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        item.params['posizione'] = -8
        self.window.search_param.setCurrentText('posizione')
        self.window.search_value.setText('-8')
        self.window.perform_search()
        self.assertTrue(item.highlighted)

        # Test ricerca lista
        item.params['ritmo'] = [7, 15]
        self.window.search_param.setCurrentText('ritmo')
        self.window.search_value.setText('[7, 15]')
        self.window.perform_search()
        self.assertTrue(item.highlighted)

    def test_shortcuts_dialog(self):
        """Test dialog scorciatoie"""
        with patch('PyQt5.QtWidgets.QMessageBox.information') as mock_info:
            self.window.show_shortcuts()
            mock_info.assert_called_once()

    def test_modify_item_width(self):
        """Test modifica larghezza item"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        initial_width = item.rect().width()
        self.window.modify_item_width(1.2)
        self.assertAlmostEqual(item.rect().width(), initial_width * 1.2, places=1)