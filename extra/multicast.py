"""Реализация отправки в несколько очередей без использования потока."""
from ast import Add
import queue
import typing as t
import threading as th

import dataclasses as dc
import events as evs


# Событие выхода из потока распределения
class MulticastClose:
    pass

# Отправка запрещена полностью
class MulticastSendStop(Exception):
    pass

# Получение данных из очереди запрещено
# class ReceiveNotAllowed(Exception):
#     pass


# Обертка очереди, собирающая события Event и условия Condition
@dc.dataclass
class QueueWrapper:
    """Оболочка очереди"""
    BREAK:   t.ClassVar[int] = 0
    CONTROL: t.ClassVar[int] = 1

    name: str
    __queue: queue.Queue
    # по умолчанию процесс отправки не контролируется событием отправки
    is_controlled: bool = dc.field(default=False)
    _events: t.List[th.Event] = dc.field(default_factory=list, repr=False, compare=False)
    timeout: t.Optional[t.Union[int, float]] = dc.field(default=None)
    # Я думаю, что условие теперь не нужно, т.к. очереди контролируются (просто добавить get с timeout)
    # _conditions: t.List[th.Condition] = dc.field(default_factory=list, repr=False, compare=False)

    def __post_init__(self):
        # Количество точек контроля (событий)
        control_count = 2 if self.is_controlled else 1
        # Первое событие - жесткий контроль остановки, второе - мягкий (если контролируется отправка)
        # Второе событие проверяет допустимость отправки, если это контролируется
        # WARN нельзя просто умножить список; события 0 и 1 будут одинаковы !!!
        self._events = [th.Event() for _ in range(control_count)] + self._events

    def __len__(self):
        return self.__queue.qsize()

    # TODO только для тестирования, затем нужно удалить
    def events(self):
        return self._events

    # ------------------------------ Методы очереди ------------------------------ #

    def put(self, item, block=True, timeout=None):
        """Кладет посылку в очередь."""
        if self.is_allowed:
            self.__queue.put(item, block, timeout)
            # теперь надо уведомить всех потребителей о том, что появились данные
            # for cv in self._conditions:
            #     with cv:
            #         # наверное уведомить всех, пока нет контроля числа уведомлений
            #         cv.notify_all()

    def get(self, block=True, timeout=None):
        """Получить значение из очереди; стандартное решение"""
        return self.__queue.get(block, timeout)

    def get_nowait(self):
        """Получить значение из очереди немедленно; поднять исключение, если пусто; стандартное решение"""
        return self.__queue.get_nowait()

    def get_wait(self):
        """Получить значение из очереди, ожидая 'timeout' секунд"""
        if self.is_permitted():
            try:
                package = self.__queue.get(timeout=self.timeout)
            except queue.Empty:
                # отправляем None
                pass
            else:
                if not isinstance(self.__queue, queue.SimpleQueue):
                    self.__queue.task_done()
                return package

    def get_instantly(self):
        """Получить значение из очереди немедленно или None, если нет значения"""
        # Класть нельзя, но выбирать можно
        if self.is_permitted():
            try:
                package = self.__queue.get_nowait()
            except queue.Empty:
                # отправляем None
                pass
            else:
                if not isinstance(self.__queue, queue.SimpleQueue):
                    self.__queue.task_done()
                return package

    def clear(self):
        """Очистить очередь"""
        self.__queue.queue.clear()

    @property
    def is_allowed(self):
        """Проверка событий на предмет допуска в очередь."""
        # True - если вообще нет событий
        # однако, если события есть, все они должны быть установлены
        return all(event.is_set() for event in self._events)

    # ------------------------- Контроль отправки пакета ------------------------- #

    def hard_start(self):
        """Разрешение работать"""
        self._events[self.BREAK].set()

    def hard_stop(self):
        """Полный запрет работы с очисткой очереди"""
        self._events[self.BREAK].clear()
        self.clear()

    def is_broken(self):
        """Полный запрет?"""
        return not self._events[self.BREAK].is_set()

    def is_permitted(self):
        """Разрешено работать?"""
        # print(self.__events[self.BREAK].is_set())
        return self._events[self.BREAK].is_set()

    def start(self):
        """Разрешение работы для контролируемой очереди"""
        if self.is_controlled:
            self._events[self.CONTROL].set()

    def stop(self):
        """Запрет отправки в контролируемую очередь"""
        if self.is_controlled:
            self._events[self.CONTROL].clear()

    # Здесь только контроль старта отправки, сама отправка может быть ограничена другими событиями
    def is_started(self):
        if self.is_controlled:
            return self._events[self.CONTROL].is_set()
        else:
            return True

