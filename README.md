# quota 

![](https://github.com/freol35241/quota/workflows/Quota/badge.svg)

**Qu**adratically **O**ptimized **T**hrust **A**llocation 

quota is an open source python package leveraging the optimization technique quadratic programming for allocation of thrust to thrusters fixed on a body in the plane (3DOFs). 

Example usage:

    from quota.thruster import AzimuthThruster
    from quota.allocator import MinimizePowerAllocator
    
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
