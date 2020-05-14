from abc import ABC, abstractmethod
import numpy as np
import plotly.graph_objects as go


class Surface(ABC):
    """
    Abstract base class for plotly surfaces.

    ...

    Attributes
    ----------
    x, y, z : numpy array
        coordinates of the surface.
    surface : list of a plotly go
        surface plotly object.

    Methods
    -------
    _coordinates_calculation(self, n1, n2, mesh_size)
        Abstract method to calculate the cartesian coordinates of the 
        surface.
    _draw_surface(self, surface_color)
        Generates the plotly surface object.
    """

    @abstractmethod
    def __init__(
        self,
        n1=np.array([0, 0, 0]),
        n2=np.array([0, 0, 0]),
        surface_color="#636efa",
        mesh_size=50,
    ):
        """
        Parameters
        ----------
        n1, n2 : numpy array, optional
            coplanar vectors orthogonal to the axis, by default 
            np.array([0, 0, 0]). Only for Cilinder and Cone.
        surface_color : str, optional
            rgb, rgba, hex, hsl, hsv, or named color string for the
            surface color, by default "#636efa".
        mesh_size : integer, optional
            size `n` of the `n x n` mesh generated to calculate the
            coordinates of the surface, by default 50.
        """

        self.x, self.y, self.z = self._coordinates_calculation(n1, n2, mesh_size)
        self.surface = self._draw_surface(surface_color)

    @abstractmethod
    def _coordinates_calculation(self, n1, n2, mesh_size):
        """Abstract method to calculate the cartesian coordinates of the 
        surface.

        It is done by building a mesh and then use it to calculate the
        coordinates.

        Parameters
        ----------
        n1, n2 : numpy array
            coplanar vectors orthogonal to the axis (only for Cilinder and
            Cone).
        mesh_size : integer
            size `n` of the `n x n` mesh generated to calculate the
            coordinates of the surface.

        Returns
        -------
        x, y, z : numpy array
            coordinates of the surface.
        """

        pass

    def _draw_surface(self, surface_color):
        """Generates the plotly surface object.
        
        It uses the calculated coordinates to build the surface.

        Parameters
        ----------        
        surface_color : str
            rgb, rgba, hex, hsl, hsv, or named color string for the
            surface color.

        Returns
        -------
        list of a plotly go
            surface plotly object.
        """

        return [
            go.Surface(
                x=self.x,
                y=self.y,
                z=self.z,
                colorscale=[[0, surface_color], [1, surface_color]],
                hoverinfo="none",
                showscale=False,
                contours=dict(x_highlight=False, y_highlight=False, z_highlight=False),
                lighting=dict(ambient=0.6, diffuse=0.9, specular=0.25, roughness=0.35),
                lightposition=dict(x=-100, y=0, z=0),
            )
        ]
