import sys
import os
import argparse

DEFAULT_VFS_NAME = "default_vfs"

CMD_EXIT = "exit"
CMD_LS = "ls"
CMD_CD = "cd"

def show_promt() -> None:
    """Выводит приветственное приглашение к вводу с именем VFS."""
    print(f"{DEFAULT_VFS_NAME}>", end="", flush = True )

def execute_command(command: str, args: list[str]) -> None:
    """Выполняет команду-заглушку или сообщает об ошибке.
    Args:
    command: имя введенной команды.
    args: список аргументов команды."""

    if command in (CMD_LS, CMD_CD):
        args_str = ", ".join(args) if args else "нет"
        print(f"[Заглушка] Вызвана команда: {command}")
        print(f"Аргументы: {args_str}")
    else:
        print(f"Ошибка: неизвестная команда '{command}'")

def handle_input(user_input: str) -> bool:
    """Разбирает введенную строку и управляет жизненным циклом REPL.
    Args:
        user_input: необработанная строка из стандартного ввода.
    Returns:
        bool: True, если нужно продолжить REPL, False — если нужно выйти."""

    trimmed = user_input.strip()
    if not trimmed:
        return True
    if trimmed.startswith("#"):
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

    """Читает и последовательно выполняет команды из стартового скрипта.
    Args:
        script_path: Физический путь к файлу скрипта на диске.
    """

    if not os.path.exists(script_path):
        print(f"Ошибка: Стартовый скрипт не найден по пути {script_path}")
        return
    print(f"\n--- Выполнение стартового скрипта: {script_path} ---")

    with open(script_path, "r", encoding="utf-8") as f:
        for line in f:
            print(f"{DEFAULT_VFS_NAME}> {line}", end="")

            if not handle_input(line):
                break

    print("--- Стартовый скрипт успешно выполнени ---\n")

def parse_arguments() -> argparse.Namespace:
      
      """Парсит аргументы командной строки при запуске приложения.
    Returns:
        argparse.Namespace: Объект с параметрами запуска эмулятора."""  
      parser = argparse.ArgumentParser(description="Эмулятор командной строки UNIX-подобной ОС.")  
      parser.add_argument("--vfs", required = True, help = "Путь к физическому расположению VFS JSON")
      parser.add_argument("--script", required = True, help = "Путь к стартовому скрипту эмулятора")

      return parser.parse_args()  
  
def start_repl() -> None:
    """Основная функция запуска интерактивного REPL-окружения."""
    args = parse_arguments()
    
    print(f"Эмулятор командной строки [23 Вариант]")
    print(f"[DEBUG] Путь к VFS: {args.vfs}")
    print(f"[DEBUG] Путь к скрипту: {args.script}")
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
