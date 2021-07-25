import os

from typing import Iterable

from Cryptodome.Cipher import AES
# from Cryptodome.Random import get_random_bytes

from applogger import AppLogger
# from registry import ConfigRegistry, AppRegistry


class MismatchedKeys(Exception):
    """Ошибка несовпадения ключей."""
    pass

def encode_xml(key: bytes, xml: bytes, cfgfilename: str) -> None:
    """Кодирование данных XML и запись в файл.

    key - действующий ключ менеджера.
    xml - подготовленный для шифрования текст XML (должен быть тип bytes).
    cfgfilename - имя и путь файла для сохранения зашифрованного файла конфигурации (сейчас - config.bin).
    """
    cipher = AES.new(key, AES.MODE_EAX)

    ciphertext, tag = cipher.encrypt_and_digest(xml)

    file_out = open(cfgfilename, 'wb')
    [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
    file_out.close()


def decode_xml(raw_data: bytes, fnm: str, keys: Iterable[bytes]) -> str:
    """Пробует декодировать данные config.bin в xml.

    raw_data - двоичные данные config.bin файла
    fnm - имя файла, который расшифровывается.
    """
    # fnm - только для вывод ошибки
    # try:
    #     file_in = open(path, 'rb')
    # except FileNotFoundError:
    #     AppLogger.instance().error("Файл '{}' не найден.".format(path))
    #     return

    # for key in ConfigRegistry.instance().getManagerConfig().getAllKeys():
    for key in keys:
        try:
            # nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
            nonce, tag, ciphertext = raw_data[:16], raw_data[16:32], raw_data[32:]
            cipher = AES.new(key, AES.MODE_EAX, nonce)
            data = cipher.decrypt_and_verify(ciphertext, tag)
        except:
            pass
        else:
            # Ключ подошел
            break
    else:
        # выход, если ничего не удалось расшифровать (цикл закончился)
        AppLogger.instance().error("Невозможно расшифровать файл '{}'. Ключ не найден.".format(os.path.basename(fnm)))
        raise MismatchedKeys('Mismatched key or other decryption error')

    try:
        data = data.decode('utf-8')
    except UnicodeDecodeError:
        AppLogger.instance().error('Неизвестная кодировка файла.')
        raise

    return data