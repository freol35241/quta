'''
Tests for constraint module
'''
import numpy as np
import pytest
import quota.constraints as cons

def test_concatenation():
    '''
    Test for checking that concatenation of sets 
    of linear constraints works.
    '''
    C_0 = np.eye(3)
    b_0 = np.zeros(3)
    n_0 = 0

    C_1 = np.eye(3)*4
    b_1 = np.ones(3)*4
    n_1 = 1

    C_out, b_out, n_out = cons.concatenate_constraints((C_0, b_0, n_0),
                                                       (C_1, b_1, n_1))

    assert C_out.shape[0] == C_0.shape[0] + C_1.shape[0]
    assert C_out.shape[1] == C_0.shape[1] == C_1.shape[1]
    assert b_out.shape[0] == b_0.shape[0] + b_1.shape[0]
    assert n_out == n_0 + n_1
    assert np.all(C_out == [[4, 0, 0],
                     [1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 1],
                     [0, 4, 0],
                     [0, 0, 4]])
    assert np.all(b_out == [4, 0, 0, 0, 4, 4])

def test_padding():
    '''
    Test for checking the padding of a single 
    linear constraint set
    '''
    C_0 = np.eye(3)
    
    C_out = cons.pad_constraints(C_0, 4, 9)

    assert C_out.shape == (3,9)

    with pytest.raises(cons.PaddingError):
        C_out = cons.pad_constraints(C_0, 4, 6)


def test_abstract_base_classes():
    '''
    Test for checking the abstract base classes
    '''
    with pytest.raises(TypeError):
        c = cons.Constraint()

    with pytest.raises(TypeError):
        c = cons.Constraint2D()

def test_1D_constraint():

    #Along first variable axis
    p0 = (-1, 0)
    p1 = (1, 0)

    c = cons.Constraint1D(p0, p1)
    C, b, n = c.constraints
    assert np.all(C == [[0, 1], 
                        [1, 0],
                        [-1, 0]])
    assert np.all(b == [0, -1, -1])
    assert n == 1

    #Along second variable axis
    p0 = (0, -1)
    p1 = (0, 1)

    c = cons.Constraint1D(p0, p1)
    C, b, n = c.constraints
    assert np.all(C == [[1, 0], 
                        [0, 1],
                        [0, -1]])
    assert np.all(b == [0, -1, -1])
    assert n == 1

    #Along equal variable axis
    p0 = (-1, -1)
    p1 = (1, 1)

    c = cons.Constraint1D(p0, p1)
    C, b, n = c.constraints
    assert np.all(C == [[-1, 1], 
                        [1, 0],
                        [0, 1],
                        [-1, 0],
                        [0, -1]])
    assert np.all(b == [0, -1, -1, -1, -1])
    assert n == 1


def test_circle_constraint():
    c = cons.CircleConstraint(1, 4)

    C, b, n = c.constraints
    C_comp = np.array([[-1, 1], 
                        [-1, -1],
                        [1, -1],
                        [1, 1]], dtype=np.float)
    assert np.allclose(C, C_comp)
    assert np.all(b == [-1, -1, -1, -1])
    assert n == 0

def test_sector_constraint():
    c = cons.SectorConstraint(1, np.deg2rad(0), np.deg2rad(90), 1)

    C, b, n = c.constraints

    C_comp = np.array([[ 1.00000000e+00, -6.12323400e-17],
       [-0.00000000e+00,  1.00000000e+00],
       [-5.00000000e-01, -1.33974596e-01],
       [-3.66025404e-01, -3.66025404e-01],
       [-1.33974596e-01, -5.00000000e-01]])

    b_comp = np.array([-0. , -0. , -0.5, -0.5, -0.5])

    assert np.allclose(C, C_comp)
    assert np.allclose(b, b_comp)
    assert n == 0

if __name__ == '__main__':
    test_concatenation()
    test_padding()
    test_abstract_base_classes()
    test_1D_constraint()
    test_circle_constraint()
    test_sector_constraint()