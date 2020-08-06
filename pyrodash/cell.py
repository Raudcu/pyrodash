import numpy as np
import pandas as pd
from pathlib import Path

from pyrodash.geometrics.parallelepiped import Parallelepiped
from pyrodash.blocks.tetrahedra import Tetrahedra
from pyrodash.blocks.spins import Spins
from pyrodash.blocks.monopole import Monopole


class UnitCell:
    """
    Class to build a unit cell of the system.

    ...

    Attributes
    ----------
    ijk : numpy array of int
        position of the cell in lattice parameter units.
    up_centers, down_centers : numpy array
        center positions of the up and down tetrahedra of the cell.
    initial_spin : int
        number of the first spin of the first up tetrahedron of the cell.
    spin_values : numpy array of int
        array with the values of the cell spins.
    cube : Parallelepiped object
        instance of the Parallelepiped class to use as cell cube.
    tetrahedra : list of Tetrahedra object
        contains instances of the Tetrahedra class for the cell tetrahedra.
    up_cubes, down_cubes : list of Parallelepiped object
        contains instances of the Parallelepiped class to use as individual
        cubes for the up and down tetrahedra.
    spins : list of Spins object
        contains instances of the Spins class for the cell spins.
    monopoles_up, monopoles_down : list of Monopole object
        contains instances of the Monopole class for the cell monopoles of 
        the up and down tetrahedra
    """

    def __init__(self, ijk, spin_values):
        """
        Parameters
        ----------
        ijk : list of int or numpy array of int
            position of the cell in lattice parameter units.
        spin_values : numpy array of int
            array with the values of all the spins of the system.
        """

        self.ijk = np.array(ijk)

        self.up_centers = (
            0.5 * np.array([[0, 0, 0], [1, 1, 0], [0, 1, 1], [1, 0, 1]]) + self.ijk
        ) / (np.sqrt(2) / 4)
        self.down_centers = self.up_centers + np.array([1, 1, 1]) / np.sqrt(2)

        _L = round((len(spin_values) / 16) ** (1 / 3))
        self.initial_spin = (
            self.ijk[0] + self.ijk[1] * _L + self.ijk[2] * _L * _L
        ) * 16
        self.spin_values = spin_values[self.initial_spin : self.initial_spin + 16]

        # Cube
        self.cube = Parallelepiped(np.sqrt(8), self.ijk * np.sqrt(8))

        # Tetrahedra
        self.tetrahedra = [Tetrahedra(center, init_count=i) for center,i in zip(self.up_centers, range(1, 17, 4))]

        # Individual cubes
        self.up_cubes = [
            Parallelepiped(np.sqrt(0.5), t.up_vertices[0] - np.sqrt([0.5, 0.5, 0.5]))
            for t in self.tetrahedra
        ]
        self.down_cubes = [
            Parallelepiped(np.sqrt(0.5), t.up_vertices[0]) for t in self.tetrahedra
        ]

        # Spins
        self.spins = [
            Spins(t.up_vertices, self.spin_values[i : i + 4])
            for t, i in zip(self.tetrahedra, range(0, 16, 4))
        ]

        # Monopoles Up
        self.monopoles_up = [
            Monopole(-int(sum(self.spin_values[i : i + 4])), center)
            for i, center in zip(range(0, 16, 4), self.up_centers)
        ]

        # Monopoles Down
        _data_file = Path(__file__).resolve().parent / "down_neighbors" / f"L{_L}.dat"

        _down_neighbors = pd.read_csv(
            _data_file, sep=r"\s+", header=None, index_col=0, dtype=np.int
        )

        self.monopoles_down = []
        for center, i in zip(self.down_centers, range(0, 16, 4)):

            spines_down = np.insert(_down_neighbors.loc[i].values, 0, i)

            self.monopoles_down.append(
                Monopole(int(sum(spin_values[spines_down])), center)
            )