# Все регистрируемые очереди будут получать посылку
class MulticastQueue:
    __PREFIX = '__!__'
    __SUFFIX = '_NAMED_QUEUE'

    def __init__(
        self,
        # неконтролируемые очереди (работают всегда, кроме явной блокировки)
        *queues: t.Union[queue.Queue, QueueWrapper],
        # по умолчанию следующие очереди контролируются
        is_controlled: bool = True,
        # контролируемые очереди (можно запретить наполнение отдельно от получения)
        **controlled_queues: t.Union[queue.Queue, QueueWrapper]
    ):
        self._output_queues = {}
        self.__events = evs.Events()
        # Очереди, куда будет отправлена вошедшая посылка
        for name, adding_queue in controlled_queues.items():
            # Для ключевых параметров очередь контролируется
            self.append(adding_queue, name, is_controlled=is_controlled)
        for adding_queue in queues:
            self.append(adding_queue)
        self.is_forbidden = False
        # При создании сразу стартуем
        # self.hard_start()
        # self.put_start()
        # Поток распределения входящего сообщения по исходящим очередям
        # self._thread = threading.Thread(
        #     target=self._publisher_multicast,
        #     args=(self.__multicast_queue, *self._output_queues),
        #     daemon=True,
        # )
        # self._thread.start()

    def __len__(self):
        """Количество исходящих очередей."""
        return len(self._output_queues)

    # распределяет входящее сообщение по исходящим очередям
    # def __publisher_multicast(self, input_queue: queue.Queue, *output_queues: queue.Queue):
    #     while True:
    #         mes = input_queue.get()
    #         if isinstance(mes, MulticastClose):
    #             return
    #         for o_q in output_queues:
    #             o_q.put(mes)

    def append(
        self,
        adding_queue: t.Union[queue.Queue, QueueWrapper],
        name: t.Optional[str] = None,
        is_controlled: bool = False
    ):
        """Добавляет обернутую очередь в список отправки."""
        # Если это очередь, создаем обертку
        if not isinstance(adding_queue, QueueWrapper):
            name = name or self.__get_queue_name()
            adding_queue = QueueWrapper(name, adding_queue, is_controlled)
        # elif name != adding_queue.name:
        #     raise KeyError('Ключевые имена одного объекта должны совпадать')
        # Добавляем обернутую очередь
        self._output_queues[adding_queue.name] = adding_queue
        self.__base_events_register(adding_queue)
            # self.__base_events_register(adding_queue)
        # если имя совпадет, то очередь будет перезаписана
        # else:
        #     name = name or self.__get_queue_name()
        #     adding_queue = QueueWrapper(name, adding_queue, is_controlled)
        #     self.__base_events_register(adding_queue)
        #     self._output_queues[name] = QueueWrapper(name, adding_queue, is_controlled)

    def __base_events_register(self, adding_queue):
        """Регистрация базовых событий"""
        self.__events.on_permit += adding_queue.hard_start
        self.__events.on_break += adding_queue.hard_stop
        adding_queue.hard_start()
        if adding_queue.is_controlled:
            self.__events.on_start += adding_queue.start
            self.__events.on_stop += adding_queue.stop
            adding_queue.start()


    def __get_queue_name(self):
        """Создать следующее порядковое имя очереди."""
        # Имя (порядковый номер) нужно только для Multicast
        numbers = [
            name[len(self.__PREFIX):-len(self.__SUFFIX)]
            for name in self._output_queues.keys()
            if name.startswith(self.__PREFIX) and name.endswith(self.__SUFFIX)
        ] or ['0']
        num = max(
            map(
                lambda name: int(name) if name.isdigit() else 0,
                numbers
            )
        )
        return f'{self.__PREFIX}{num + 1}{self.__SUFFIX}'
        # self._output_queues[name] = QueueWrapper(name, input_queue)

    # TODO желательно создать механизм удаления очереди, но нужно также чистить и events; как?
    def delete(self, queue_name):
        """Удаление именованной очереди из рассылки"""
        # deleting_queue = self._output_queues[queue_name]
        # вначале удалить события из подписки
        for handler in self.__events:
            for target in handler.targets:
                if target.__self__ is self._output_queues[queue_name]:
                    handler -= target
        # теперь удалить саму очередь
        self._output_queues.pop(queue_name)

    # мягкая остановка потока отправки (остановка только контролируемых пакетов)
    # Выборка из очереди разрешена
    def put_stop(self):
        self.__events.on_stop()

    # мягкий старт (только контролируемых пакетов)
    def put_start(self):
        self.__events.on_start()

    # общий старт (просто разрешение для всех, запускаются только неконтролируемые очереди)
    def hard_start(self):
        self.__events.on_permit()
        self.is_forbidden = False

    # общая жесткая остановка всех очередей с полной их очисткой
    # Очистка очереди - выбирать из нее нечего
    def hard_stop(self):
        self.__events.on_break()
        self.is_forbidden = True

    # отправка посылки
    def put(self, item, block=True, timeout=None):
        """Положить в очередь"""
        if self.is_forbidden:
            raise MulticastSendStop('sending stopped')
        for queue_item in self._output_queues.values():
            queue_item.put(item, block, timeout)

    def get(self, queue_name: str, block=True, timeout=None):
        """Получить посылку из определенной очереди"""
        # if self.is_forbidden:
        #     raise MulticastSendStop('sending stopped')
        return self._output_queues[queue_name].get(block, timeout)

    def get_nowait(self, queue_name: str):
        """Получить посылку немедленно из определенной очереди"""
        # if self.is_forbidden:
        #     raise MulticastSendStop('sending stopped')
        return self._output_queues[queue_name].get_nowait()

    def get_instantly(self, queue_name: str):
        """Получить посылку немедленно из определенной очереди или None, если она пуста"""
        # if self.is_forbidden:
        #     raise MulticastSendStop('sending stopped')
        return self._output_queues[queue_name].get_instantly()

    # ------------------------ контроль конкретной очереди ----------------------- #
    def start(self, queue_name):
        self._output_queues[queue_name].start()

    def stop(self, queue_name):
        self._output_queues[queue_name].stop()

    def is_started(self, queue_name):
        self._output_queues[queue_name].is_started()

    def length(self, queue_name):
        """Приблизительная длина конкретной очереди"""
        return len(self._output_queues[queue_name])

    # TODO только для тестов, потом можно удалить
    def lengths(self):
        """Приблизительная длина всех очередей"""
        return {name: len(q) for name, q in self._output_queues.items() if not name.startswith(self.__PREFIX)}

    def get_events(self):
        return self.__events

    # также можно использовать для отправки, но лучше бы отменить?
    # def __call__(self, message: t.Any) -> None:
    #     self.send(message)

    # возвращает саму очередь входящих сообщения. Для чего?
    # def queue(self) -> queue.Queue:
    #     return self.__multicast_queue


