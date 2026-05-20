import unittest
import time
import os
import tempfile
import json
from unittest.mock import Mock, patch
from todo_app import TodoApp

class TestPerformance(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\n" + "="*60)
        print("ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ")
        print("="*60 + "\n")
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.tasks_file_path = os.path.join(self.temp_dir, "tasks.json")
        
        with patch('tkinter.Tk'), patch('tkinter.Frame'), patch('tkinter.Label'), \
             patch('tkinter.Button'), patch('tkinter.Entry'), patch('tkinter.Canvas'), \
             patch('tkinter.Scrollbar'), patch('tkinter.Checkbutton'), patch('tkinter.BooleanVar'), \
             patch('tkinter.messagebox'):
            
            self.app = TodoApp(Mock())
            self.app.tasks_file = self.tasks_file_path
            self.app.tasks = []
    
    def tearDown(self):
        if os.path.exists(self.tasks_file_path):
            os.remove(self.tasks_file_path)
        os.rmdir(self.temp_dir)
    
    def test_add_task_performance(self):
        print("Тест: Скорость добавления")
        start = time.time()
        for i in range(100):
            self.app.tasks.append({"text": f"Задача {i}", "completed": False})
        duration = time.time() - start
        self.assertLess(duration, 1.0)
        print(f"✓ 100 задач за {duration:.3f} сек")
    
    def test_delete_all_performance(self):
        print("Тест: Скорость удаления")
        for i in range(100):
            self.app.tasks.append({"text": f"Задача {i}", "completed": False})
        start = time.time()
        self.app.tasks.clear()
        duration = time.time() - start
        self.assertLess(duration, 0.1)
        print(f"✓ 100 задач удалено за {duration:.3f} сек")
    
    def test_large_taskset_performance(self):
        print("Тест: 10000 задач")
        start = time.time()
        for i in range(10000):
            self.app.tasks.append({"text": f"Задача {i}", "completed": False})
        duration = time.time() - start
        self.assertLess(duration, 1.0)
        print(f"✓ 10000 задач создано за {duration:.3f} сек")
    
    def test_save_performance(self):
        print("Тест: Скорость сохранения")
        for i in range(1000):
            self.app.tasks.append({"text": f"Задача {i}", "completed": False})
        start = time.time()
        with open(self.tasks_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.app.tasks, f)
        duration = time.time() - start
        self.assertLess(duration, 0.5)
        print(f"✓ 1000 задач сохранено за {duration:.3f} сек")
    
    def test_load_performance(self):
        print("Тест: Скорость загрузки")
        tasks = [{"text": f"Задача {i}", "completed": False} for i in range(1000)]
        with open(self.tasks_file_path, 'w', encoding='utf-8') as f:
            json.dump(tasks, f)
        start = time.time()
        with open(self.tasks_file_path, 'r', encoding='utf-8') as f:
            self.app.tasks = json.load(f)
        duration = time.time() - start
        self.assertLess(duration, 0.5)
        print(f"✓ 1000 задач загружено за {duration:.3f} сек")

if __name__ == "__main__":
    unittest.main()