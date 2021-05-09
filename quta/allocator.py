"""
Module containing the core allocation solver functionality
"""

import warnings
import itertools
from abc import ABC, abstractmethod

import numpy as np
import quadprog

from quta.thruster import Thruster
from quta.constraints import concatenate_constraints, pad_constraints

DOFS = 3


class AllocationError(Exception):
    """
    AllocationError class
    """


class Allocator(ABC):
    """
    Abstract base class for allocation problem
     formulations.
    """

    def __init__(self):
        self._thrusters = []

        self.set_slack_coefficients()

    def set_slack_coefficients(self, coefs=(1000, 1000, 1000)):
        """
        Set slack coefficients [Fx, Fy, Mz] used in the
         problem formulation for penalty calculation.
        """
        self._slack_coefs = coefs

    @property
    def n_thrusters(self):
        """
        Number of thrusters assigned to this
         allocation problem.
        """
        return len(self._thrusters)

    @property
    def n_problem(self):
        """
        Number of unknown variables to be allocated
         in the original (non-relaxed) problem.
        """
        return 2 * self.n_thrusters

    @property
    def n_relaxed_problem(self):
        """
        Number of unknown variables to be allocated
         in the relaxed problem.
        """
        return self.n_problem + DOFS

    @abstractmethod
    def problem_formulation(self, relax):
        """
        Problem formulation, to be overrided
         by child class.
        """

    def add_thruster(self, thruster):
        """
        Add a thruster to the allocation problem.
        """
        if isinstance(thruster, Thruster):
            self._thrusters.append(thruster)
        else:
            raise TypeError("Thruster is not of proper type!")

    # pylint: disable=too-many-locals,invalid-name
    def assemble_constraints(self, global_thrust, relax, combination):
        """
        Assemble linear constraints into matrix form
        """
        C = np.zeros((DOFS, self.n_problem))
        C[0, ::2] = 1
        C[1, 1::2] = 1
        C[2, ::2] = [-thruster.pos_y for thruster in self._thrusters]
        C[2, 1::2] = [thruster.pos_x for thruster in self._thrusters]

        if relax:
            # Add slack variables
            C = np.concatenate((C, np.eye(3)), axis=1)

        n_eq = DOFS
        b = np.array(global_thrust, dtype="float")

        for i, tup in enumerate(zip(self._thrusters, combination)):
            t, disjunct = tup
            C_t, b_t, n_eq_t = t.static_constraints()[disjunct].constraints
            C_t = pad_constraints(C_t, i * 2, C.shape[1])
            C, b, n_eq = concatenate_constraints((C, b, n_eq), (C_t, b_t, n_eq_t))

        return C.T, b, n_eq

    # pylint: disable=too-many-locals,invalid-name
    def allocate(self, global_thrust, relax=True):
        """
        Allocate global thrust vector to available thrusters
        """

        if self.n_problem == 0:
            raise AllocationError(
                """At least one thruster must be added
            to the allocator-object before attempting an allocation!"""
            )

        G, a = self.problem_formulation(relax)

        disjuncts = []
        for t in self._thrusters:
            disjuncts.append(range(t.disjunctions))

        results = {}
        for combination in itertools.product(*disjuncts):

            C, b, n_eq = self.assemble_constraints(global_thrust, relax, combination)

            try:
                res = quadprog.solve_qp(
                    G, a, C, b, n_eq
                )  # pylint: disable=c-extension-no-member
                results[res[1]] = res
            except ValueError:
                warn_str = """This constraint combination has no solution:
                {}""".format(
                    combination
                )
                warnings.warn(warn_str, UserWarning)

        if not results:
            raise AllocationError(
                """This problem has no solution!
            Try adding slack variables by setting relax=True"""
            )

        res = results[min(results.keys())]

        return res[0][: self.n_problem], res


class MinimizePowerAllocator(Allocator):
    """
    Class for allocating thrust while minimizing total power consumption
    """

    # pylint: disable=invalid-name
    def problem_formulation(self, relax):
        """
        Problem formulation in matrix form
        """
        n = self.n_relaxed_problem if relax else self.n_problem

        G = np.eye(n)
        if relax:
            G[-3, -3] = self._slack_coefs[0]
            G[-2, -2] = self._slack_coefs[1]
            G[-1, -1] = self._slack_coefs[2]

        a = np.zeros(n)

        return G, a
