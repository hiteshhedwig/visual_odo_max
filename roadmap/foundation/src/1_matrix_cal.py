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
        self.matrix = np.random.rand(rows, cols).astype(np.float32)
        self.rows = rows
        self.cols = cols

    def get_matrix(self):
        """Return the matrix"""
        return self.matrix
    
    def get_shape(self):
        return self.matrix.shape
    
    def set_matrix(self,matrix):
        self.matrix = matrix
        return self.matrix
    
    def __add__(self, other):
        # assert other.get_shape() == self.get_matrix()
        if other.get_shape() == self.get_shape():
            print("matrix check okay ", self.get_shape())
        else:
            raise ValueError(f"matrix check failed - {self.get_shape()} != {other.get_shape()}")
                              
        added_matrix = other.get_matrix() + self.get_matrix()
        final_matrix = MatrixOperations(self.rows, self.cols)
        final_matrix.set_matrix(added_matrix)
        return final_matrix

    
if __name__ == '__main__':
    mat_1 = MatrixOperations(4,3)
    print("MAT 1 " , mat_1.get_matrix())
    mat_2 = MatrixOperations(4,3)
    print("MAT 2 ", mat_2.get_matrix())

    mat_3 = mat_1 + mat_2   
    print(mat_3.get_matrix())