import math

from typing import List

Vector = List[float]


def scalar(first: Vector, second: Vector) -> float:
    if len(first) != len(second):
        raise TypeError("Vectors must be the same length")
    return sum([x * y for x, y in zip(first, second)])


def module(vector: Vector) -> float:
    return math.sqrt(scalar(vector, vector))


def angle(first: Vector, second: Vector) -> float:
    if len(first) != len(second):
        raise TypeError("Vectors must be the same length")
    return math.acos(scalar(first, second) / (module(first) * module(second)))


def get_vector_sum(first: Vector, *args: Vector) -> Vector:
    if not all([len(first) == len(v) for v in args]):
        raise TypeError("Vectors must be the same length")
    return [sum(v) for v in list(zip(first, *args))]
