import numpy as np
from numpy import matmul
from numpy import linalg
from numpy.matrixlib.defmatrix import matrix

# Функция для нахождения
def transpose_matrix(matrix):
    matrix=np.array(matrix)
    return np.round(matrix.T,4)

def compose_matrix(matrix_a, matrix_b):
    matrix_a=np.array(matrix_a)
    matrix_b = np.array(matrix_b)
    return np.round(matrix_a + matrix_b,4)

def subtract_matrix(matrix_a, matrix_b):
    matrix_a = np.array(matrix_a)
    matrix_b = np.array(matrix_b)
    return np.round(matrix_a - matrix_b,4)

def check_same_size(matrix_a, matrix_b):
    matrix_a=np.array(matrix_a)
    matrix_b = np.array(matrix_b)
    rows_a, cols_a = matrix_a.shape
    rows_b, cols_b = matrix_b.shape
    if cols_a == cols_b and rows_a == rows_b:
        return True
    else:
        return False

def check_multiply_sizes(matrix_a, matrix_b):
    matrix_a = np.array(matrix_a)
    matrix_b = np.array(matrix_b)
    cols_a = matrix_a.shape[1]
    rows_b = matrix_b.shape[0]
    if cols_a == rows_b:
        return True
    else:
        return False

def check_square(matrix):
    matrix=np.array(matrix)
    size = matrix.shape
    if size[0] == size[1]:
        return True
    else:
        return False

def multiply_matrix(matrix_a, matrix_b):
    matrix_a=np.array(matrix_a)
    matrix_b = np.array(matrix_b)
    return np.round(matmul(matrix_a, matrix_b),4)

def multiply_num(n, matrix):
    matrix=np.array(matrix)
    return np.round(n*matrix,4)

def exponentiation_matrix(n, matrix):
    matrix=np.array(matrix)
    if check_square(matrix):
        return np.round(np.linalg.matrix_power(matrix, n),4)

def solution_SLAU(matrix, matrix_b):
    matrix_1 = np.linalg.inv(matrix)
    matrix_x = matmul(matrix_1, matrix_b)
    return list(matrix_x)

def determinant(matrix):
    matrix = np.array(matrix)
    return np.round(np.linalg.det(matrix),4)

def matrix_rang(matrix):
    matrix=np.array(matrix)
    return np.round(np.linalg.matrix_rank(matrix),4)

def matrix_inv(matrix):
    matrix=np.array(matrix)
    return np.round(np.linalg.inv(matrix),4)
def rang_check(A,B):
    A=np.array(A)
    B=np.array(B)
    B=B.reshape(-1,1)
    res=np.hstack((A,B))
    if matrix_rang(res)!=matrix_rang(A):
        return True
    else:
        return False


