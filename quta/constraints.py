"""
Module containing functionality for creating linearized
constraints for some simple geometries

All linearized constrains returned to be compatible
with quadprog format: C.T x >= b
"""
import math
from abc import ABC, abstractmethod
import numpy as np


class ConstraintError(Exception):
    """
    ConstraintError class
    """


class ConvexError(ConstraintError):
    """
    ConvexError class
    """


class PaddingError(ConstraintError):
    """
    PaddingError class
    """


# pylint: disable=invalid-name
def concatenate_constraints(original_set, additional_set):
    """
    Method for concatenating sets of linear constraints.
     original_set and additional_set are both tuples of
     for (C, b, n_eq). Output is a concatenated tuple of
     same form.

    All equality constraints are always kept on top.
    """
    C_org, b_org, n_org = original_set
    C_add, b_add, n_add = additional_set

    if n_add > 0:
        C_out = np.insert(C_org, n_org, C_add[:n_add, :], axis=0)
        C_out = np.concatenate((C_out, C_add[n_add:, :]))

        b_out = np.insert(b_org, n_org, b_add[:n_add])
        b_out = np.concatenate((b_out, b_add[n_add:]))

    else:
        C_out = np.concatenate((C_org, C_add))
        b_out = np.concatenate((b_org, b_add))

    n_out = n_org + n_add

    return C_out, b_out, n_out


def pad_constraints(C, pad_with_before, total_size, pad_value=0):
    """
    Method for padding a 2D constraint matrix in order to match
     the total number of variables in the problem formulation.
    """
    pad_with_after = total_size - C.shape[1] - pad_with_before

    if pad_with_after < 0:
        raise PaddingError("Padded size is larger than total size!")

    C_out = np.pad(
        C,
        ((0, 0), (pad_with_before, pad_with_after)),
        "constant",
        constant_values=pad_value,
    )
    return C_out


def _point_on_circle(angle, radius):
    return radius * np.cos(angle), radius * np.sin(angle)


#
#
#
#### Base constraint class ####
#

# pylint: disable=too-few-public-methods
class Constraint(ABC):
    """
    Abstract base class for a set
     of linear, convex constraints
    """

    def __init__(self):

        self._C, self._b, self._n = self._linearized_constraint()

    @abstractmethod
    def _linearized_constraint(self):
        """
        Abstract method, to be overridden.
        """

    @property
    def constraints(self):
        """
        Constraints in matrix and vector form
        """
        return self._C, self._b, self._n


#
#
#
#### 1D constraints ####
#


class Constraint1D(Constraint):
    """
    Abstract base class for a set of
     linear, convex constraints forming
     a 1D equality line with 'end caps'.
    """

    def __init__(self, po0, po1):
        x0, y0 = po0
        x1, y1 = po1

        dx = x1 - x0
        dy = y1 - y0
        angle = np.arctan2(dy, dx)

        self._angle = angle
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1

        super().__init__()

    def _linearized_constraint(self):

        C = np.zeros((5, 2))
        b = np.zeros(5)

        x0, y0, x1, y1 = self._x0, self._y0, self._x1, self._y1
        a = self._angle

        if a / np.pi == a // np.pi:
            # Only forces in x-direction allowed
            C = np.zeros((3, 2))
            b = np.zeros(3)

            # Equality constraint
            C[0, 0] = 0
            C[0, 1] = 1
            b[0] = 0

            # Boundaries
            C[1] = [1, 0]
            b[1] = x0
            C[2] = [-1, 0]
            b[2] = -x1

        elif a / (0.5 * np.pi) == a // (0.5 * np.pi):
            # Only forces in y-direction allowed
            C = np.zeros((3, 2))
            b = np.zeros(3)

            # Equality constraint
            C[0, 0] = 1
            C[0, 1] = 0
            b[0] = 0

            # Boundaries
            C[1] = [0, 1]
            b[1] = y0
            C[2] = [0, -1]
            b[2] = -y1

        else:
            # Forces in both x- and y-direction allowed
            C = np.zeros((5, 2))
            b = np.zeros(5)

            x_c = -(y1 - y0) / (x1 - x0)
            y_c = 1
            b_c = y1 + x_c * x1

            # Equality constraint
            C[0, 0] = x_c
            C[0, 1] = y_c
            b[0] = b_c

            # Boundaries
            C[1] = [1, 0]
            b[1] = min([x0, x1])
            C[2] = [0, 1]
            b[2] = min([y0, y1])
            C[3] = [-1, 0]
            b[3] = -max([x0, x1])
            C[4] = [0, -1]
            b[4] = -max([y0, y1])

        return C, b, 1


#
#
#
#### 2D constraints ####
#


class Constraint2D(Constraint):
    """
    Abstract base class for a set of
     linear, convex constraints forming
     a 2D boundary surface.
    """

    @abstractmethod
    def _boundary_points(self):
        pass

    def _linearized_constraint(self):

        points = self._boundary_points()
        n = len(points)

        C = np.zeros((n, 2))
        b = np.zeros(n)

        for i in range(0, n):
            x0, y0 = points[i - 1]
            x1, y1 = points[i]
            C[i, 0] = y1 - y0
            C[i, 1] = x0 - x1
            b[i] = x0 * y1 - x1 * y0

        return -C, -b, 0  # Negation to adhere to quadprog format C.T x >= b


class CircleConstraint(Constraint2D):
    """
    Constraint describing a circle
    """

    def __init__(self, radius, edges=16):
        self._radius = radius
        self._edges = edges
        super().__init__()

    def _boundary_points(self):

        n = self._edges
        radius = self._radius

        step_angle = 2 * np.pi / n

        points = []
        for i in range(0, n):
            points.append(_point_on_circle(i * step_angle, radius))

        return points


class SectorConstraint(Constraint2D):
    """
    Constraint describing a circle sector
    """

    def __init__(self, radius, start, end, edges=10):

        delta = (end - start) % (2 * np.pi)
        if delta > np.pi:
            raise ConvexError(
                """Delta angle of this SectorConstraint
                               is {:.1f} deg which is greater than 180
                               deg. Please reformulate to a convex
                               constraint.""".format(
                    np.rad2deg(delta)
                )
            )

        self._radius = radius
        self._start = start
        self._edges = edges
        self._delta = delta

        super().__init__()

    def _boundary_points(self):

        radius = self._radius
        start = self._start
        delta = self._delta

        n = math.ceil(delta / 2 * np.pi * self._edges)

        step_angle = delta / n

        points = []

        # Origin
        points.append((0, 0))

        # Circle arc
        for i in range(0, n + 1):
            points.append(_point_on_circle(i * step_angle + start, radius))

        return points
