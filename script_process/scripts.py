class Script:
    def __init__(self, name: str, attack=False):
        self.name = name
        self.path = self._init_path(name, attack)

    def _init_path(self, name, attack=False) -> str:
        attack_string = 'attacks/' if attack else ''
        return f'scripts/{attack_string}/{name}.gml'


INIT = Script('init')
