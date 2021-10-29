import logging, sys, io
from threading import Lock

from accessify import private


class AppLogger:

    DEBUG_LEVELV_NUM = 11
    # DEBUG_THREAD_NUM = 22
    __instance = None
    __logger = None
    __stream = None
    __lock = Lock()

    @private
    def __init__(self):
        self.__addLoggingLevel('DEBUGV', AppLogger.DEBUG_LEVELV_NUM)
        # self.__addLoggingLevel('THREAD', AppLogger.DEBUG_THREAD_NUM)
        AppLogger.__logger = logging.getLogger('app')
        AppLogger.__logger.setLevel(logging.DEBUG)
        # AppLogger.__logger.debugv = self.debugv
        # print(logging._nameToLevel)
        self.__make_handlers()
        
        # self.__add_filter()
        # self.__logger = CustomLoggerAdapter(self.__logger, {'username': 'adilkhash'})

    def __addLoggingLevel(self, levelName, levelNum, methodName=None):
        """Устанавливает пользовательский уровень level."""
        if not methodName:
            methodName = levelName.lower()

        if hasattr(logging, levelName):
           raise AttributeError('{} already defined in logging module'.format(levelName))
        if hasattr(logging, methodName):
           raise AttributeError('{} already defined in logging module'.format(methodName))
        if hasattr(logging.getLoggerClass(), methodName):
           raise AttributeError('{} already defined in logger class'.format(methodName))

        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, args, **kwargs)
        def logToRoot(message, *args, **kwargs):
            logging.log(levelNum, message, *args, **kwargs)

        logging.addLevelName(levelNum, levelName)
        setattr(logging, levelName, levelNum)
        setattr(logging.getLoggerClass(), methodName, logForLevel)
        setattr(logging, methodName, logToRoot)

    @staticmethod
    def instance():
        with AppLogger.__lock:
            if AppLogger.__instance is None:
                AppLogger.__instance = AppLogger()
            return AppLogger.__logger

    @staticmethod
    def get_stream():
        # TODO потом заменить командами для потока, а не отдавать поток
        return AppLogger.__instance.__stream.getvalue()

    @staticmethod
    def set_command_stream(command):
        # TODO возможно нужно будет использовать инициализацию, если до этого момента не будет создан экземпляр AppLogger
        # AppLogger.instance()
        AppLogger.__instance.__stream.add_command(command)

    def __make_handlers(self):
        # handler - куда будут записаны логи
        self.__stream = CommandsStringIO()
        # TODO заменить на MemoryHandler ?
        self.handler = logging.StreamHandler(stream=self.__stream)
        # self.stream.write('Test entry...')
        # self.stream.flush()
        self.handler.setLevel(logging.INFO)
        self.handler.setFormatter(self.__make_formatter())
        fh = logging.FileHandler('tmplog/test.log', 'w', encoding='utf-8')
        fh.setLevel(logging.ERROR)
        # fh.setLevel(logging.THREAD)
        fh.setFormatter(self.__get_formatter())
        fh.addFilter(self.MyFilter(logging.ERROR))
        # fh.addFilter(self.MyFilter(logging.THREAD))
        AppLogger.__logger.addHandler(self.handler)
        AppLogger.__logger.addHandler(fh)

    def __make_formatter(self):
        # formatter - как будет записано сообщение (какой будет вывод)
        outline = '[%(asctime)s: %(levelname)s] %(message)s'
        return logging.Formatter(fmt=outline)

    def __get_formatter(self):
        # formatter - как будет записано сообщение (какой будет вывод)
        outline = '[%(asctime)s: %(levelname)s] - [%(name)s - (%(filename)s).%(funcName)s()-=[%(lineno)s]=-] - %(message)s'
        return logging.Formatter(fmt=outline)

    def __add_filter(self):
        # filter выводит сообщения только с заданным условием (н-р, в тексте должно быть слово python)
        def filter_python(record):
            return record.getMessage().find('python') != -1
        AppLogger.__logger.addFilter(filter_python)

    class MyFilter:
        """Фильтр соответствия уровню level."""
        def __init__(self, level):
            self.__level = level

        def filter(self, logRecord):
            return logRecord.levelno == self.__level


# Класс потока с выполнением команд
class CommandsStringIO(io.StringIO):
    """Переопределение потока StringIO для выполнения команды."""
    def add_command(self, command=None):
        if not hasattr(self, 'outer_commands'):
            self.outer_commands = []
        if command:
            self.outer_commands.append(command)

    def write(self, s):
        super().write(s)
        if hasattr(self, 'outer_commands'):
            for command in self.outer_commands:
                command.execute()
            # Очистка потока для новых данных
            self.truncate(0)
            self.seek(0)


# тест адаптера
# Адаптер добавляет некоторую информацию к выводу (можно динамически)
class CustomLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f'{msg} := from {self.extra["username"]}', kwargs