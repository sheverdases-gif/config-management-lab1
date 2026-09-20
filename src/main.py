import sys
import os
import argparse
import json

DEFAULT_VFS_NAME = "default_vfs"

CMD_EXIT = "exit"
CMD_LS = "ls"
CMD_CD = "cd"

vfs_tree = {}
current_path = []
vfs_name = "vfs"

def load_vfs(vfs_path: str) -> None:
    
    """Загружает структуру виртуальной файловой системы из JSON-файла.
    Args:
        vfs_path: Путь к файлу vfs.json на диске."""
    
    global vfs_tree, vfs_name
    if not os.path.exists(vfs_path):
        print(f"Ошибка: файл VFS не найден по пути {vfs_path}")
        sys.exit(1)
    try:
        with open(vfs_path, "r", encoding = "utf-8") as f:
            vfs_tree = json.load(f)
        vfs_name = os.path.splitext(os.path.basename(vfs_path))[0]
    except json.JSONDecodeError:
        print(f"Ошибка: файл {vfs_path} содержит некорректный json")
        sys.exit(1)

def get_current_dir_node() -> dict:

    """Возвращает JSON-узел текущей директории, в которой находится пользователь.
    Returns:
        dict: Узел текущей папки из vfs_tree."""
    
    node = vfs_tree
    for folder in current_path:
        if "children" in node and folder in node["children"]:
            node = node["children"][folder]
    return node

def show_promt() -> None:

    """Выводит приветственное приглашение к вводу с именем VFS."""

    path_str = "/" + "/".join(current_path)
    print(f"[{vfs_name} {path_str}]>", end="", flush = True )

def execute_command(command: str, args: list[str]) -> None:

    """Выполняет команду-заглушку или сообщает об ошибке.
    Args:
    command: имя введенной команды.
    args: список аргументов команды."""
    current_node = get_current_dir_node()

    if command == CMD_LS:
        if "children" in current_node and current_node["children"]:
            items = list(current_node["children"].keys())
            print("  ".join(items))
        else:
            pass
    elif command == CMD_CD:
        if not args:
            current_path.clear()
            return

        target = args[0]
        if target == "..":
            if current_path:
                current_path.pop()
        elif "children" in current_node and target in current_node["children"]:
            child_node = current_node["children"][target]
            if child_node.get("type") == "dir":
                current_path.append(target)
            else:
                print(f"cd: не является директорией: {target}")
        else:
            print(f"cd: нет такого файла или директории {target}")
    else:
        print(f"Ошибка: неизвестная команда '{command}'")

def handle_input(user_input: str) -> bool:

    """Разбирает введенную строку и управляет жизненным циклом REPL.
    Args:
        user_input: необработанная строка из стандартного ввода.
    Returns:
        bool: True, если нужно продолжить REPL, False — если нужно выйти."""

    trimmed = user_input.strip()
    if not trimmed or trimmed.startswith("#"):
        return True
    if "#" in trimmed:
        trimmed = trimmed.split("#")[0].strip()

    tokens = trimmed.split()
    if not tokens:
        return True
    
    command = tokens[0]
    args = tokens[1:]

    if command == CMD_EXIT:
        print("Завершение работы эмулятора.")
        return False

    execute_command(command, args)
    return True

def run_start_script(script_path: str) -> None:

    """Читает и последовательно выполняет команды из стартового скрипта."""

    if not os.path.exists(script_path):
        print(f"Ошибка: Стартовый скрипт не найден по пути {script_path}")
        return
    
    print(f"\n--- Выполнение стартового скрипта: {script_path} ---")
    with open(script_path, "r", encoding="utf-8") as f:
        for line in f:
            path_str = "/" + "/".join(current_path)
            print(f"[{vfs_name}{path_str}]> {line}", end="")

            if not handle_input(line):
                break

    print("--- Стартовый скрипт успешно выполненен ---\n")

def parse_arguments() -> argparse.Namespace:
      
      """Парсит аргументы командной строки при запуске приложения."""

      parser = argparse.ArgumentParser(description="Эмулятор командной строки UNIX-подобной ОС.")  
      parser.add_argument("--vfs", required = True, help = "Путь к физическому расположению VFS JSON")
      parser.add_argument("--script", required = True, help = "Путь к стартовому скрипту эмулятора")

      return parser.parse_args()  
  
def start_repl() -> None:

    """Основная функция запуска интерактивного REPL-окружения."""

    args = parse_arguments()

    load_vfs(args.vfs)

    print(f"Эмулятор командной строки [23 Вариант]")
    print(f"[DEBUG] модель VFS успешно загружена из: {args.vfs}")
    print(f'Введите "{CMD_EXIT}" для выхода.\n')

    run_start_script(args.script)

    while True:
        show_promt()
        try:
            line = sys.stdin.readline()
            if not line:
                print("\nЗавершение работы эмулятора.")
                break
            if not handle_input(line):
                break
        except KeyboardInterrupt:
            print("\nЗаверщение работы эмулятора.")
            break
if __name__ == "__main__":
    start_repl()
