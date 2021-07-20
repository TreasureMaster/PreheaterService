import pytest
import accessify

from modulehelper import ModuleHelper


def test_create_modulehelper():
    """Невозможно напрямую создать класс ModuleHelper, так как __init__
    объявлен как приватный."""
    with pytest.raises(accessify.errors.InaccessibleDueToItsProtectionLevelException) as excinfo:
        helper = ModuleHelper()
    exception_msg = excinfo.value.args[0]
    assert exception_msg == 'ModuleHelper.__init__() is inaccessible due to its protection level'

def test_instance_modulehelper():
    """Метод instance должен указывать на один и тот же объект (синглтон в пределах приложения)."""
    helper1 = ModuleHelper.instance()
    assert isinstance(helper1, ModuleHelper)
    helper2 = ModuleHelper.instance()
    assert helper2 is helper1