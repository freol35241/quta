"""
Tests for allocator module
"""
import pytest
import quta.allocator as al


def test_baseclass():
    with pytest.raises(TypeError):
        a = al.Allocator()


@pytest.mark.parametrize("IMP", [al.MinimizePowerAllocator])
def test_implementations(IMP):
    a = IMP()

    with pytest.raises(al.AllocationError):
        a.allocate(0, 0)
