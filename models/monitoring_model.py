from __future__ import annotations

import enum
import dataclasses as dc
import operator
import typing as t


@dc.dataclass
class Monitoring:
    """Общий класс мониторинга"""
    headers: t.List[str]
    # indexes: t.List[str]
    parameters: t.List[Parameter]

    def __getitem__(self, i):
        if item := self.iexist(i):
            return item
        else:
            raise IndexError(f'Не существует параметр с индексом: {i}')

    @property
    def indexes(self):
        # treeview не работает с генератором, нужен tuple или list
        return tuple(f'#{n+1}' for n in range(len(self.headers)))

    def iexist(self, i):
        return next(filter(lambda p: p.key == i, self.parameters), None)

    # def get_headers(self):
    #     return zip(self.indexes, self.titles)


@dc.dataclass
class Parameter:
    """Класс, описывающий каждый параметр"""
    raw_value: t.Union[int, float, list, MonitoringState]
    description: str
    key: int
    ratio: int
    action: t.Optional[Action] = None

    def __post_init__(self):
        if isinstance(self.action, str):
            self.action = Action(self.action)

    @property
    def value(self):
        if self.action is None:
            if isinstance(self.raw_value, list):
                return '; '.join(map(str, self.raw_value))
            return self.raw_value
        else:
            return self.action.execute(self.raw_value, self.ratio)

    def __iter__(self):
        yield self.value
        yield self.description
        yield self.key
        yield self.ratio

class Action(enum.Enum):
    """Действие, производимое для корректировки значения параметра"""
    ADD = '+'
    MUL = '*'
    STATE = 'state'

    def execute(self, a, b):
        """Производит вычисление в зависимости от значения перечисления"""
        DO = {
            '+': operator.add,
            '*': operator.mul,
            'state': self._state
        }
        return DO[self.value](a, b)

    def _state(self, s, n):
        return [
            '0 - выключен',
            '1 - новая запись',
            '2 - мониторинг',
            '3 - пауза'
        ][s]

    # def _add(self, a, b):
    #     """Сложение переданных значений"""
    #     return a + b

    # def _mul(self, a, b):
    #     """Умножение переданных значений"""
    #     return a * b

class MonitoringState(enum.IntEnum):
    """Состояние мониторинга"""
    DISABLED = 0
    NEW = 1
    PROCESS = 2
    PAUSE = 3


if __name__ == '__main__':
    param = Parameter(5, 'one', 128, 2, '*')
    # param = Parameter()
    print(param)
    print(param.value)
    print(list(Action))
    # print(param.action.execute())
    param = Parameter(5, 'two', 128, 2)
    print(param)
    print(param.value)

    print('-'*50)
    print(dir(Monitoring))