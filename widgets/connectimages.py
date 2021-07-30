from tkinter import *

from PIL import Image, ImageTk


class ResizableImage(Frame):
    """Картинка растягивается вместе с окном.

    parent - виджет, к которому прикрепляется фрейм картинки.
    link - путь к файлу картинки.
    ratio - коэффициент изменения картинки.
    """
    def __init__(self, parent, link='images/image.jpg', cnf={}, **kwargs):
        super().__init__(parent, cnf, **kwargs)
        self.parent = parent
        self.image = Image.open(link)
        self._make_image()

    def _make_image(self):
        """Создание картинки."""
        self.img_copy= self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)

        self._how_resize()

    def _how_resize(self):
        """Как будет изменяться картинка - событие."""
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self, event=None):
        """Изменение размера картинки."""
        self.image = self.img_copy.resize(
            self._get_new_sizes(event)
        )

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)

    def _get_new_sizes(self, event):
        """Размер картинки берется из события изменения размеров окна."""
        return (event.width, event.height)


class OnceResizedImage(ResizableImage):
    """Создает картинку определенного размера, пропорционально отношению (RATIO)."""

    def __init__(self, parent, link='images/image.jpg', ratio=1, cnf={}, **kwargs):
        self.ratio = ratio
        super().__init__(parent, link, cnf, **kwargs)

    def _how_resize(self):
        """Как будет изменяться картинка - однократное изменение."""
        self._resize_image()

    def _get_new_sizes(self, event):
        """Размер картинки вычисляется с помощью заданного коэффициента.

        event - используется для совместимости метода с базовым классом.
        """
        width, height = self.image.size
        reduction = round(height / self.ratio)
        return (round(width / reduction), round(height / reduction))


class HeightResizedImage(ResizableImage):
    """Создает картинку заданной высотой."""

    def __init__(self, parent, link='images/image.jpg', maxheight=1, cnf={}, **kwargs):
        self.maxheight = maxheight
        super().__init__(parent, link, cnf, **kwargs)

    def _get_new_sizes(self, event):
        """Размер картинки вычисляется с помощью заданного коэффициента.

        event - используется для совместимости метода с базовым классом.
        """
        width, height = self.image.size
        reduction = round(height / self.maxheight)
        return (round(width / reduction), round(height / reduction))


class OnceByHeightResizedImage(OnceResizedImage):
    """Создает картинку по размеру уже размещенного родительского виджета."""

    def _get_new_sizes(self, event):
        """Размер картинки вычисляется с помощью заданного коэффициента.

        event - используется для совместимости метода с базовым классом.
        """
        print(self.parent.winfo_reqheight())
        width, height = self.image.size
        reduction = round(height / self.parent.winfo_reqheight() * self.ratio)
        return (round(width / reduction), round(height / reduction))


class OnceByHeightMappedImage(OnceByHeightResizedImage):
    """Создает картинку по размеру еще НЕ размещенного родительского виджета."""

    # WARNING не работает правильно.
    def __init__(self, parent, link='images/image.jpg', ratio=1, lastadded=None, cnf={}, **kwargs):
        self.last_added = lastadded
        super().__init__(parent, link, ratio, cnf, **kwargs)

    def _how_resize(self):
        self.last_added.bind('<Map>', self._resize_image)


class ModuleImage(Frame):
    __MAX_HEIGHT = 250
    def __init__(self, master, image=None, maxheight=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.maxheight = maxheight or ModuleImage.__MAX_HEIGHT
        self.image = image and Image.open(image)
        if self.image:
            self._make_image()

    def updateImage(self, image=None):
        if self.image:
            self.background.destroy()
        self.image = image and Image.open(image)
        if self.image:
            self._make_image()

    def clearImage(self):
        # ERROR: если еще не был показан модуль (соответственно нет картинки)
        if hasattr(self, 'background'):
            self.background.destroy()
        # self.update()

    def _make_image(self):
        """Создание картинки."""
        self.img_copy= self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self._resize_image()
        # self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self):
        """Событие изменения размера картинки."""
        width, height = self.image.size
        reduction = (height / self.maxheight)
        new_width = round(width / reduction)
        new_height = round(height / reduction)

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


if __name__ == '__main__':
    root = Tk()
    root.title("Title")
    root.geometry("700x700")
    root.configure(background="black")

    # Тест изменяемого в реальном времени размера в зависимости от размера родительского фрейма
    # e = ResizableImage(root)
    # print(e.image)
    # e.pack(fill=BOTH, expand=YES)

    # Тест однократного изменяемого размера в зависимости от заданного коэффициента изменения
    # ind = OnceResizedImage(root, link='tasks/yes2.png', ratio=24)

    # ind = ModuleImage(root, image='module/data/image.jpg')
    # ind = ModuleImage(root, image='data/binar5s.jpg')

    # Тест однократно изменяемого размера картинки в зависимости от размеров родительского фрейма
    # frm = Frame(root)
    # frm.pack(expand=NO)
    # frm.config(width=150, height=150)
    # frm.config(
    #     borderwidth=2,
    #     highlightthickness=2,
    #     highlightbackground='red',
    #     # relief='raised'
    # )
    # ind = OnceByHeightResizedImage(frm, ratio=1)

    # То же на кнопке (не получается, нужно размещать другим способом - параметр image)
    # btn = Button(root, command=lambda: None)
    # btn.pack(expand=NO)
    # btn.config(width=150, height=150)
    # btn.config(
    #     borderwidth=2,
    #     highlightthickness=2,
    #     highlightbackground='red',
    #     relief='flat'
    # )
    # ind = OnceByHeightResizedImage(btn, ratio=2)
    ind = HeightResizedImage(root, maxheight=190)
    ind.config(
        borderwidth=2,
        highlightthickness=2,
        highlightbackground='red'
    )
    ind.pack(expand=NO)

    # ind.size_image()


    root.mainloop()