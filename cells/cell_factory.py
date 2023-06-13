import random
from cells.cell import Cell

class CellFactory:
    """
    Class responsible for generating cell objects
    TODO: create set of possible cell types 
    and separate this from cell values
    """
    def __init__(self):
        self._cell_types= {}

    def register_cell_type(self, key, value):
        self._cell_types[key] = value

    def create(self, x, y, key=None):
        """
        Returns an instance of an cell object
        If no key is given, returns a random cell
        """
        if (key == None):
            key = random.choice(list(self._cell_types.keys()))
        cell = Cell(x,y, key, self._cell_types[key])
        if not cell:
            raise ValueError(key)
        return cell