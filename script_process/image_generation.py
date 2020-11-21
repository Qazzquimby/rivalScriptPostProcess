import abc
import os
import sys

from PIL import Image, ImageDraw


class Shape(abc.ABC):
    name = NotImplemented

    def __init__(self, width: int, height: int, color: str = None):
        self.width = width
        self.height = height
        self._color = color

    def save(self, path: str):
        image = self._make_image()
        self._draw_on_image(image)
        image.save(f'{path}{self.file_name}')

    @property
    def file_name(self):
        color_str = self._get_color_file_name_part()
        return f'{color_str}{self.name}_{self.width}_{self.height}.png'

    @classmethod
    def from_file_name(cls, file_name):
        try:
            file_name = file_name.split('.png')[0]
            name, kwargs = cls._unpack_file_name(file_name)
            if name != cls.name:
                return None
            return cls(**kwargs)
        except (ValueError, IndexError, TypeError):
            return None

    @classmethod
    def _unpack_file_name(cls, file_name):
        *color, name, width, height = file_name.split('_')
        color = color[0] if color else None
        kwargs = {
            "color": color,
            "width": int(width),
            "height": int(height)
        }
        return name, kwargs

    def _get_color_file_name_part(self):
        if self._color is None:
            color_str = ''
        else:
            color_str = f'{self.color}_'
        return color_str

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
    name = "ellipse"

    def __init__(self, width: int, height: int, color: str = None):
        super().__init__(width=width, height=height, color=color)

    def _draw_on_canvas(self, canvas: ImageDraw):
        canvas.ellipse((0, 0, self.width - 1, self.height - 1), fill=self.color)


class Circle(Ellipse):
    name = "circle"

    def __init__(self, diameter: int, color: str = None):
        super().__init__(width=diameter, height=diameter, color=color)

    @property
    def file_name(self):
        color_str = self._get_color_file_name_part()
        return f'{color_str}{self.name}_{self.width}.png'

    @classmethod
    def _unpack_file_name(cls, file_name):
        *color, name, diameter = file_name.split('_')
        color = color[0] if color else None
        kwargs = {
            "color": color,
            "diameter": int(diameter),
        }
        return name, kwargs


class Rectangle(Shape):
    name = "rect"

    def __init__(self, width: int, height: int, color: str = None):
        super().__init__(width=width, height=height, color=color)

    def _draw_on_canvas(self, canvas: ImageDraw):
        canvas.rectangle((0, 0, self.width - 1, self.height - 1), fill=self.color)


def make_sprite_for_file_name(sprite_path: str, file_name: str):
    """Generate a sprite matching the file name.

    Format
    <color_>circle_diameter
    <color_>ellipse_width_height
    <color_>rect_width_height
    """

    for shape_type in (Circle, Ellipse, Rectangle):
        shape = shape_type.from_file_name(file_name)
        if shape is not None:
            path = f'{sprite_path}/{file_name}'
            if not os.path.exists(path):
                shape.save(sprite_path)


if __name__ == '__main__':
    root_path = sys.argv[1]
    sprite_path = f'{root_path}/sprites/'

    make_sprite_for_file_name(sprite_path, "ellipse_30_30.png")
    make_sprite_for_file_name(sprite_path, "red_ellipse_30_30.png")
    make_sprite_for_file_name(sprite_path, "circle_22.png")
    make_sprite_for_file_name(sprite_path, "blue_circle_30.png")
    make_sprite_for_file_name(sprite_path, "rect_34_36.png")
    make_sprite_for_file_name(sprite_path, "orange_rect_3_5.png")

    Ellipse(width=45, height=45, color="red").save(sprite_path)
    Ellipse(20, 30).save(sprite_path)
    Circle(50, color="blue").save(sprite_path)
    Rectangle(80, 50, "orange").save(sprite_path)
