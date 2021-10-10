"""Это модуль связи LIN, совместимый с чипом FTDI. (первая версия)"""

import serial, time

from typing import List

class LIN:

    # Поле BREAK - это 13 или более нулевых битов подряд
    BREAK_LENGTH = 14
    # Поле синхронизации. Позволяет устройствам настроиться на скорость приема/передачи.
    SYNC_BYTE = 0x55
    # Старт/стоп биты и т.п. формируются автоматически pyserial (стандартная настройка 8N1)
    # Коэффициенты пауз (между повторными стартами и для начально старта)
    LIN_WAKEUP_RATIO = 100
    LIN_START_RATIO = 10 * LIN_WAKEUP_RATIO

    def __init__(self, portnum: str, baud: int=9600, enhanced=False):
        self.__portNumber = portnum
        self.__enhanced = enhanced
        self.__breakSignal = LIN.BREAK_LENGTH / baud
        try:
            self.__portInstance = serial.Serial(self.__portNumber, baud, timeout=0.1)
        except IOError as e:
            print(e)
            raise
        # Маркер старта шины LIN (только что запущена или уже работает)
        self.__initLIN = True
        # Отметка времени определения паузы
        self.__time_marker = time.time()

    def is_start_needed(self) -> bool:
        """Проверят, нужно ли посылать стартовый фрейм (будить шину LIN)."""
        # DEPRECATED возможно, не будет использоваться,
        # т.к. по условию заказчика BREAK нужно отправлять всегда
        # return (self.__initLIN or
        #         (time.time() - self.__time_marker) > self.__breakSignal * self.LIN_WAKEUP_RATIO)
        return True

    def close(self) -> None:
        """Закрывает соединение LIN."""
        self.__portInstance.close()
 
    def byte2hex_text(self, byte_line: bytes) -> str:
        '''Преобразует байтовую строку в шестнадцатеричное строковое представление,
        например для вывода.
        '''
        # DEPRECATED будет удалено, т.к. используется вспомогательно.
        return ''.join([ "%02X " % x for x in byte_line ]).strip()

    def byte2hex_list(self, byte_line: bytes) -> str:
        '''Преобразует байтовую строку в шестнадцатеричный список.'''
        return list(map(int, byte_line))

    def send_start(self) -> None:
        """Стартовая пауза для начала работы с шиной LIN."""
        # Передает время, после которого необходимо будет активировать BREAK (13 нулевых битов)
        # Отправка BREAK только при старте и при длительных паузах
        # (чтобы не было начальных 0х00 при получении ответа)
        if self.is_start_needed():
            self.__portInstance.send_break(self.__breakSignal)
            # По условию заказчика, нужно ждать чуть больше длины 1 байта
            time.sleep(0.7 * self.__breakSignal)
            if self.__initLIN:
                # пауза ожидания "пробуждения" LIN (чтобы не ловить начальные пустые ответы)
                time.sleep(self.__breakSignal * self.LIN_START_RATIO)
                self.__initLIN = False
            # print('wake up LIN bus !!!')

    def send_header(self, PID: int) -> None:
        # Стартовый фрейм BREAK (начальная пауза)
        self.send_start()
        # Отправить байт 0x55 (поле синхронизации для настройки скорости)
        self.__portInstance.write(chr(self.SYNC_BYTE).encode('latin-1'))
        # Поле PID (поле идентификатора устройства). Номер устройства (6 бит). Кроме служебных (0x3C, 0x3F).
        # Также здесь передается количество передаваемых байт Frame Data
        # (0x00-0x1F - 2 байта, 0x20-0x2F - 4 байта, 0x30-0x3F - 8 байт)
        self.__portInstance.write(chr(PID).encode('latin-1'))

    def get_response(self, readlen: int, view_text: bool = False) -> str:
        # Очистить все входные буферы
        self.__portInstance.flushInput()
        '''
        Важно :
        В случае трансивера LIN вывод передатчика подсоединяется обратно к выводу приемника
        для диагностических целей.
        
        Следовательно, первые 2 прочитанных байта приведут к SYNC (0x55) &
        Address(передается в заголовке) байт.
        
        Для фактического сообщения мы читаем эти 2 байта и отбрасываем их.
        '''
        # Удалить байт синхронизации 0x55
        # self.__portInstance.read(1)
        if view_text:
            return self.byte2hex_text(self.__portInstance.read(readlen))
        else:
            return self.byte2hex_list(self.__portInstance.read(readlen))

    def send_data(self, message: List[int], PID: int) -> None:
        tmpBuffer = bytearray(i for i in message)
        if self.__enhanced:
            tmpBuffer = bytearray((PID,)) + tmpBuffer
        tmpBuffer.append(self.calc_CRC(tmpBuffer))
        self.__portInstance.write(tmpBuffer)

    def calc_CRC(self, message: List[int]) -> int:
        """Расчет контрольной суммы.
        Контрольная сумма рассчитывается согласно следующей формуле:
        CRC = INV (data byte 1 ⊕ data byte 2 ⊕ ... ⊕ data byte 8)"""
        return (~sum(message) & 0xFF)

    def send_command(self, PID: int, message: List[int]) -> None:
        """Команда для LIN-устройства."""
        self.send_header(PID)
        # time.sleep(.001)
        self.send_data(message, PID)
        self.__updateTimeMarker()

    def get_answer(self, PID: int) -> None:
        """Запрос ответа у LIN-устройства."""
        self.send_header(PID)
        self.__updateTimeMarker()

    def __updateTimeMarker(self) -> None:
        """Помечает время для контроля паузы между запросами."""
        self.__time_marker = time.time()


if __name__ == '__main__':
    nano = LIN('COM3', 9600)
    data = (nano.calc_CRC([0x01, 0x40]))
    # print(hex(data & (2**32 - 1)))
    print(data)
    # nano.sendHeader(0xC4)
    # mark = True
    # while mark:
    #     if (text := nano.readResponse(24)):
    #         mark = False
    #         print(text)
    #     else:
    #         print('nothing')
    # print(text)
    # print(len(text))