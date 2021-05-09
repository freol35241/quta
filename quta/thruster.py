"""
Thruster module containing classes for different type of thrusters
"""
import numpy as np
from quta.constraints import Constraint, Constraint1D, CircleConstraint


class Thruster:
    """
    Class holding properties of a Thruster
    """

    def __init__(self, pos):
        self._x = np.array(pos)
        self._u = np.array([0, 0])
        self._constraints = []

    @property
    def pos_x(self):
        """
        x-position of thruster
        """
        return self._x[0]

    @property
    def pos_y(self):
        """
        y-position of thruster
        """
        return self._x[1]

    def add_constraint(self, constraint):
        """
        Add a constraint to this thruster
        """
        if isinstance(constraint, Constraint):
            self._constraints.append(constraint)
        else:
            raise TypeError("Constraint is not of proper type!")

    @property
    def disjunctions(self):
        """
        Returns number of disjunct constraints
        """
        return len(self._constraints)

    def static_constraints(self):
        """
        Returns static constaints
        """
        return self._constraints

    # def dynamic_constraints(self, current_state):
    #    raise NotImplementedError('Dynamic constraints are not yet implemented')

    # def plot(self):
    #    raise NotImplementedError('Thruster visualization is not yet implemented')


class TransverseThruster(Thruster):
    """
    Class holding properties of a transverse
     thruster. Force direction is transverse to
     the vessel longitudinal axis.

    Utilizes a line constraint with arbitrary
     direction, length and offset along line.
    """

    def __init__(self, pos, max_force):
        super().__init__(pos)

        self._max_force = max_force

        self.add_constraint(Constraint1D((0, -max_force), (0, max_force)))


class LongitudinalThruster(Thruster):
    """
    Class holding properties of a longitudinal
     thruster. Force direction is along to
     the vessel longitudinal axis.

    Utilizes a line constraint with arbitrary
     direction, length and offset along line.
    """

    def __init__(self, pos, max_force):
        super().__init__(pos)

        self._max_force = max_force

        self.add_constraint(Constraint1D((-max_force, 0), (max_force, 0)))


class AzimuthThruster(Thruster):
    """
    Convenience class for setting up a typical
     Azimuthing thruster.

    It is assumed that an Azimuthing thruster can
     produce the same amount of force in any direction
     [0,2*pi]. The only bound existing is then the maximum
     force that can be delivered (max_force).
    """

    def __init__(self, pos, max_force, n_discret):
        super().__init__(pos)

        self._max_force = max_force
        self._n_discret = int(n_discret // 2) * 2

        self.add_constraint(CircleConstraint(self._max_force, self._n_discret))
