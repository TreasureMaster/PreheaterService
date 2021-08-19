from .maincommands import Command


class DeviceConnect(Command):
    __commands = [
        'Подключить',
        'Отключить'
    ]

    def __init__(self, itself):
        self.itself = itself
        self.current_command = 0

    def execute(self):
        # print('Device connected')
        self.current_command = not self.current_command
        # print(self.itself.text)
        self.itself.config(
            text = DeviceConnect.__commands[self.current_command]
        )