import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import main

class TestEmulator(unittest.TestCase):
    """Класс автотестов для проверки логики эмулятора командной строки."""
    def setUp(self) -> None:
        """Подготовка окруженния перед каждым тестом"""
        main.history_list.clear()
    def test_handle_input_basic_command(self) -> None:
        """Проверяет базовый парсинг команды без аргументов"""
        main.execute_command = lambda cmd, args: None

        result = main. handle_input("ls")

        self.assertTrue(result)
        self.assertIn("ls", main.history_list)

    def test_handle_input_with_arguments(self) -> None:
        """Проверяет корректное разделение команды и ее аргументов"""
        captured = []
        main.execute_command = lambda cmd, args: captured.append((cmd, args))
        main.handle_input("cd home user docs")

        self.assertEqual(captured[0][0], "cd")
        self.assertEqual(captured[0][1], ["home", "user", "docs"])

    def test_handle_input_ignore_pure_comment(self) -> None:
        """Проверяет, что комментарии игнорируются"""
        main.execute_command = lambda cmd, args: sys.exit("Ошибка: комментарий выполнился")

        result = main.handle_input("# Это обычный комментарий, его нельзя выполнять")

        self.assertTrue(result)
        self.assertEqual(len(main.history_list), 0)

    def test_handle_input_inline_comment(self) -> None:
        """Проверяет отсечение комментария, который идет после рабочей команды"""
        captured = []
        main.execute_command = lambda cmd, args: captured.append((cmd, args))
        main.handle_input("ls -la #Показываем скрытые файлы")

        self.assertEqual(captured[0][0], "ls")
        self.assertEqual(captured[0][1], ["-la"])

if __name__ == "__main__":
    unittest.main()