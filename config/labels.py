"""Настройки меток вывода информации об отправленных пакетах."""


class LabelsConfig:
    _COUNTER_LABELS = {
            'all': 'Все:',
            'good': 'Хорошие:',
            'bad_echo': 'Нет эха:',
            'bad_answer': 'Нет ответа',
        }
    _ALL_LABELS = {
            'send': 'Отправлено:',
            'echo': 'Эхо:',
            'answer': 'Ответ:',
            **_COUNTER_LABELS
        }