'''
Tests for thruster module
'''
import numpy as np
import pytest
import quota.thruster as th
from quota.constraints import Constraint1D, Constraint2D

def test_base_class():
    pos = (2, 2)
    t = th.Thruster(pos)
    assert (t.pos_x, t.pos_y) == pos
    assert t.static_constraints() == []

    #with pytest.raises(NotImplementedError):
    #    t.dynamic_constraints()

    #with pytest.raises(NotImplementedError):
    #    t.plot()

    with pytest.raises(TypeError):
        t.add_constraint('Wrong input type')

@pytest.mark.parametrize('TH', [th.LongitudinalThruster, th.TransverseThruster])
def test_1D_thrusters(TH):
    pos = (8, 10)
    t = TH(pos, 1000)

    assert t.disjunctions == 1

    assert isinstance(t.static_constraints()[0], Constraint1D)

@pytest.mark.parametrize('TH', [th.AzimuthThruster])
def test_2D_thrusters(TH):
    pos = (8, 10)
    t = TH(pos, 1000, 18)

    assert t.disjunctions == 1

    assert isinstance(t.static_constraints()[0], Constraint2D)

if __name__ == '__main__':
    test_base_class()
    test_1D_thrusters(th.LongitudinalThruster)
    test_2D_thrusters(th.AzimuthThruster)
