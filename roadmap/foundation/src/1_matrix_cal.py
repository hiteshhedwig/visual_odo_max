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
    
    def sanity_check(self, other, ops):
        if ops in ["+", "-"]:
            if other.get_shape() == self.get_shape():
                print(f"matrix check okay for {ops}", self.get_shape())
            else:
                raise ValueError(f"matrix check failed for {ops} - {self.get_shape()} != {other.get_shape()}")
        
        if ops in ["*"]:
            if self.cols == other.rows :
                print(f"matrix check okay for {ops}")
            else :
                raise ValueError(f"matrix check failed for operation : {ops} shapes : {self.get_shape()} * {other.get_shape()}. ERROR : {self.cols} != {other.rows}")

    def __add__(self, other):
        self.sanity_check(other,"+")

        added_matrix = other.get_matrix() + self.get_matrix()
        final_matrix = MatrixOperations(self.rows, self.cols)
        final_matrix.set_matrix(added_matrix)
        return final_matrix
    
    def __sub__(self, other):
        self.sanity_check(other, "-")
                      
        added_matrix = self.get_matrix() - other.get_matrix() 
        final_matrix = MatrixOperations(self.rows, self.cols)
        final_matrix.set_matrix(added_matrix)
        return final_matrix
    
    def __mul__(self, other):
        self.sanity_check(other, "*")

        added_matrix = self.get_matrix() @ other.get_matrix() 
        final_matrix = MatrixOperations(self.rows, self.cols)
        final_matrix.set_matrix(added_matrix)
        return final_matrix


    
if __name__ == '__main__':
    mat_1 = MatrixOperations(2,3)
    print("MAT 1 " , mat_1.get_matrix())
    mat_2 = MatrixOperations(3,2)
    print("MAT 2 ", mat_2.get_matrix())

    mat_3 = mat_1 * mat_2   
    print(mat_3.get_matrix())