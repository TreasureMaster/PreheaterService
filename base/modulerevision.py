from __future__ import annotations

import time

from .moduleconfig import ModuleConfig
from registry import ModListRegistry


class ModuleRevision:
    """Класс, описывающий версию модуля."""

    # TODO нужна ли проверка версий всех модулей из текущего списка модулей,
    # чтобы избежать совпадающих версий ???
    def __init__(self, cfg: ModuleConfig) -> None:
        self.__config = cfg

    @property
    def name(self):
        return self.__config.getProperty('name')

    @property
    def major(self):
        return int(self.__config.getProperty('majorrevision'))

    @property
    def minor(self):
        return int(self.__config.getProperty('minorrevision'))

    @property
    def editrev(self):
        return int(self.__config.getProperty('editrevision'))

    @property
    def lastupd(self):
        return int(self.__config.getProperty('lastupdated'))

    @property
    def baserevision(self):
        return self.getBaseRevision()

    @property
    def edition(self):
        return self.getEdition()

    @property
    def revision(self):
        return self.getRevision()

    def getBaseRevision(self) -> str:
        return '{}.{}'.format(
            self.__config.getProperty('majorrevision'),
            self.__config.getProperty('minorrevision')
        )

    def getEdition(self) -> str:
        return '{}-{}'.format(
            self.__config.getProperty('editrevision'),
            time.strftime('%d%m%y', time.localtime(self.__config.getProperty('lastupdated')))
        )

    def getRevision(self) -> str:
        return '{}.{}'.format(
            self.getBaseRevision(),
            self.getEdition()
        )

    def __eq__(self, other: ModuleRevision) -> bool:
        """Проверка равенства версий двух модулей."""
        return (
            (self.name == other.name) and
            (self.major == other.major) and
            (self.minor == other.minor) and
            (self.editrev == other.editrev) and
            (self.lastupd == other.lastupd)
        )

    def getMaxEdition(self):
        """Получение максимального числа редакции.
        
        name, major, minor должны быть равны.
        editrev при равенстве предыдущих должна быть больше всех.
        """
        return max(modrev.editrev for modrev in ModListRegistry.instance().getRevisions()
                   if modrev.name == self.name and modrev.major == self.major and modrev.minor == self.minor)

    def increment(self) -> None:
        """Увеличение редакции модуля на 1 с установкой даты редактирования."""
        self.__config.setProperty('editrevision', max(self.editrev, self.getMaxEdition()) + 1)
        self.__config.setProperty('lastupdated', int(time.time()))