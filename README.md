# Overview

An interactive web app for drawing a unit cell of the pyrochlore lattice (corner-sharing tetrahedra) and configurations of the Spin Ice model. 

It was developed using Python and Dash, containerized with Docker and deployed on Azure.

Website: <https://pyrodash.azurewebsites.net/> (because it's deployed with a free plan, it may take some time to load after a period of inactivity).

# Possible general improvements

* Be able to plot more than one cell.
* Change a configuration by double clicking on a spin (it'll probably have performance issues).
* Specify width for different screen sizes.
* Be able to change the view by choosing from a list of typical orientations.
* Include clientside callback to improve performance of the generate pdf callback.
