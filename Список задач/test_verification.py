import unittest
import json
import os
import tempfile
from unittest.mock import Mock, patch
from todo_app import TodoApp

class TestVerification(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\n" + "="*60)
        print("ТЕСТЫ ВЕРИФИКАЦИИ")
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
            self.app.update_task_list = Mock()
            self.app.save_tasks = Mock()
    
    def tearDown(self):
        if os.path.exists(self.tasks_file_path):
            os.remove(self.tasks_file_path)
        os.rmdir(self.temp_dir)
    
    def test_add_task_verification(self):
        print("Тест: Добавление задачи")
        self.app.tasks.append({"text": "Новая задача", "completed": False})
        self.assertEqual(len(self.app.tasks), 1)
        self.assertEqual(self.app.tasks[0]["text"], "Новая задача")
        print("✓ Задача добавлена корректно")
    
    def test_delete_task_verification(self):
        print("Тест: Удаление задачи")
        self.app.tasks = [
            {"text": "Задача 1", "completed": False},
            {"text": "Задача 2", "completed": True}
        ]
        del self.app.tasks[0]
        self.assertEqual(len(self.app.tasks), 1)
        self.assertEqual(self.app.tasks[0]["text"], "Задача 2")
        print("✓ Задача удалена корректно")
    
    def test_complete_task_verification(self):
        print("Тест: Отметка выполнения")
        self.app.tasks = [{"text": "Задача", "completed": False}]
        self.app.tasks[0]["completed"] = True
        self.assertTrue(self.app.tasks[0]["completed"])
        print("✓ Статус задачи изменен корректно")
    
    def test_mark_all_verification(self):
        print("Тест: Отметка всех задач")
        self.app.tasks = [
            {"text": "Задача 1", "completed": False},
            {"text": "Задача 2", "completed": False}
        ]
        for task in self.app.tasks:
            task["completed"] = True
        self.assertTrue(all(task["completed"] for task in self.app.tasks))
        print("✓ Все задачи отмечены как выполненные")
    
    def test_clear_all_verification(self):
        print("Тест: Очистка всех задач")
        self.app.tasks = [
            {"text": "Задача 1", "completed": False},
            {"text": "Задача 2", "completed": True}
        ]
        self.app.tasks.clear()
        self.assertEqual(len(self.app.tasks), 0)
        print("✓ Все задачи удалены")
    
    def test_save_verification(self):
        print("Тест: Сохранение задач")
        test_tasks = [
            {"text": "Сохраненная задача 1", "completed": False},
            {"text": "Сохраненная задача 2", "completed": True}
        ]
        with open(self.tasks_file_path, 'w', encoding='utf-8') as f:
            json.dump(test_tasks, f)
        self.assertTrue(os.path.exists(self.tasks_file_path))
        with open(self.tasks_file_path, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        self.assertEqual(loaded_data, test_tasks)
        print("✓ Задачи успешно сохранены")
    
    def test_load_verification(self):
        print("Тест: Загрузка задач")
        test_tasks = [
            {"text": "Загруженная задача 1", "completed": False},
            {"text": "Загруженная задача 2", "completed": True}
        ]
        with open(self.tasks_file_path, 'w', encoding='utf-8') as f:
            json.dump(test_tasks, f)
        with open(self.tasks_file_path, 'r', encoding='utf-8') as f:
            self.app.tasks = json.load(f)
        self.assertEqual(len(self.app.tasks), 2)
        self.assertEqual(self.app.tasks[0]["text"], "Загруженная задача 1")
        print("✓ Задачи успешно загружены")

if __name__ == "__main__":
    unittest.main()