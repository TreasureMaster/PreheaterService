import os

from Cryptodome.Cipher import AES
# from Cryptodome.Random import get_random_bytes

from applogger import AppLogger
from registry import ConfigRegistry


class MismatchedKeys(Exception):
    pass

def encode_xml():
    # TODO пока не реализовано
    key = b'fg(GG4_+=|~?/{;}'
    cipher = AES.new(key, AES.MODE_EAX)

    with open('config.xml', 'r', encoding='utf-8') as fd:
        data = fd.read()

    ciphertext, tag = cipher.encrypt_and_digest(data.encode())

    file_out = open('config.bin', 'wb')
    [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
    file_out.close()


def decode_xml(raw_data, fnm):
    """Пробует декодировать данные config.bin в xml"""
    # fnm - только для вывод ошибки
    # try:
    #     file_in = open(path, 'rb')
    # except FileNotFoundError:
    #     AppLogger.instance().error("Файл '{}' не найден.".format(path))
    #     return

    for key in ConfigRegistry.instance().getManagerConfig().getMainKeys():
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