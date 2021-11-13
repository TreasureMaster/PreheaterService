"""Настройки меток вывода информации об отправленных пакетах."""


class LabelsConfig:
    _COUNTER_LABELS = {
            'all': 'Все:',
            'good': 'Хорошие:',
            'bad': 'Плохие:',
            'bad_echo': 'Нет эха:',
            'bad_answer': 'Нет ответа',
            'bad_crc': 'CRC',
        }
    _ALL_LABELS = {
            'send': 'Отправлено:',
            'echo': 'Эхо:',
            'answer': 'Ответ:',
            **_COUNTER_LABELS
        }
    _TITLE_LABELS = [
        'Передача',
        'Пакеты',
        'Ошибки'
    ]