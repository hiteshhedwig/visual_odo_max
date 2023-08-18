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
        return self
    
    def determinant(self, matrix):
        if len(matrix) != len(matrix[0]):
            raise ValueError("Matrix must be square.")
            
        # Base case for 2x2 matrix
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        
        det = 0
        for j in range(len(matrix[0])):
            # Get the submatrix by removing the first row and j-th column
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            
            # Add or subtract the term, alternatingly
            det += ((-1) ** j) * matrix[0][j] * self.determinant(submatrix)
        
        return det
    
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

        if ops is ["inverse"] :
            if len(self.matrix) != len(self.matrix[0]):
                raise ValueError("Matrix must be square.")
            
            if self.determinant(self.matrix) == 0:
                raise ValueError("Determinant value of the matrix is zero.")
            

    def __add__(self, other):
        self.sanity_check(other,"+")

        added_matrix = other.get_matrix() + self.get_matrix()

        return MatrixOperations(self.rows, self.cols).set_matrix(added_matrix)
    
    def __sub__(self, other):
        self.sanity_check(other, "-")
                      
        sub_matrix = self.get_matrix() - other.get_matrix() 

        return MatrixOperations(self.rows, self.cols).set_matrix(sub_matrix)
    
    def __mul__(self, other):
        self.sanity_check(other, "*")

        mul_matrix = self.get_matrix() @ other.get_matrix() 

        return MatrixOperations(self.rows, self.cols).set_matrix(mul_matrix)

    def get_inverse(self):
        # The code you provided is implementing the method `get_inverse()` in the
        # `MatrixOperations` class. This method calculates the inverse of a matrix using the
        # Gauss-Jordan elimination algorithm.
        self.sanity_check(self.matrix,"inverse")
        
        A = self.get_matrix()
        n = len(A)
        # Create an augmented matrix [A|I]
        augmented = [list(row) + [0] * n for row in A]
        for i in range(n):
            augmented[i][n + i] = 1

        # Use Gauss-Jordan elimination
        for i in range(n):
            # Make diagonal contain all ones
            diag = augmented[i][i]
            for j in range(2 * n):
                augmented[i][j] /= diag

            # Make other rows contain zeros
            for k in range(n):
                if k != i:
                    factor = -augmented[k][i]
                    for j in range(2 * n):
                        augmented[k][j] += factor * augmented[i][j]

        # Extract the inverse matrix
        inverse = [row[n:] for row in augmented]

        return inverse
    
if __name__ == '__main__':
    mat_1 = MatrixOperations(2,3)
    print("MAT 1 " , mat_1.get_matrix())
    mat_2 = MatrixOperations(3,2)
    print("MAT 2 ", mat_2.get_matrix())

    mat_3 = mat_1 * mat_2   
    print(mat_3.get_matrix())

    print("----")
    print(mat_3.get_inverse())