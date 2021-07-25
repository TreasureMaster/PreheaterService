"""Исключения проекта."""

class FNModuleInvalidModeException(Exception):
    """Исключение для неподдерживемого режима работы модуля.

    mode - режим работы, вызвавший ошибку
    message - сообщение об ошибке
    """
    def __init__(self, mode: str, message: str = 'Invalid mode of module') -> None:
        self.mode = mode
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}: '{self.mode}'"