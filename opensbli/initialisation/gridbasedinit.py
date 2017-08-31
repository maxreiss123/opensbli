#    OpenSBLI: An automatic code generator for solving differential equations.
#    Copyright (C) 2016 Satya P. Jammy, Christian T. Jacobs

#    This file is part of OpenSBLI.

#    OpenSBLI is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    OpenSBLI is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with OpenSBLI.  If not, see <http://www.gnu.org/licenses/>.

from opensbli.core.opensbliequations import NonSimulationEquations, Discretisation, Solution, OpenSBLIEquation
from opensbli.core.kernel import Kernel
from .common import *


class GridBasedInitialisation(Discretisation, NonSimulationEquations):
    def __new__(cls, order=None, **kwargs):
        ret = super(GridBasedInitialisation, cls).__new__(cls)
        if order:  # Local order if multiple instances of the class are declared on the block
            ret.order = order
        else:
            ret.order = 0
        ret.equations = []
        ret.kwargs = kwargs
        """A control parameter is needed for where to put these equations in the algorithm
        """
        ret.algorithm_place = [BeforeSimulationStarts()]
        return ret

    def __hash__(self):
        h = hash(self._hashable_content())
        self._mhash = h
        return h

    def _hashable_content(self):
        return "GridBasedInitialisation"

    def add_equations(cls, equation):
        #equation = cls._sanitise_equations(equation)
        if isinstance(equation, list):
            for no, eq in enumerate(equation):
                eq = OpenSBLIEquation(eq.lhs, eq.rhs)
                # eq.set_vector(no)
                cls.equations += [eq]
        else:
            equation = OpenSBLIEquation(equation.lhs, equation.rhs)
            cls.equations += [equation]
        return

    def spatial_discretisation(cls, schemes, block):
        kernel1 = Kernel(block, computation_name="Grid_based_initialisation%d" % cls.order)
        kernel1.set_grid_range(block)
        # Checking
        # for eq in block.list_of_equation_classes:
        # from opensbli.core.metrics import *
        # if isinstance(eq, MetricsEquation):
        # for k in eq.Kernels:
        # print k.computation_name, k.halo_ranges, k.ranges
        for d in range(block.ndim):
            for sc in schemes:
                if schemes[sc].schemetype == "Spatial":
                    kernel1.set_halo_range(d, 0, schemes[sc].halotype)
                    kernel1.set_halo_range(d, 1, schemes[sc].halotype)
        kernel1.add_equation(cls.equations)
        kernel1.update_block_datasets(block)
        cls.Kernels = [kernel1]
        # Checking
        # for eq in block.list_of_equation_classes:
        # from opensbli.core.metrics import *
        # if isinstance(eq, MetricsEquation):
        # for k in eq.Kernels:
        # print k.computation_name, k.halo_ranges, k.ranges
        return

    def apply_boundary_conditions(cls, block):
        """No boundary conditions in the Initialisation
        """
        return


# class GridGeneration(Discretisation, NonSimulationEquations):
#     def __new__(cls, )
