# quta 

[![PyPI version shields.io](https://img.shields.io/pypi/v/quta.svg)](https://pypi.python.org/pypi/quta/)
![](https://github.com/freol35241/quta/workflows/quta/badge.svg)
[![codecov](https://codecov.io/gh/freol35241/quta/branch/master/graph/badge.svg)](https://codecov.io/gh/freol35241/quta)
![docs](https://github.com/freol35241/quta/workflows/docs/badge.svg)

**Qu**adratically optimized **T**hrust **A**llocation 

quta is an open source python package leveraging the optimization technique quadratic programming for allocation of thrust to thrusters fixed on a body in the plane (3DOFs). 

Example usage:

    from quta.thruster import AzimuthThruster
    from quta.allocator import MinimizePowerAllocator
    
    az1 = AzimuthThruster((-20, 5), 10000, 32)
    az2 = AzimuthThruster((-20, -5), 10000, 32)

    a = MinimizePowerAllocator()
    
    a.add_thruster(az1)
    a.add_thruster(az2)
    
    u, res = a.allocate([0, 500, 8000], relax=False)

ToDo

* Update readme
* Documentation/examples

Contributions welcome through pull requests!
