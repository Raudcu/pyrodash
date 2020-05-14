import numpy as np
from itertools import product
import plotly.graph_objects as go


class Parallelepiped:
    """
    Class to build and draw a Parallelepiped.

    ...

    Attributes
    ----------
    L : numpy array
        x, y, z lengths of the parallelepiped sides.
    initial_vertex_position : numpy array
        x, y, z coordinates of the initial vertex position.
    vertices : numpy array
        vertices coordinates of the parallelepiped.
    face_vertices : numpy array
        vertices coordinates of each face.
    faces : list of plotly go
        scatter 3d plotly objects of the parallelepiped faces.
    """

    def __init__(
        self,
        L,
        initial_vertex_position=[0, 0, 0],
        edge_color="black",
        edge_width=1.5,
        face_opacity=0,
    ):
        """
        Parameters
        ----------
        L : list of float or numpy array
            x, y, z lengths of the parallelepiped sides.
        initial_vertex_position : list of float or numpy array, optional
            x, y, z coordinates of the initial vertex position, 
            by default [0, 0, 0].
        edge_color : str, optional
            rgb, rgba, hex, hsl, hsv, or named color string for the edge
            color, by default "black".
        edge_width : float, optional
            edge width, by default 1.5.
        face_opacity : int between or equal to 0 and 1, optional
            opacity of the faces, by default 0.
        """

        self.L = np.array(L)
        self.initial_vertex_position = np.array(initial_vertex_position)

        self.vertices = self.initial_vertex_position + np.array(
            list(product([0, self.L[0]], [0, self.L[1]], [0, self.L[2]]))
        )

        self.face_vertices = self._face_vertices_calculation()

        self.faces = self._draw_faces(edge_color, edge_width, face_opacity)

    def _face_vertices_calculation(self):
        """Calculates the vertices coordinates of each parallelepiped face.

        Returns
        -------
        face_vertices : numpy array
            vertices coordinates of each face.
        """

        face_vertices = []

        # The six ways of grabbing four points between the eight
        # parallelepiped vertices.
        faces = [
            (2, 0, 1, 3),
            (4, 6, 7, 5),
            (6, 2, 3, 7),
            (0, 4, 5, 1),
            (0, 4, 6, 2),
            (1, 5, 7, 3),
        ]

        for face in faces:
            # The x,y,z coordinates of each of the four face vertex.
            vert_x = self.vertices[face, 0]
            vert_y = self.vertices[face, 1]
            vert_z = self.vertices[face, 2]

            face_vertices.append(
                [np.array(vert) for vert in zip(vert_x, vert_y, vert_z)]
            )

        return np.array(face_vertices)

    def _draw_faces(self, edge_color, edge_width, face_opacity):
        """Generates the plotly scatter 3d for the parallelepiped faces.

        It builds each face from the face vertices by generating two 
        scatters: one to ensure the edges with the proper color and width, 
        and the other one for the faces.

        Parameters
        ----------
        edge_color : str
            rgb, rgba, hex, hsl, hsv, or named color string for the edge
            color.
        edge_width : float.
            edge width.
        face_opacity : int between or equal to 0 and 1
            opacity of the faces.

        Returns
        -------
        faces : list of plotly go
            scatter 3d plotly objects of the parallelepiped faces.
        """

        faces = []

        for i, vert in enumerate(self.face_vertices):

            faces.append(
                go.Scatter3d(
                    x=vert[:, 0],
                    y=vert[:, 1],
                    z=vert[:, 2],
                    mode="lines",
                    line=dict(color=edge_color, width=edge_width),
                    hoverinfo="none",
                    showlegend=False,
                )
            )

            faces.append(
                go.Scatter3d(
                    x=vert[:, 0],
                    y=vert[:, 1],
                    z=vert[:, 2],
                    mode="lines",
                    line=dict(color="gray", width=0),
                    opacity=face_opacity,
                    surfaceaxis=i // 2,
                    surfacecolor="gray",
                    hoverinfo="none",
                    showlegend=False,
                )
            )

        return faces


if __name__ == "__main__":

    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    import plotly.graph_objects as go

    p = Parallelepiped([1, 2, 3], [1, 1, 1], "orange", 10, 0.2)

    fig = go.Figure(data=p.faces)

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(dcc.Graph(figure=fig))

    app.run_server(debug=True)
