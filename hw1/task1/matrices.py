from vectors import *
import copy


class Matrix:
    content: List[Vector]

    def __init__(self, first: Vector, *args: Vector):
        if len(first) == 0:
            raise TypeError("Matrix can't be created from empty vectors")
        if not all(len(first) == len(vector) for vector in args):
            raise TypeError("Rows must be the same length")
        self.content = [first, *args]

    def __str__(self):
        return str(self.content)

    def __add__(self, other):
        if self.get_dimensions() != other.get_dimensions():
            raise TypeError("Matrices must have the same dimensions")
        return Matrix(*[get_vector_sum(x, y) for x, y in zip(self.content, other.content)])

    def get_dimensions(self):
        return {"columns": len(self.content[0]), "rows": len(self.content)}

    def __mul__(self, other):
        if self.get_dimensions()["rows"] != other.get_dimensions()["columns"]:
            raise TypeError("Matrices can't be multiplied")
        return Matrix(*[[scalar(row, column) for column in transpose(other).content] for row in self.content])


def transpose(matrix: Matrix, in_place=False) -> Matrix:
    transposed = [list(t) for t in zip(*matrix.content)]
    if in_place:
        matrix.content = transposed
        transposed = copy.deepcopy(transposed)
    return Matrix(*transposed)