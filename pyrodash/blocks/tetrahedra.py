import numpy as np
import plotly.graph_objects as go


class Tetrahedra:
    """
    Class for drawing Tetrahedra in pairs (one 'Up' and one 'Down') in the
    [111] direction.

    ...

    Attributes
    ----------
    center_up : numpy array
        x, y, z coordinates of the center of the Up Tetrahedron.
    L : float
        length of the side of the cube where the Tetrahedron is inscribed,
        by default 0.25.
    up_vertices, down_vertices : numpy array
        vertices coordinates of the Up and Down Tetrahedra.
    up_faces, down_faces : list of plotly go
        mesh3d plotly objects of the faces of the Up and Down Tetrahedra.
    site_numbers : plotly go
        scatter 3d plotly object without markers, to number the sites.
    """

    def __init__(self, center_up, L=0.25, init_count=1, N=1):
        """
        Parameters
        ----------
        center_up : list of float or numpy array
            x, y, z coordinates of the center of the Up Tetrahedron.
        L : float, optional
            length of the side of the cube where the Tetrahedron is
            inscribed, by default 0.25.
        init_count : int, optional
            spin from which start counting the sites, by default 1.
        N : integer, optional
            related to the opacity of the faces: the higher N is, the more
            transparent the faces will be, by default 1.
        """

        self.center_up = np.array(center_up)
        self.L = L

        self.up_vertices, self.down_vertices = self._vertices_calculation()
        self.up_faces, self.down_faces = self._draw_faces(N)
        self.site_numbers = self._sites(init_count)

    def _vertices_calculation(self):
        """Calculates the vertices coordinates of the Tetrahedra.

        It is done by adding to 'center_up' the positions of the vertices
        of the Up Tetrahedron with respect to its center. The Down
        Tetrahedron vertices are calculated by inverting the values of the
        vertices and moving them.

        Returns
        -------
        up_vertices, down_vertices : numpy array
            vertices coordinates of the Up and Down Tetrahedra.
        """

        up_vertices = self.center_up + self.L / 2 * np.array(
            [[1, 1, 1], [1, -1, -1], [-1, -1, 1], [-1, 1, -1]]
        )

        down_vertices = -up_vertices + 2 * up_vertices[0]

        return up_vertices, down_vertices

    def _draw_faces(self, N):
        """Generates the plotly 3d meshes for the faces of the Tetrahedra.
        
        It uses the vertices of the Tetrahedra to build the mesh for each
        face and then add it to the corresponding list.

        Parameters
        ----------
        N : integer
            related to the opacity of the faces: the higher N is, the more
            transparent the faces will be.

        Returns
        -------
        up_faces, down_faces : list of plotly go
            mesh3d plotly objects of the faces of the Up and Down
            Tetrahedra.
        """

        up_faces = []
        down_faces = []

        for i, face in enumerate([(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 3)]):
            up_faces.append(
                go.Mesh3d(
                    x=self.up_vertices[:, 0],
                    y=self.up_vertices[:, 1],
                    z=self.up_vertices[:, 2],
                    i=[face[0]],
                    j=[face[1]],
                    k=[face[2]],
                    opacity=(0.15 + i * 0.15) / np.cbrt(N),
                    facecolor=["mediumpurple"],
                    hoverinfo="none",
                    showscale=False,
                )
            )

            down_faces.append(
                go.Mesh3d(
                    x=self.down_vertices[:, 0],
                    y=self.down_vertices[:, 1],
                    z=self.down_vertices[:, 2],
                    i=[face[0]],
                    j=[face[1]],
                    k=[face[2]],
                    opacity=(0.15 + i * 0.15) / np.cbrt(N),
                    facecolor=["lightskyblue"],
                    hoverinfo="none",
                    showscale=False,
                )
            )

        return up_faces, down_faces

    def _sites(self, initial_spin):
        """Generates a Scatter 3d object without markers.

        It uses the vertices positions to build a scatter that has opacity
        zero in all the points, but that it's used to put the site number
        on the hover of each Up Tetrahedron site.

        Parameters
        ----------
         initial_spin : int
            spin from which start counting the sites.

        Returns
        -------
        list with a plotly go
            scatter 3d plotly object without markers, to number the sites.
        """

        return go.Scatter3d(
                x=self.up_vertices[:, 0],
                y=self.up_vertices[:, 1],
                z=self.up_vertices[:, 2],
                mode="markers",
                marker_color="mediumpurple",
                opacity=0,
                hoverinfo="text",
                hovertext=[initial_spin + i for i in range(4)],
                hoverlabel_font=dict(family="serif", size=20, color="white"),
                showlegend=False
            )


if __name__ == "__main__":

    import dash
    import dash_core_components as dcc
    import dash_html_components as html

    import plotly.graph_objects as go

    t = Tetrahedra([1, 1, 1])

    fig = go.Figure(data=t.up_faces + t.down_faces + [t.site_numbers])

    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(dcc.Graph(figure=fig))

    app.run_server(debug=True)
