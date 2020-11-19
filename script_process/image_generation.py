import abc
import sys

from PIL import Image, ImageDraw


class Shape(abc.ABC):
    def __init__(self, width: int, height: int, name: str, color: str = None):
        self.width = width
        self.height = height
        self._color = color
        self.name = name

    def save(self, path: str):
        image = self._make_image()
        self._draw_on_image(image)
        image.save(f'{path}{self.file_name}')

    @property
    def file_name(self):
        if self._color is None:
            color_str = ''
        else:
            color_str = f'{self.color}_'

        return f'{color_str}{self.name}_{self.width}_{self.height}.png'

    @property
    def color(self):
        if self._color is None:
            return "white"
        else:
            return self._color

    def _make_image(self) -> Image:
        image = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        return image

    def _draw_on_image(self, image: Image):
        canvas = ImageDraw.Draw(image)
        self._draw_on_canvas(canvas)

    def _draw_on_canvas(self, canvas: ImageDraw):
        raise NotImplementedError


class Ellipse(Shape):
    def __init__(self, width: int, height: int, color: str = None):
        super().__init__(width=width, height=height, color=color, name="ellipse")

    def _draw_on_canvas(self, canvas: ImageDraw):
        canvas.ellipse((0, 0, self.width - 1, self.height - 1), fill=self.color)


class Circle(Ellipse):
    def __init__(self, diameter: int, color: str = None):
        super().__init__(width=diameter, height=diameter, color=color)
        self.name = "circle"


class Rectangle(Shape):
    def __init__(self, width: int, height: int, color: str = None):
        super().__init__(width=width, height=height, color=color, name="rect")

    def _draw_on_canvas(self, canvas: ImageDraw):
        canvas.rectangle((0, 0, self.width - 1, self.height - 1), fill=self.color)


if __name__ == '__main__':
    root_path = sys.argv[1]
    sprite_path = f'{root_path}/sprites/'

    Ellipse(width=45, height=45, color="red").save(sprite_path)
    Ellipse(20, 30).save(sprite_path)
    Circle(50, color="blue").save(sprite_path)
    Rectangle(80, 50, "orange").save(sprite_path)
