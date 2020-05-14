import numpy as np
from scipy.linalg import norm
import plotly.graph_objects as go

import pyrodash.utils.linalg as linalg


class Circle:
    """
    Class to build and draw a filled Circle in the space.

    ...

    Attributes
    ----------
    center : numpy array
        x, y, z coordinates of the circle center.
    radius : float
        radius of the circle.
    axis : numpy array
        unit vector of the circle axis.
    x, y, z : numpy array
        coordinates of the circle edge.
    scatter : list with a plotly go
        scatter 3d plotly object of a filled circle.
    """

    def __init__(
        self,
        center,
        radius,
        axis,
        n1=np.array([0, 0, 0]),
        n2=np.array([0, 0, 0]),
        color="#636efa",
    ):
        """
        Parameters
        ----------
        center : list of float or numpy array
            x, y, z coordinates of the circle center.
        radius : float
            radius of the circle.
        axis : list of float or numpy array
            unit vector of the circle axis.
        n1, n2 : numpy array, optional
            coplanar vectors orthogonal to the axis, by default 
            np.array([0, 0, 0]).
        color : str, optional
            rgb, rgba, hex, hsl, hsv, or named color string for the
            surface color, by default "#636efa".
        """

        self.center = np.array(center)
        self.radius = radius

        self.axis = np.array(axis) / norm(axis)

        if np.all(n1 == 0) or np.all(n2 == 0):
            n1, n2 = linalg.perpendicular_plane_vectors(self.axis)

        self.x, self.y, self.z = self._coordinates_calculation(n1, n2)
        self.scatter = self._draw_circle(color)

    def _coordinates_calculation(self, n1, n2):
        """Calculates the cartesian coordinates of the circle edge.

        It calculates the coordinates of the circle edge contained in the
        plane given by n1 and n2.

        Parameters
        ----------
        n1, n2 : numpy array
            coplanar vectors orthogonal to the circle axis.

        Returns
        -------
        x, y, z : numpy array
            coordinates of the circle edge.
        """

        theta = np.linspace(0, 2 * np.pi, 50)

        x, y, z = [
            self.center[i]
            + self.radius * np.cos(theta) * n1[i]
            + self.radius * np.sin(theta) * n2[i]
            for i in [0, 1, 2]
        ]

        return x, y, z

    def _draw_circle(self, color):
        """Generates the plotly scatter 3d object of a filled circle.
        
        It uses the calculated coordinates to draw the edges, and then 
        fills it.

        Parameters
        ----------
        color : str
            rgb, rgba, hex, hsl, hsv, or named color string for the
            surface color.

        Returns
        -------
        list of a plotly go
            scatter 3d plotly object of a filled circle.
        """

        return [
            go.Scatter3d(
                x=self.x,
                y=self.y,
                z=self.z,
                mode="lines",
                line_color=color,
                surfaceaxis=2,
                hoverinfo="none",
                showlegend=False,
            )
        ]


if __name__ == "__main__":

    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    import plotly.graph_objects as go

    c = Circle([2, 5, 7], 2, [1, 1, 1])
    
    fig = go.Figure(data=c.scatter)

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(dcc.Graph(figure=fig))

    app.run_server(debug=True)
