# tests/test_performance.py
import psutil
import os
from base_test import BaseTest
import time

class PerformanceTest(BaseTest):
    def test_memory_usage(self):
        """Test utilizzo memoria"""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Crea molti items
        for i in range(100):
            self.timeline.add_music_item(i, 0, 3, f"Test{i}", self.window.settings)
            
        # Verifica che l'uso di memoria non sia eccessivo
        current_memory = process.memory_info().rss
        memory_increase = (current_memory - initial_memory) / 1024 / 1024  # MB
        self.assertLess(memory_increase, 100)  # Non più di 100MB
        
    def test_zoom_performance(self):
        """Test performance zoom"""
        # Aggiungi molti items
        for i in range(50):
            self.timeline.add_music_item(i, 0, 3, f"Test{i}", self.window.settings)
            
        # Misura tempo per zoom
        start_time = time.time()
        self.timeline.scale_scene(2.0)
        end_time = time.time()
        
        self.assertLess(end_time - start_time, 0.5)  # Non più di 500ms