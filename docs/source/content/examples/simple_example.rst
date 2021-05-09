.. quta-simple-example

Two stern-mounted, azimuthing thrusters 
==========================================

.. code:: python

    from quta.thruster import AzimuthThruster
    from quta.allocator import MinimizePowerAllocator
    
    az1 = AzimuthThruster((-20, 5), 10000, 32)
    az2 = AzimuthThruster((-20, -5), 10000, 32)

    a = MinimizePowerAllocator()
    
    a.add_thruster(az1)
    a.add_thruster(az2)
    
    u, res = a.allocate([0, 500, 8000], relax=False)