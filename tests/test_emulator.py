import unittest
import sys
import os

base_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(base_dir, "..", "src"))

import main

class TestEmulator(unittest.TestCase):
    """Класс автотестов для проверки логики эмулятора командной строки."""
    def test_handle_input_basic_command(self) -> None:
        """Проверяет базовый парсинг команды без аргументов."""
        main.history_list.clear()
        main.execute_command = lambda cmd, args: None

        result = main. handle_input("ls")
        
        self.assertTrue(result)
        self.assertIn("ls", main.history_list)

    def test_handle_input_with_arguments(self) -> None:
        """Проверяет корректное разделение команды и ее аргументов"""
        main.history_list.clear()
        captured = []
        main.execute_command = lambda cmd, args: captured.append((cmd, args))

        main.handle_input("cd home user docs")

        self.assertEqual(captured[0][0], "cd")
        self.assertEqual(captured[0][1], ["home", "user", "docs"])

    def test_handle_input_ignore_pure_comment(self) -> None:
        """Проверяет, что комментарии игнорируются"""
        main.history_list.clear()
        err_msg = "Ошибка: комментарий выполнился"
        main.execute_command = lambda cmd, args: sys.exit(err_msg)

        comment_str = "# Это обычный комментарий, его нельзя выполнять"
        result = main.handle_input(comment_str)

        self.assertTrue(result)
        self.assertEqual(len(main.history_list), 0)

    def test_handle_input_inline_comment(self) -> None:
        """Проверяет отсечение комментария, который идет после рабочей команды"""
        main.history_list.clear()
        captured = []
        main.execute_command = lambda cmd, args: captured.append((cmd, args))
        main.handle_input("ls -la #Показываем скрытые файлы")

        self.assertEqual(captured[0][0], "ls")
        self.assertEqual(captured[0][1], ["-la"])

if __name__ == "__main__":
    unittest.main()