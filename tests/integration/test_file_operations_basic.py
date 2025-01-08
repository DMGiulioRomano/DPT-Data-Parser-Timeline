# tests/integration/test_file_operations_basic.py
from tests.integration import (
    BaseTest,
    MusicItem,
    tempfile, os
)


class FileOperationsTest(BaseTest):
    """Test delle operazioni su file"""
    
    def test_save_and_load(self):
        """Test salvataggio e caricamento"""
        with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as tmp:
            temp_path = tmp.name

        try:
            # Crea dati di test
            item1 = self.timeline.add_music_item(0, 0, 3, "Test1", self.window.settings)
            item2 = self.timeline.add_music_item(2, 1, 4, "Test2", self.window.settings)

            # Salva
            self.window.current_file = temp_path
            self.window.save_to_yaml()

            # Pulisci e ricarica
            self.timeline.clear()
            self.window.load_from_yaml()

            # Verifica
            items = [i for i in self.timeline.items() if isinstance(i, MusicItem)]
            self.assertEqual(len(items), 2)
            
        finally:
            os.unlink(temp_path)