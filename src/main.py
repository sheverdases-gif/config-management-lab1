import sys

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
    
    tokens = trimmed.split()
    command = tokens[0]
    args = tokens[1:]

    if command == CMD_EXIT:
        print("Завершение работы эмулятора.")
        return False

    execute_command(command, args)
    return True

def start_repl() -> None:
    """Основная функция запуска интерактивного REPL-окружения."""
    print(f"Эмулятор командной строки [23 Вариант]")
    print(f'Введите "{CMD_EXIT}" для выхода.\n')

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
