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


if __name__ == '__main__':
    test_concatenation()
    test_padding()