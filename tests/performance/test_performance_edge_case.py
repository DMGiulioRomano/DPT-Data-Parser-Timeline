# tests/performance/test_performance_edge_case.py
from tests.performance import (
    BaseTest,
    time,
    QPointF
)

class PerformanceEdgeCaseTest(BaseTest):
    def test_large_timeline_performance(self):
        """Test performance con timeline grande"""
        start_time = time.time()
        
        # Crea molte tracce e items
        original_tracks = self.timeline.num_tracks
        self.timeline.num_tracks = 100
        
        for i in range(50):
            for track in range(10):
                self.timeline.add_music_item(i, track, 1, f"Test{i}-{track}", 
                                          self.window.settings)
        
        # Verifica tempo di rendering
        end_time = time.time()
        self.assertLess(end_time - start_time, 2.0)  # Non più di 2 secondi
        
        # Verifica performance zoom
        start_time = time.time()
        self.timeline.scale_scene(2.0)
        end_time = time.time()
        self.assertLess(end_time - start_time, 0.5)  # Non più di 500ms

    def test_rapid_operation_stability(self):
        """Test stabilità con operazioni rapide"""
        item = self.timeline.add_music_item(0, 0, 3, "Test", self.window.settings)
        
        # Operazioni rapide multiple
        start_time = time.time()
        for i in range(100):
            item.setSelected(True)
            item.setSelected(False)
            item.setPos(QPointF(i, 0))
            self.timeline.scale_scene(1.0 + (i % 5) / 10)
        
        end_time = time.time()
        self.assertLess(end_time - start_time, 1.0)  # Non più di 1 secondo