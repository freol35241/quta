import time
import numpy as np

from quota.thruster import AzimuthThruster, TransverseThruster, Thruster
from quota.allocator import MinimizePowerAllocator

from quota.constraints import SectorConstraint, Constraint1D



def test_function():
    az1 = AzimuthThruster((-20, 5), 10000, 32)
    az2 = AzimuthThruster((-20, -5), 10000, 32)
    az3 = AzimuthThruster((20, 0), 2000, 32)

    sp1 = Thruster((-20, 0))
    sp1.add_constraint(SectorConstraint(2000, np.deg2rad(350), np.deg2rad(10), 32))
    sp1.add_constraint(SectorConstraint(2000, np.deg2rad(80), np.deg2rad(100), 32))
    sp1.add_constraint(SectorConstraint(1000, np.deg2rad(180), np.deg2rad(270), 32))

    sp2 = Thruster((20, 0))
    sp2.add_constraint(Constraint1D((-200, 200), (200, -200)))

    #az4 = AzimuthThruster((-20, 0), 5000, 16)

    tt1 = TransverseThruster((20, 0), 1000)

    al = MinimizePowerAllocator()
    al.set_slack_coefficients([1000, 1000, 100])

    #al.add_thruster(az1)
    al.add_thruster(az2)
    #al.add_thruster(az3)
    #al.add_thruster(tt1)
    #al.add_thruster(az4)
    #al.add_thruster(sp1)
    al.add_thruster(sp2)
    #al.add_thruster(tt1)
    
    t1 = time.time()
    u, res = al.allocate([0, 300, 0], relax=False)

    dt = time.time() - t1
    print(dt)
    print(u)
    print(res)


if __name__ == '__main__':
    test_function()
