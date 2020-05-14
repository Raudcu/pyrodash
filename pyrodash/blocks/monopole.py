from pyrodash.geometrics.sphere import Sphere


class Monopole(Sphere):
    """
    Class to represent and draw the monopoles according to its charges.

    It inherits most of the Attributes from Sphere and adds the charge to
    them.

    ...

    Attributes
    ----------
    charge : int
        charge of the monopole.
    center : numpy array
        x, y, z coordinates of the center.
    radius : float
        radius of the sphere.
    x, y, z : numpy array
        coordinates of the surface of the sphere.
    surface : list with a plotly go
        surface plotly object of the drawn sphere.
    """

    def __init__(self, charge, center):
        """
        Parameters
        ----------
        charge : int
            charge of the monopole.
        center : list of float or numpy array
            x, y, z coordinates of the center.
        """

        self.charge = charge

        # Spin Ice
        if self.charge == 0:
            super().__init__(center, 0, surface_color="k")

        # Simple monopole
        elif self.charge == +2:
            super().__init__(center, 0.16, surface_color="#02590f")

        elif self.charge == -2:
            super().__init__(center, 0.16, surface_color="#be0119")

        # Double monopole
        elif self.charge == +4:
            super().__init__(center, 0.24, surface_color="#01ff07")

        elif self.charge == -4:
            super().__init__(center, 0.24, surface_color="r")


if __name__ == "__main__":

    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    import plotly.graph_objects as go

    m = Monopole(int(sum([1, 1, -1, 1])), [0, 0, 0])

    fig = go.Figure(data=m.surface)

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(dcc.Graph(figure=fig))

    app.run_server(debug=True)
