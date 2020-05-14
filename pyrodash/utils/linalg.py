"""Linear algebra module

    It only contains a function to find a pair of coplanar vectors
    orthogonal between them and with a given one.
"""

import numpy as np
from scipy.linalg import norm


def perpendicular_plane_vectors(vector):
    """Function to find a pair of coplanar vectors orthogonal to a
    given one.

    It first finds a vector that points out in a direction different
    than the given vector. With this new one and the given one, it
    finds a unit vector, n1, perpendicular to them. Finally with
    the given vector and n1, it builds a third unit vector, n2,
    perpendicular to both of them and hence, coplanar with n1.

    Parameters
    ----------
    vector : numpy array
        given unit vector.

    Returns
    -------
    n1, n2 : numpy array
        coplanar unit vectors orthogonal to the given vector.
    """

    not_vector = np.array([1, 0, 0])
    if (vector == not_vector).all():
        not_vector = np.array([0, 1, 0])

    n1 = np.cross(vector, not_vector)
    n1 = n1 / norm(n1)

    n2 = np.cross(vector, n1)

    return n1, n2
