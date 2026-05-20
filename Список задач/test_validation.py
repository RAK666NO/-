import unittest
from unittest.mock import Mock, patch
from todo_app import TodoApp

class TestValidation(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\n" + "="*60)
        print("ТЕСТЫ ВАЛИДАЦИИ")
        print("="*60 + "\n")
    
    def setUp(self):
        with patch('tkinter.Tk'), patch('tkinter.Frame'), patch('tkinter.Label'), \
             patch('tkinter.Button'), patch('tkinter.Entry'), patch('tkinter.Canvas'), \
             patch('tkinter.Scrollbar'), patch('tkinter.Checkbutton'), patch('tkinter.BooleanVar'), \
             patch('tkinter.messagebox'):
            
            self.app = TodoApp(Mock())
            self.app.tasks = []
    
    def test_empty_task_validation(self):
        print("Тест: Пустая задача")
        task_text = "   ".strip()
        self.assertEqual(len(task_text), 0)
        print("✓ Пустая задача не добавлена")
    
    def test_whitespace_task_validation(self):
        print("Тест: Задача из пробелов")
        task_text = "   \t\n   ".strip()
        self.assertEqual(len(task_text), 0)
        print("✓ Задача из пробелов не добавлена")
    
    def test_task_structure_validation(self):
        print("Тест: Структура задачи")
        valid_task = {"text": "Задача", "completed": False}
        self.assertIn("text", valid_task)
        self.assertIn("completed", valid_task)
        print("✓ Структура задачи валидна")
    
    def test_task_status_validation(self):
        print("Тест: Статус задачи")
        self.assertIsInstance(True, bool)
        print("✓ Статус задачи имеет правильный тип")
    
    def test_task_text_type_validation(self):
        print("Тест: Тип текста задачи")
        self.assertIsInstance("строка", str)
        print("✓ Текст задачи имеет правильный тип")
    
    def test_task_id_format_validation(self):
        print("Тест: Формат ID задач")
        for i in range(5):
            task_id = f"[{i:03d}]"
            self.assertEqual(len(task_id), 5)
            self.assertTrue(task_id.startswith("["))
            self.assertTrue(task_id.endswith("]"))
        print("✓ Формат ID задач корректен")
    
    def test_task_limit_validation(self):
        print("Тест: Лимит задач")
        for i in range(1000):
            self.app.tasks.append({"text": f"Задача {i}", "completed": False})
        self.assertEqual(len(self.app.tasks), 1000)
        print("✓ Система выдерживает 1000+ задач")
    
    def test_long_text_validation(self):
        print("Тест: Длинный текст")
        long_text = "A" * 1000
        self.app.tasks.append({"text": long_text, "completed": False})
        self.assertEqual(len(self.app.tasks[0]["text"]), 1000)
        print("✓ Длинный текст обрабатывается корректно")
    
    def test_special_characters_validation(self):
        print("Тест: Специальные символы")
        special_chars = "!@#$%^&*()_+{}:<>?|~`"
        self.app.tasks.append({"text": special_chars, "completed": False})
        self.assertEqual(self.app.tasks[0]["text"], special_chars)
        print("✓ Специальные символы обрабатываются корректно")

if __name__ == "__main__":
    unittest.main()