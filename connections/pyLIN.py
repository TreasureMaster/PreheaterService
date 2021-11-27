"""Это модуль связи LIN, совместимый с чипом FTDI. (первая версия)"""

from typing import List

from connections import microserial, microsleep

class LIN:

    # Поле BREAK - это 13 или более нулевых битов подряд
    BREAK_LENGTH = 13
    # Поле синхронизации. Позволяет устройствам настроиться на скорость приема/передачи.
    SYNC_BYTE = 0x55
    # Старт/стоп биты и т.п. формируются автоматически pyserial (стандартная настройка 8N1)
    # Коэффициенты пауз (между повторными стартами и для начально старта)
    LIN_WAKEUP_RATIO = 100
    LIN_START_RATIO = 10 * LIN_WAKEUP_RATIO

    def __init__(self, portnum: str, baud: int=9600):
        self.__portNumber = portnum
        # self.__enhanced = enhanced
        self.__breakSignal = LIN.BREAK_LENGTH / baud
        try:
            self.__portInstance = microserial.MicroSerial(self.__portNumber, baud, timeout=0.028)
        except IOError as e:
            print(e)
            raise
        # Маркер старта шины LIN (только что запущена или уже работает)
        self.__initLIN = True
        # Отметка времени определения паузы
        # self.__time_marker = time.time()

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
            microsleep.sleep(0.4 * self.__breakSignal)
            if self.__initLIN:
                # пауза ожидания "пробуждения" LIN (чтобы не ловить начальные пустые ответы)
                microsleep.sleep(self.__breakSignal * self.LIN_START_RATIO)
                self.__initLIN = False
            # print('wake up LIN bus !!!')

    def send_header(self, PID: int) -> None:
        # Стартовый фрейм BREAK (начальная пауза)
        self.send_start()
        # Создать заголовок
        header = bytearray((self.SYNC_BYTE, PID))
        # Отправить байт 0x55 (поле синхронизации для настройки скорости)
        # self.__portInstance.write(chr(self.SYNC_BYTE).encode('latin-1'))
        # Поле PID (поле идентификатора устройства). Номер устройства (6 бит). Кроме служебных (0x3C, 0x3F).
        # Также здесь передается количество передаваемых байт Frame Data
        # (0x00-0x1F - 2 байта, 0x20-0x2F - 4 байта, 0x30-0x3F - 8 байт)
        # self.__portInstance.write(chr(PID).encode('latin-1'))
        self.__portInstance.write(header)
        return header

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
        # Ожидать синхро-байт 0x55 или конца длины запрашиваемого количества байт
        for _ in range(readlen):
            start_byte = self.__portInstance.read(1)
            # print('type first:', start_byte, type(start_byte))
            if int.from_bytes(start_byte, 'big') == 0x55:
                break

        if view_text:
            # b = self.__portInstance.read(readlen)
            # print('type package:', b, type(b))
            return self.byte2hex_text(start_byte + self.__portInstance.read(readlen))
            # return self.byte2hex_text(start_byte + b)
        else:
            return self.byte2hex_list(start_byte + self.__portInstance.read(readlen))

    def send_data(self, message: List[int], PID: int) -> None:
        tmpBuffer = bytearray(i for i in message)
        # if self.__enhanced:
        #     tmpBuffer = bytearray((PID,)) + tmpBuffer
        tmpBuffer.append(self.calc_CRC(tmpBuffer))
        self.__portInstance.write(tmpBuffer)
        return self._view_package(PID, tmpBuffer)

    # def calc_CRC(self, message: List[int]) -> int:
    #     """Расчет контрольной суммы.
    #     Контрольная сумма рассчитывается согласно следующей формуле:
    #     CRC = INV (data byte 1 ⊕ data byte 2 ⊕ ... ⊕ data byte 8)"""
    #     return (~sum(message) & 0xFF)

    def calc_CRC(self, message: List[int]) -> int:
        """Расчет контрольной суммы.

        Контрольная сумма рассчитывается согласно следующей формуле:
        CRC = INV (data byte 1 ⊕ data byte 2 ⊕ ... ⊕ data byte 8)
        Контрольная сумма рассчитывается со сдвигом."""
        result = ~sum(message)
        while True:
            high, low = divmod(result, 256)
            if high:
                result = high + low
            else:
                break
        return result

    # def check_CRC(self, message):
    #     return self.calc_CRC(message)

    def send_command(self, PID: int, message: List[int]) -> None:
        """Команда для LIN-устройства."""
        self.send_header(PID)
        return self.byte2hex_text(self.send_data(message, PID))
        # self.__updateTimeMarker()

    def get_answer(self, PID: int) -> None:
        """Запрос ответа у LIN-устройства."""
        self.send_header(PID)
        # self.__updateTimeMarker()

    def _view_package(self, PID, tmpBuffer):
        """Возвращаемое значение пакета для отображения в окне менеджера."""
        return bytearray((self.SYNC_BYTE, PID)) + tmpBuffer

    # def __updateTimeMarker(self) -> None:
    #     """Помечает время для контроля паузы между запросами."""
    #     self.__time_marker = time.time()


class LIN2(LIN):
    """Реализация шины LIN 2.xx"""

    def __init__(self, portnum: str, baud: int=9600):
        super().__init__(portnum, baud)

    def send_data(self, message: List[int], PID: int) -> None:
        """Вариант отправки LIN 2.xx"""
        tmpBuffer = bytearray(i for i in message)
        # tmpBuffer = bytearray((PID,)) + tmpBuffer
        tmpBuffer.append(self.calc_CRC(bytearray((PID,)) + tmpBuffer))
        # print(tmpBuffer)
        self._LIN__portInstance.write(tmpBuffer)
        return self._view_package(PID, tmpBuffer)


# Общее описание вариантов LIN
LIN_REVISIONS = {
    'LIN 1.x': LIN,
    'LIN 2.x': LIN2
}

LIN_REVISIONS_NAMES = list(LIN_REVISIONS.keys())
LIN_REVISIONS_BUSES = list(LIN_REVISIONS.values())


if __name__ == '__main__':
    import time
    nano1 = LIN('COM3', 9600)
    data = (nano1.calc_CRC([0x01, 0x40]))
    print(nano1.byte2hex_text([data]))
    nano1.send_data([0x01, 0x40], 0x03)
    nano1.close()
    time.sleep(.5)

    print('-'*30)
    nano2 = LIN2('COM3', 9600)
    data = (nano2.calc_CRC([0x03, 0x01, 0x40]))
    # print(hex(data & (2**32 - 1)))
    print(nano2.byte2hex_text([data]))
    print(nano2.BREAK_LENGTH)
    nano2.send_data([0x01, 0x40], 0x03)
    # nano2.get_all()
    nano2.close()
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
    print('-'*30)
    print(LIN_REVISIONS_NAMES)
    print(LIN_REVISIONS_BUSES)