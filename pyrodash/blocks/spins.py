import numpy as np

from pyrodash.blocks.arrow import Arrow


class Spins:
    """
    Class to build and draw the spins of an Up Tetrahedron.

    The class generates, from the spin values passed to its constructor, 
    the axis of the spins and their respectives colors, and use the 
    Arrow class to build and draw the four spins.

    ...

    Attributes
    ----------
    base_spin_axes : numpy array
        class attribute with base vectors of the spin axes of an Up 
        Tetrahedron.
    positions : numpy array
        contains arrays with the x, y, z coordinates of each spin 
        position.
    s1234 : numpy array
        spin values.
    axes : numpy array
        contains arrays with the spin axes.
    colors : list of str
        strings of the spin colors.
    arrows : list of Arrow object
        contains instances of the Arrow class to use as spins.
    surfaces : list of plotly go
        plotly objects of the drawn spins.
    """

    base_spin_axes = np.array(
        [[1, 1, 1], [1, -1, -1], [-1, -1, 1], [-1, 1, -1]]
    ) / np.sqrt(3)

    def __init__(self, positions, s1234):
        """
        Parameters
        ----------
        positions : numpy array
            contains arrays with the x, y, z coordinates of each spin 
            position.
        s1234 : list of int or numpy array
            spin values.
        """

        self.positions = positions

        if not all(s == 1 or s == -1 for s in s1234):
            raise ValueError("spin values must be 1 or -1")
        else:
            self.s1234 = np.array(s1234)

        self.axes = np.diag(self.s1234) @ Spins.base_spin_axes

        self.colors = ["blue" if s == 1 else "black" for s in self.s1234]

        self.arrows = [
            Arrow(pos, 0.036, 0.6, axis, surface_color=color)
            for pos, axis, color in zip(self.positions, self.axes, self.colors)
        ]

        self.surfaces = [surface for arrow in self.arrows for surface in arrow.surface]


if __name__ == "__main__":

    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    import plotly.graph_objects as go

    positions = np.array(
        [
            [0.125, 0.125, 0.125],
            [0.125, -0.125, -0.125],
            [-0.125, -0.125, 0.125],
            [-0.125, 0.125, -0.125],
        ]
    ) / (np.sqrt(2) / 4)

    s = Spins(positions, [1, -1, 1, 1])

    fig = go.Figure(data=s.surfaces)

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(dcc.Graph(figure=fig))

    app.run_server(debug=True)
