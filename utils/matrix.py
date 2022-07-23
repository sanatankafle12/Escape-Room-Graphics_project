from __future__ import annotations
from settings import *
from utils.vector import *
from math import cos, sin
from copy import deepcopy
from math import cos, sin
from utils.vector import Vector3


class Matrix:

    def __init__(self, r: int = 4, c: int = 4):
        self.val = [[0.0 for _ in range(c)] for _ in range(r)]

    def __repr__(self) -> str:
        """repr(self)"""
        return f"matrix->{self.val}"

    @property
    def row(self) -> int:
        """The number of rows in self."""
        return len(self.val)

    @property
    def col(self) -> int:
        """The number of cols in self."""
        return len(self.val[0])

    @classmethod
    def from_vector(cls, vec: Vector3) -> Matrix:
        rv = cls(1, 4)
        rv.val = [[vec.x, vec.y, vec.z, vec.w]]
        return rv

    @classmethod
    def rotation_x(cls, angle: float) -> Matrix:
        matrix = cls()
        matrix.val = [
            [1, 0.0, 0.0, 0.0],
            [0.0, cos(angle), sin(angle), 0.0],
            [0.0, -sin(angle), cos(angle), 0.0],
            [0.0, 0.0, 0.0, 1],
        ]
        return matrix

    @classmethod
    def rotation_y(cls, angle: float) -> Matrix:
        matrix = cls()
        matrix.val = [
            [cos(angle), 0.0, -sin(angle), 0.0],
            [0.0, 1, 0.0, 0.0],
            [sin(angle), 0.0, cos(angle), 0.0],
            [0.0, 0.0, 0.0, 1],
        ]
        return matrix

    @classmethod
    def rotation_z(cls, angle: float) -> Matrix:
        matrix = cls()
        matrix.val = [
            [cos(angle), sin(angle), 0.0, 0.0],
            [-sin(angle), cos(angle), 0.0, 0.0],
            [0.0, 0.0, 1, 0.0],
            [0.0, 0.0, 0.0, 1],
        ]
        return matrix

    @classmethod
    def scaling(cls, scale: float) -> Matrix:
        matrix = cls()
        matrix.val = [
            [scale, 0.0, 0.0, 0.0],
            [0.0, scale, 0.0, 0.0],
            [0.0, 0.0, scale, 0.0],
            [0.0, 0.0, 0.0, 1],
        ]
        return matrix

    @classmethod
    def identity(cls, size: int = 4) -> Matrix:
        matrix = cls()
        matrix.val = [
            [1.0 if i == j else 0.0 for j in range(size)] for i in range(size)
        ]
        return matrix

    @classmethod
    def translate(cls, position: Vector3) -> Matrix:
        matrix = cls()
        matrix.val = [
            [1, 0.0, 0.0, position.x],
            [0.0, 1, 0.0, position.y],
            [0.0, 0.0, 1, position.z],
            [0.0, 0.0, 0.0, 1],
        ]
        return matrix

    def __matmul__(self, other: Matrix) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented

        if self.col != other.row:
            raise ValueError(
                f"{(self.row, self.col)}, {(other.row, other.col)}"
            )

        rv = Matrix(self.row, other.col)
        for x in range(self.row):
            for y in range(other.col):
                val = sum(self.val[x][z] * other.val[z][y] for z in range(self.col))
                rv.val[x][y] = round(val, 5)

        return rv

    def transpose(self) -> Matrix:
        rv = Matrix(self.row, self.col)
        for x in range(self.row):
            for y in range(self.col):
                rv.val[x][y] = self.val[y][x]
        return rv

    def submatrix(self, row: int, col: int) -> Matrix:
        temp = deepcopy(self)
        del temp.val[row]
        for i in range(self.row):
            del temp.val[i][col]

        return temp

    def det(self) -> float:
        if self.row != self.col:
            raise ValueError("Matrix determinant only defined for square matrices.")

        if self.row == 2:
            return self.val[0][0] * self.val[1][1] - self.val[0][1] * self.val[1][0]

        d = 0.0
        for j in range(self.col):
            c = self.cofactor(0, j)
            d += c * self.val[0][j]
        return d

    def updateInfo(self):
        self.row = len(self.val)
        self.col = len(self.val[0])

    def transpose(self):
        temp = [[0 for i in range(self.col)] for j in range(self.row)]
        for x in range(self.row):
            for y in range(self.col):
                temp[x][y] = self.val[y][x]
        self.val = temp

    def __repr__(self):
        ## DEBUG
        return f'matrix->{self.val}'


def multiplyMatrix(m1, m2):
    m = Matrix(m1.row, m2.col)

    if m1.col != m2.row:
        print("we can't this two matricies")
        return None

    for x in range(m1.row):
        for y in range(m2.col):
            sum = 0
            for z in range(m1.col):
                sum += m1.val[x][z] * m2.val[z][y]
            m.val[x][y] = round(sum, 5)

    return m

def multiplyMatrixVector(vec, mat):
    temp = Matrix(1, 4)
    temp.val = vec.toMatrix()
    m = multiplyMatrix(temp, mat)
    v = toVector3(m)
    if m.val[0][3] != 0:
        v = v / m.val[0][3]
    return v

def QuickInverse(m):
    matrix = Matrix()
    matrix.val[0][0], matrix.val[0][1], matrix.val[0][2], matrix.val[0][3] = m.val[0][0], m.val[1][0], m.val[2][0], 0.0
    matrix.val[1][0], matrix.val[1][1], matrix.val[1][2], matrix.val[1][3] = m.val[0][1], m.val[1][1], m.val[2][1], 0.0
    matrix.val[2][0], matrix.val[2][1], matrix.val[2][2], matrix.val[2][3] = m.val[0][2], m.val[1][2], m.val[2][2], 0.0
    matrix.val[3][0] = -(m.val[3][0] * matrix.val[0][0] + m.val[3][1] * matrix.val[1][0] + m.val[3][2] * matrix.val[2][0])
    matrix.val[3][1] = -(m.val[3][0] * matrix.val[0][1] + m.val[3][1] * matrix.val[1][1] + m.val[3][2] * matrix.val[2][1])
    matrix.val[3][2] = -(m.val[3][0] * matrix.val[0][2] + m.val[3][1] * matrix.val[1][2] + m.val[3][2] * matrix.val[2][2])
    matrix.val[3][3] = 1.0
    return matrix


