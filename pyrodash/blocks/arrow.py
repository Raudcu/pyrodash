import numpy as np

from pyrodash.geometrics import Cylinder
from pyrodash.geometrics import Cone
from pyrodash.geometrics import Circle
import pyrodash.utils.linalg as linalg


class Arrow:
    """
    Class to draw an Arrow.

    To do it, it uses a Cylinder, a Cone and two circles as the respective
    bases. It can be drawn with a pivot on the tail, the mid or the tip.

    ...

    Attributes
    ----------
    pos : numpy array
        x, y, z coordinates of the arrow position.
    radius : float
        radius of the arrow cylinder.
    length : float
        total length of the arrow.
    axis : numpy array
        unit vector of the arrow axis.
    pivot : str
        part of the arrow that is anchored to pos, by default 'mid'.
    cylinder : Cylinder object
        instance of the Cylinder class to use as the arrow shaft.
    base_cylinder : Circle object
        instance of the Circle class for the cylinder base.
    cone : Cone object
        instance of the Cone class to use as the arrow tip.
    base_cone : Circle object.
        instance of the Circle class for the cone base.
    surface : list of plotly go
        plotly objects of the drawn arrow.
    """

    def __init__(
        self,
        pos,
        radius,
        length,
        axis,
        cone_length_ratio=0.4,
        cone_cylinder_radius_ratio=1.8,
        pivot="mid",
        surface_color="#636efa",
        mesh_size=50,
    ):
        """
        Parameters
        ----------
        pos : list of float or numpy array
            x, y, z coordinates of the arrow position.
        radius : float
            radius of the arrow shaft.
        length : float
            total length of the arrow.
        axis : list of float or numpy array
            unit vector of the arrow axis.
        cone_length_ratio : float, optional
            ratio between the length of the tip (arrow head) and the total
            length, by default 0.4
        cone_cylinder_radius_ratio : float, optional
            ratio between the shaft and the tip radiuses, by default 1.8.
        pivot : {'tail', 'mid', 'tip'}, optional
            part of the arrow that is anchored to pos, by default 'mid'.
        surface_color : str, optional
            rgb, rgba, hex, hsl, hsv, or named color string for the
            surface color, by default "#636efa".
        mesh_size : integer, optional
            size `n` of the `n x n` mesh generated to calculate the
            coordinates of the surface, by default 50.
        """

        self.pos = np.array(pos)
        self.radius = radius

        self.length = length
        self.axis = np.array(axis) / np.linalg.norm(np.array(axis))

        cylinder_radius = self.radius
        cylinder_length = (1 - cone_length_ratio) * self.length

        cone_base_radius = cone_cylinder_radius_ratio * cylinder_radius
        cone_length = cone_length_ratio * self.length

        if pivot not in {"tail", "mid", "tip"}:
            raise ValueError(
                f"'{pivot}' is not a valid value for pivot; "
                "supported values are 'tail', 'mid', 'tip'"
            )
        else:
            self.pivot = pivot

        if self.pivot == "tail":
            cylinder_center = np.array(pos) + 0.5 * cylinder_length * self.axis
        elif self.pivot == "mid":
            cylinder_center = np.array(pos) - 0.5 * cone_length * self.axis
        elif self.pivot == "tip":
            cylinder_center = (
                np.array(pos) - (cone_length + 0.5 * cylinder_length) * self.axis
            )

        n1, n2 = linalg.perpendicular_plane_vectors(self.axis)

        self.cylinder = Cylinder(
            cylinder_center,
            cylinder_radius,
            cylinder_length,
            self.axis,
            n1,
            n2,
            surface_color,
            mesh_size,
        )
        self.base_cylinder = Circle(
            self.cylinder.base_center, cylinder_radius, self.axis, n1, n2, surface_color
        )

        self.cone = Cone(
            self.cylinder.top_center,
            cone_base_radius,
            cone_length,
            self.axis,
            n1,
            n2,
            surface_color,
            mesh_size,
        )
        self.base_cone = Circle(
            self.cone.base_center, cone_base_radius, self.axis, n1, n2, surface_color
        )

        self.surface = (
            self.cylinder.surface
            + self.base_cylinder.scatter
            + self.cone.surface
            + self.base_cone.scatter
        )


if __name__ == "__main__":

    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    import plotly.graph_objects as go

    a = Arrow([1, 2, 3], 0.5, 10, [-1, -2, 1], pivot="tail", mesh_size=100)

    fig = go.Figure()

    fig.add_traces(a.surface)

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(dcc.Graph(figure=fig))

    app.run_server(debug=True)
