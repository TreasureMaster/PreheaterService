import serial

from serial.serialutil import PortNotOpenError

from connections import microsleep


class MicroSerial(serial.Serial):
    """Класс serial.Serial с более точными значениями сигналов."""
    def send_break(self, duration=0.25):
        """\
        Отправить условие перерыва. По времени;
        возвращается в состояние ожидания по истечении заданного времени.
        """
        if not self.is_open:
            raise PortNotOpenError()
        self.break_condition = True
        microsleep.sleep(duration)
        self.break_condition = False