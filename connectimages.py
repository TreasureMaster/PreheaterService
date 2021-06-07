from tkinter import *

from PIL import Image, ImageTk


class ResizableImage(Frame):
    def __init__(self, master, *args, image=None):
        Frame.__init__(self, master, *args)
        self.image = image and Image.open(f"tasks/{image}.png")
        if self.image:
            self._make_image()

    def _make_image(self):
        """Создание картинки."""
        self.img_copy= self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self, event):
        """Событие изменения размера картинки."""
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


class IndicatorImage(Frame):
    RATIO = 24
    def __init__(self, master, *args, image=None):
        Frame.__init__(self, master, *args)
        self.image = image and Image.open(f"tasks/{image}.png")
        if self.image:
            self._make_image()

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
        reduction = round(height / self.RATIO)
        new_width = round(width / reduction)
        new_height = round(height / reduction)

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


if __name__ == '__main__':
    root = Tk()
    root.title("Title")
    root.geometry("600x600")
    root.configure(background="black")

    # e = ResizableImage(root, image='yes2')
    # print(e.image)
    # e.pack(fill=BOTH, expand=YES)

    ind = IndicatorImage(root, image='yes2')
    ind.pack(fill=BOTH, expand=YES)

    # ind.size_image()


    root.mainloop()