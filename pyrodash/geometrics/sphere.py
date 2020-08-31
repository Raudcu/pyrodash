import numpy as np

from pyrodash.geometrics.surface import Surface


class Sphere(Surface):
    """
    Class for drawing spheres to use as monopoles.

    It inherits from the Surface abstract base class.

    ...

    Attributes
    ----------
    center : numpy array
        x, y, z coordinates of the center.
    radius : float
        radius of the sphere.
    x, y, z : numpy array
        coordinates of the surface of the sphere.
    surface : list of a plotly go
        surface plotly object of the drawn sphere.
    """

    def __init__(self, center, radius, surface_color="#636efa", mesh_size=50):
        """
        Parameters
        ----------
        center : list of float or numpy array
            x, y, z coordinates of the center.
        radius : float
            radius of the sphere.
        surface_color : str, optional
            rgb, rgba, hex, hsl, hsv, or named color string for the
            surface color, by default "#636efa".
        mesh_size : integer, optional
            size `n` of the `n x n` mesh generated to calculate the
            coordinates of the surface, by default 50.
        """

        self.center = np.array(center)
        self.radius = radius

        self.x, self.y, self.z = self._coordinates_calculation(mesh_size)
        self.surface = self._draw_surface(surface_color)

    def _coordinates_calculation(self, mesh_size):
        """Calculates the cartesian coordinates of the surface of the
        sphere.

        It overrides the method of the parent abstract class.

        Parameters
        ----------
        mesh_size : integer
            size `n` of the `n x n` mesh generated to calculate the
            coordinates of the surface.

        Returns
        -------
        x, y, z : numpy array
            coordinates of the surface of the sphere.
        """

        theta = np.linspace(0, np.pi, mesh_size)
        phi = np.linspace(0, 2 * np.pi, mesh_size)
        theta, phi = np.meshgrid(theta, phi)

        x = self.center[0] + self.radius * np.sin(theta) * np.cos(phi)
        y = self.center[1] + self.radius * np.sin(theta) * np.sin(phi)
        z = self.center[2] + self.radius * np.cos(theta)

        return x, y, z


if __name__ == "__main__":

    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    import plotly.graph_objects as go

    s = Sphere([1, 1, 1], 0.5, mesh_size=100)

    fig = go.Figure(data=s.surface)

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(dcc.Graph(figure=fig))

    app.run_server(debug=True)
