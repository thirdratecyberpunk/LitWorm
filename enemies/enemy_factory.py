import random

class EnemyFactory:
    """
    Class responsible for generating enemy objects
    """
    def __init__(self):
        self._enemy_types= {}

    def register_enemy_type(self, key, enemy_type):
        self._enemy_types[key] = enemy_type

    def create(self, key=None):
        """
        Returns an instance of an enemy object
        If no key is given, returns a random enemy
        """
        if (key == None):
            key = random.choice(list(self._enemy_types.keys()))
        enemy_type = self._enemy_types.get(key)
        if not enemy_type:
            raise ValueError(key)
        return enemy_type()