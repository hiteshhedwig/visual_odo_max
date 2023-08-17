import numpy as np

# 1. Linear Algebra:
# Project 1: Matrix Calculator
#     Objective: Implement a calculator that can perform operations like addition, subtraction, multiplication, and inversion of matrices.
#     Skills Gained: Familiarity with matrix operations, which are fundamental for transformations in VO.


class MatrixOperations(object):
    """
    matrix operations
    """
    def __init__(self, rows, cols):
        self.matrix = np.zeros((rows,cols), dtype=np.float32)

    def get_matrix(self):
        """Return the matrix"""
        return self.matrix
    
    def __add__(self, other):
        pass
    

if __name__ == '__main__':
    mo = MatrixOperations(4,3)
    print(mo.get_matrix())