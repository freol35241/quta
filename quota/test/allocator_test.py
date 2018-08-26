'''
Tests for allocator module
'''
import numpy as np
import pytest
import quota.allocator as al

def test_baseclass():
    with pytest.raises(TypeError):
        a = al.Allocator()

@pytest.mark.parametrize('IMP', [al.MinimizePowerAllocator])
def test_implementations(IMP):
    a = IMP()

    with pytest.raises(al.AllocationError):
        a.allocate(0, 0, 0)

if __name__ == '__main__':
    test_baseclass()
    test_implementations(al.MinimizePowerAllocator)