if __name__ == '__main__':
    # cond = th.Condition()
    multicast = MulticastQueue(
        queue.Queue(),
        queue.Queue(),
        monitoring=queue.Queue(),
        firmware=queue.Queue(),
        testing=QueueWrapper('event_testing', queue.Queue(), _events=[th.Event()]),
        # cond=QueueWrapper('conditions', queue.Queue(), _events=[th.Event()], _conditions=[cond])
    )
    # print('init', list(q.is_permitted() for q in multicast._output_queues.values() if q.is_controlled))
    print(multicast._output_queues)
    print('-'*30)
    multicast.append(queue.Queue())
    print(multicast._output_queues)

    print('-'*60)
    # print('added queue', list(q.is_permitted() for q in multicast._output_queues.values() if q.is_controlled))
    print('начало:', multicast.lengths())
    # test положен, когда все разрешено (во все очереди)
    multicast.put('test')
    print('кладем test:', multicast.lengths())
    # print('put test', list(q.is_permitted() for q in multicast._output_queues.values() if q.is_controlled))
    import time
    time.sleep(.5)
    # запрет на put
    multicast.put_stop()
    # print('put stop', list(q.is_permitted() for q in multicast._output_queues.values() if q.is_controlled))
    # print(multicast.length('monitoring'))
    print(multicast.get_instantly('monitoring'))
    # print(multicast.length('monitoring'))
    print(multicast.get_instantly('firmware'))
    print('запретили класть и забрали 2:', multicast.lengths())
    # разрешили put firmware
    multicast.start('firmware')
    multicast.put('test 2')
    print('разрешили firmware и положили test 2', multicast.lengths())
    time.sleep(.5)
    print(multicast.get_instantly('monitoring'))
    print(multicast.get_instantly('firmware'))
    print('забрали еще 2', multicast.lengths())
    try:
        print(multicast.get_nowait('event_testing'))
    except queue.Empty:
        print('event_testing: в очереди ничего нет')

    # Проверим hard_stop
    print('-'*60)
    multicast.put_start()
    multicast.put('проверка hard_stop 1')
    multicast.put('проверка hard_stop 2')
    print('разрешили класть и положили h_test 1 и 2', multicast.lengths())
    time.sleep(.5)
    print(multicast.get_instantly('firmware'))
    print(multicast.get_instantly('monitoring'))
    print('забрали 2 в hard', multicast.lengths())
    multicast.hard_stop()
    print('hard-stop, чистим очереди')
    print(multicast.get_instantly('firmware'))
    print(multicast.get_instantly('monitoring'))
    print('хотели еще 2 после hard', multicast.lengths())

    # как определить подписку на события для конкретной очереди
    print('-'*60)
    events = (multicast.get_events())
    for handler in events:
        print('-'*30)
        print(handler.__name__)
        print(handler)
        print(handler.targets)
    print(handler.targets[0].__self__)
    # проверка удаления событий:
    print('DELETE' + '-'*60)
    multicast.delete('event_testing')
    for handler in multicast.get_events():
        print('-'*30)
        print(handler.__name__)
        print(handler)
        print(handler.targets)
    print(multicast._output_queues)

    # Проверка условия:
    # with cond:
    #     consent = cond.wait(1)
    #     if consent:
    #         print('Посылка с условием:', multicast.get_instantly('conditions'))
    #     else:
    #         print('Ничего нет')