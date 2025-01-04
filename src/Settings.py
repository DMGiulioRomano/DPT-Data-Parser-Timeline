import json
import os
from pathlib import Path

class Settings:
    def __init__(self):
        # Ottiene il percorso della directory corrente dello script
        current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.settings_file = current_dir / 'settings.json'
        
        self.default_settings = {
            'last_open_directory': str(current_dir),
            'last_save_directory': str(current_dir),
            'make_directory': str(current_dir),
            'default_duration': 5,
            'default_track_count': 8,
            'text_color': '#000000',
            'item_text_size': 12,
            'timeline_text_size': 14,
        }
        self.current_settings = {}
        self.load_settings()

    def load_settings(self):
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    self.current_settings = json.load(f)
            else:
                self.current_settings = self.default_settings.copy()
                self.save_settings()
        except Exception as e:
            print(f"Errore nel caricamento delle impostazioni: {e}")
            self.current_settings = self.default_settings.copy()

    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.current_settings, f, indent=4)
        except Exception as e:
            print(f"Errore nel salvataggio delle impostazioni: {e}")

    def get(self, key, default=None):
        return self.current_settings.get(key, default)

    def set(self, key, value):
        self.current_settings[key] = value
        self.save_settings()