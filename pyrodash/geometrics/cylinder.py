import numpy as np
from scipy.linalg import norm

from pyrodash.geometrics.surface import Surface
import pyrodash.utils.linalg as linalg


class Cylinder(Surface):
    """
    Class to build and draw a Cylinder.

    It inherits from the Surface abstract base class.

    ...

    Attributes
    ----------
    center : numpy array
        x, y, z coordinates of the center of the cylinder.
    radius : float
        radius of the cylinder.
    length : float
        length of the cylinder.
    axis : numpy array
        unit vector of the cylinder axis.
    base_center : numpy array
        x, y, z coordinates of the center of the base.
    top_center : numpy array
        x, y, z coordinates of the center of the top.
    x, y, z : numpy array
        coordinates of the surface of the cylinder.
    surface : list of a plotly go
        surface plotly object of the drawn cylinder.
    """

    def __init__(
        self,
        center,
        radius,
        length,
        axis,
        n1=np.array([0, 0, 0]),
        n2=np.array([0, 0, 0]),
        surface_color="#636efa",
        mesh_size=50,
    ):
        """
        Parameters
        ----------
        center : list of float or numpy array
            x, y, z coordinates of the center of the cylinder.
        radius : float
            radius of the cylinder.
        length : float
            length of the cylinder.
        axis : list of float or numpy array
            vector of the cylinder axis.
        n1, n2 : numpy array, optional
            coplanar vectors orthogonal to the axis, by default 
            np.array([0, 0, 0]).
        surface_color : str, optional
            rgb, rgba, hex, hsl, hsv, or named color string for the
            surface color, by default "#636efa".
        mesh_size : integer, optional
            size `n` of the `n x n` mesh generated to calculate the
            coordinates of the surface, by default 50.
        """

        self.center = np.array(center)
        self.radius = radius

        self.length = length
        self.axis = np.array(axis) / norm(axis)

        self.base_center = self.center - self.length / 2 * self.axis
        self.top_center = self.center + self.length / 2 * self.axis

        if np.all(n1 == 0) or np.all(n2 == 0):
            n1, n2 = linalg.perpendicular_plane_vectors(self.axis)

        self.x, self.y, self.z = self._coordinates_calculation(n1, n2, mesh_size)
        self.surface = self._draw_surface(surface_color)

    def _coordinates_calculation(self, n1, n2, mesh_size):
        """Calculates the cartesian coordinates of the surface of the
        cylinder.

        It overrides the method of the parent abstract class.

        Parameters
        ----------
        n1, n2 : numpy array
            coplanar vectors orthogonal to the cylinder axis.
        mesh_size : integer
            size `n` of the `n x n` mesh generated to calculate the
            coordinates of the surface.

        Returns
        -------
        x, y, z : numpy array
            coordinates of the surface of the cylinder.
        """

        theta = np.linspace(0, 2 * np.pi, mesh_size)
        t = np.linspace(0, 1, mesh_size)
        theta, t = np.meshgrid(theta, t)

        x, y, z = [
            self.base_center[i]
            + t * self.length * self.axis[i]
            + self.radius * np.sin(theta) * n1[i]
            + self.radius * np.cos(theta) * n2[i]
            for i in [0, 1, 2]
        ]

        return x, y, z


if __name__ == "__main__":

    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    import plotly.graph_objects as go

    c = Cylinder([2, 5, 7], 2, 10, [1, 1, 1], mesh_size=100)

    fig = go.Figure(data=c.surface)

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(dcc.Graph(figure=fig))

    app.run_server(debug=True)
