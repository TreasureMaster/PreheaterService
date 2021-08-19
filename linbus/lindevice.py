'''
Реализация класса работы модуля с шиной LIN.
'''
from .pyLIN import LIN

from typing import List
from .config import LINConfig


class LINBusCommandLengthError(Exception):
    pass


# LINConfig - просто имплементация констант, которые потом можно заменить внешними
class LINDevice(LINConfig):

    def __init__(self, port, baud=None):
        self.linbus = LIN(port, baud)

    def send_short_command(self, cmd: List[int]) -> None:
        """Отправка короткой команды отопителю."""
        if len(cmd) != 2:
            raise LINBusCommandLengthError
        self.linbus.send_command(self.SHORT_COMMAND, cmd)

    def send_long_command(self, cmd: List[int]) -> None:
        """Отправка длинной команды отопителю."""
        if len(cmd) != 8:
            raise LINBusCommandLengthError
        self.linbus.send_command(self.LONG_COMMAND, cmd)

    def get_short_answer(self) -> str:
        """Запрос ответа на короткую команду отопителю."""
        self.linbus.get_answer(self.SHORT_ANSWER)
        return self.linbus.get_response(self.SHORT_ANS_LENGTH)

    def get_long_answer(self) -> str:
        """Запрос ответа на длинную команду отопителю."""
        self.linbus.get_answer(self.LONG_ANSWER)
        return self.linbus.get_response(self.LONG_ANS_LENGTH)


    def scheduleDiagMsg2(self, msg):
        if len(msg) == self.SHORT_CMD_LENGTH:
            self.send_short_command(msg)
        else:
            self.send_long_command(msg)
        answer = self.linbus.get_response(16)
        print('эхо после команды:', answer)

        # self.linbus.getAnswer(0x85)
        print('запрос короткого ответа:')
        print (self.get_short_answer())
        # self.linbus.getAnswer(0xC4)
        print('запрос длинного ответа:')
        print (self.get_long_answer())

    def scheduleDiagMsg(self, msg):
        self.linbus.send_command(0x03, msg)
        print('эхо после команды:', self.linbus.get_response(16))

        self.linbus.get_answer(0x85)
        print('запрос короткого ответа:')
        print (self.linbus.get_response(26))
        self.linbus.get_answer(0xC4)
        print('запрос длинного ответа:')
        return self.linbus.get_response(26)


if __name__ == '__main__':
    import time
    device = LINDevice('COM3', 9600)
    print ("Entering while loop...")
    count = 5
    msg = [0x01, 0x40]
    # msg = [0x01, 0x40, 0x01, 0x40, 0x01, 0x40, 0x01, 0x40]

    while count:
        print(count, end=': ')
        print()
        # print (device.scheduleDiagMsg([0x01, 0x40]))
        if count == 1:
            time.sleep(1)
        device.scheduleDiagMsg2(msg)
        count -= 1

    device.linbus.close()
    print ("Done !! ")
