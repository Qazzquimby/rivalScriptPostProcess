import abc
import re
import typing as t


class Asset(abc.ABC):
    def __init__(self, asset_string: str):
        self.asset_string = asset_string

    @classmethod
    def get_from_text(cls, text) -> t.List:
        raise NotImplementedError

    def supply(self) -> None:
        raise NotImplementedError

    def __eq__(self, other):
        return self.asset_string == other.asset_string

    def __hash__(self):
        return hash(self.__class__.__name__ + self.asset_string)


class Sprite(Asset):
    _pattern = r"(?<=sprite_get\([\"'])(.+?)(?=['\"]\))"

    @classmethod
    def get_from_text(cls, text) -> t.List['Sprite']:
        asset_strings = list(re.findall(pattern=cls._pattern, string=text))
        return [Sprite(string) for string in asset_strings]

    def supply(self):
        # Generate sprite
        # save if missing
        print('debug')

ASSET_TYPES = [Sprite]
