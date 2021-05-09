"""
Integration tests for quota package
"""

import time
import pytest
import numpy as np

from quota.thruster import AzimuthThruster, TransverseThruster, Thruster
from quota.allocator import MinimizePowerAllocator, AllocationError

from quota.constraints import SectorConstraint, Constraint1D


def calculate_global_thrust(thruster_positions, xy_forces):
    out = np.zeros(3)
    xy_forces = xy_forces.reshape((-1, 2))

    for pos, xy_force in zip(thruster_positions, xy_forces):
        out[0] += xy_force[0]
        out[1] += xy_force[1]
        out[2] += -xy_force[0] * pos[1] + xy_force[1] * pos[0]

    return out


def test_double_stern_azimuths():
    az1 = AzimuthThruster((-20, 5), 10000, 32)
    az2 = AzimuthThruster((-20, -5), 10000, 32)

    a = MinimizePowerAllocator()

    a.add_thruster(az1)
    a.add_thruster(az2)

    wanted = [0, 500, 8000]

    u, res = a.allocate(wanted, relax=False)
    assert np.allclose(u, [-1800.0, 250.0, 1800.0, 250.0])
    actual = calculate_global_thrust([az1._x, az2._x], u)
    assert np.allclose(wanted, actual)

    with pytest.raises(AllocationError):
        u, res = a.allocate([25000, 0, 0], relax=False)

    u, res = a.allocate([25000, 0, 0], relax=True)
    assert np.allclose(u, [10000, 0, 10000, 0])
    assert np.allclose(res[0][-3:], [5000, 0, 0])


def test_single_stern_azimuth_with_bow_thruster():
    az = AzimuthThruster((-20, 0), 10000, 32)
    tt = TransverseThruster((20, 0), 1000)

    a = MinimizePowerAllocator()

    a.add_thruster(az)
    a.add_thruster(tt)

    wanted = [0, 500, 8000]

    u, res = a.allocate(wanted, relax=False)
    assert np.allclose(u, [0, 50, 0, 450])
    actual = calculate_global_thrust([az._x, tt._x], u)
    assert np.allclose(wanted, actual)

    with pytest.raises(AllocationError):
        u, res = a.allocate([0, 2002, 0], relax=False)

    u, res = a.allocate([0, 2002, 0], relax=True)
    assert np.allclose(u, [0, 1000, 0, 1000])
    assert np.allclose(res[0][-3:], [0, 2, 0], atol=1e-1)
