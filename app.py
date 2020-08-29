#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
from plotly.io import to_image

import base64
import pandas as pd
import json
import io

from pyrodash import UnitCell


# App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

server = app.server


# Layout
app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H1("Pyrodash")),
                dbc.Col(
                    html.A(
                        html.Img(
                            src=app.get_asset_url("GitHub-Mark-32px.png"),
                            alt="GitHub Repo",
                            style={"float": "right", "padding-right": "15px"},
                            id="github-logo",
                        ),
                        href="https://github.com/Raudcu/pyrodash",
                        target="_blank",
                    ),
                    width=1,
                ),
                dbc.Tooltip("GitHub Repo", target="github-logo", placement="left"),
            ],
            justify="between",
            align="center",
        ),
        html.H4(
            "An interactive app for drawing the pyrochlore lattice "
            + "and configurations of the Spin Ice model."
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            dcc.Loading(dcc.Graph(id="graph"), type="cube"),
                            style={"padding-bottom": "5px"},
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Loading(
                                        dbc.Button(
                                            "Generate pdf",
                                            size="lg",
                                            color="primary",
                                            block=True,
                                            id="generate_button",
                                        ),
                                        type="dot",
                                    ),
                                    width=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        dbc.Button(
                                            "Download Plot",
                                            size="lg",
                                            color="success",
                                            block=True,
                                            outline=True,
                                            disabled=True,
                                        ),
                                        id="download_place",
                                    ),
                                    width=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        dcc.Upload(
                                            dbc.Button(
                                                "Upload config file",
                                                size="lg",
                                                color="info",
                                                block=True,
                                            ),
                                            id="upload_data",
                                        ),
                                        id="upload_data_button",
                                    ),
                                    width=4,
                                ),
                                dbc.Tooltip(
                                    "Single column data of spin values",
                                    target="upload_data_button",
                                    placement="bottom",
                                ),
                            ],
                            align="center",
                            justify="start",
                        ),
                    ],
                    width={"size": 7, "offset": 1},
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Label("Configuration", width=4),
                                dbc.Col(
                                    dcc.Dropdown(
                                        options=[
                                            {"label": "Spin Ice +z", "value": "+z"},
                                            {
                                                "label": "Single Monopole Crystal",
                                                "value": "ms",
                                            },
                                            {
                                                "label": "Double Monopole Crystal",
                                                "value": "md",
                                            },
                                        ],
                                        value="+z",
                                        clearable=False,
                                        id="config_selection_dropdown",
                                    ),
                                    width=8,
                                ),
                                dcc.Store(id="store_selected_configuration_data"),
                            ],
                            no_gutters=True,
                            align="center",
                            style={"padding-bottom": "30px"},
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Number of Tetrahedra", width=4),
                                dbc.Col(
                                    dcc.Slider(
                                        min=1,
                                        max=4,
                                        marks={
                                            i: {
                                                "label": str(i),
                                                "style": {
                                                    "font-size": "15px",
                                                    "font-family": "Lato, Helvetica Neue",
                                                },
                                            }
                                            for i in range(1, 5)
                                        },
                                        value=4,
                                        id="tetra_slider",
                                    ),
                                    width=8,
                                ),
                            ],
                            no_gutters=True,
                            align="center",
                            style={"padding-bottom": "30px"},
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Which", width=2),
                                dbc.Col(
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "Up+Down", "value": "ud"},
                                            {"label": "Up", "value": "u"},
                                            {"label": "Down", "value": "d"},
                                        ],
                                        value="ud",
                                        id="tetra_radio",
                                    ),
                                    width=4,
                                ),
                                dbc.Label("Projection", width=3),
                                dbc.Col(
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "Perspective", "value": "ps"},
                                            {"label": "Orthorombic", "value": "or"},
                                        ],
                                        value="ps",
                                        id="projection_radio",
                                    ),
                                    width=3,
                                ),
                            ],
                            align="center",
                            style={"padding-bottom": "30px"},
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Cell Cube", width=2),
                                dbc.Col(
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "Yes", "value": "y"},
                                            {"label": "No", "value": "n"},
                                        ],
                                        value="y",
                                        id="cell_cube_radio",
                                    ),
                                    width=4,
                                ),
                                dbc.Label("Individual cubes", width=3),
                                dbc.Col(
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "Yes", "value": "y"},
                                            {"label": "No", "value": "n"},
                                        ],
                                        value="n",
                                        id="individual_cubes_radio",
                                    ),
                                    width=3,
                                ),
                            ],
                            align="center",
                            style={"padding-bottom": "30px"},
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Spins", width=2),
                                dbc.Col(
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "Yes", "value": "y"},
                                            {"label": "No", "value": "n"},
                                        ],
                                        value="n",
                                        id="spins_radio",
                                    ),
                                    width=4,
                                ),
                                dbc.Label("Monopoles", width=3),
                                dbc.Col(
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "Yes", "value": "y"},
                                            {"label": "No", "value": "n"},
                                        ],
                                        value="n",
                                        id="monopoles_radio",
                                    ),
                                    width=3,
                                ),
                            ],
                            align="center",
                            style={"padding-bottom": "30px"},
                        ),
                    ],
                    width=4,
                    style={"padding-right": "60px"},
                ),
            ],
            no_gutters=True,
            align="center",
        ),
    ]
)


# Callbacks
@app.callback(
    Output("store_selected_configuration_data", "data"),
    [Input("config_selection_dropdown", "value"), Input("upload_data", "contents")],
)
def configuration_data(config_selection, contents):

    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if input_id == "upload_data":

        _, content_string = contents.split(",")

        decoded = base64.b64decode(content_string)

        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), header=None)

        spin_values = df.squeeze()

    else:

        if config_selection == "+z":
            spin_values = pd.Series([1, -1, 1, -1] * 4)

        elif config_selection == "ms":
            spin_values = pd.Series([1, -1, -1, -1] * 4)

        elif config_selection == "md":
            spin_values = pd.Series([-1, -1, -1, -1] * 4)

    return spin_values.to_json()


@app.callback(
    Output("graph", "figure"),
    [
        Input("store_selected_configuration_data", "data"),
        Input("tetra_slider", "value"),
        Input("tetra_radio", "value"),
        Input("projection_radio", "value"),
        Input("cell_cube_radio", "value"),
        Input("individual_cubes_radio", "value"),
        Input("spins_radio", "value"),
        Input("monopoles_radio", "value"),
    ],
    [State("graph", "relayoutData")],
)
def cell_construction(
    configuration_data,
    tetra_count,
    which_tetras,
    projection,
    cube,
    individual_cubes,
    spins,
    monopoles,
    relayoutData,
):

    # Spin values
    s_spin_values = pd.read_json(configuration_data, typ="series")

    # Cell
    cell = UnitCell([0, 0, 0], s_spin_values.array)

    # Tetrahedra
    tetras = cell.tetrahedra[:tetra_count]

    if which_tetras == "ud":
        tetra_surfaces = [face for t in tetras for face in t.up_faces + t.down_faces]
        site_numbers = [t.site_numbers for t in tetras]

    elif which_tetras == "u":
        tetra_surfaces = [face for t in tetras for face in t.up_faces]
        site_numbers = [t.site_numbers for t in tetras]

    elif which_tetras == "d":
        tetra_surfaces = [face for t in tetras for face in t.down_faces]
        site_numbers = []

    data = tetra_surfaces + site_numbers

    # Cube
    if cube == "y":
        data += cell.cube.faces

    # Individual cubes
    if individual_cubes == "y":
        if which_tetras == "ud":
            cubes_faces = [
                face
                for cube in (
                    cell.up_cubes[:tetra_count] + cell.down_cubes[:tetra_count]
                )
                for face in cube.faces
            ]

        elif which_tetras == "u":
            cubes_faces = [
                face for cube in cell.up_cubes[:tetra_count] for face in cube.faces
            ]

        elif which_tetras == "d":
            cubes_faces = [
                face for cube in cell.down_cubes[:tetra_count] for face in cube.faces
            ]

        data += cubes_faces

    # Spins
    if spins == "y":
        spins_surfaces = [
            surface for spin in cell.spins[:tetra_count] for surface in spin.surfaces
        ]
        data += spins_surfaces

    # Monopoles
    if monopoles == "y":
        if which_tetras == "ud":
            for mu, md in zip(
                cell.monopoles_up[:tetra_count], cell.monopoles_down[:tetra_count],
            ):
                data += mu.surface + md.surface

        elif which_tetras == "u":
            for mu in cell.monopoles_up[:tetra_count]:
                data += mu.surface

        elif which_tetras == "d":
            for md in cell.monopoles_down[:tetra_count]:
                data += md.surface

    # Layout
    axis = dict(
        title="",
        showaxeslabels=False,
        showbackground=False,
        showgrid=False,
        showline=False,
        showspikes=False,
        showticklabels=False,
        ticks="",
    )

    layout = go.Layout(
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        template="simple_white",
        scene=dict(
            camera_eye=dict(x=0.5, y=-1.5, z=0.5), xaxis=axis, yaxis=axis, zaxis=axis,
        ),
    )

    if projection == "ps":
        layout.scene.camera.projection.type = "perspective"
    else:
        layout.scene.camera.projection.type = "orthographic"
        layout.scene.aspectmode = "manual"
        layout.scene.aspectratio = dict(x=1.5, y=1.5, z=1.5)

        if tetra_count == 2:
            if which_tetras == "u" or which_tetras == "d":
                layout.scene.aspectratio.z = 0.5
            else:
                layout.scene.aspectratio.z = 0.75

    # Return figure
    fig = go.Figure(data=data, layout=layout)

    if relayoutData and "scene.camera" in relayoutData:
        fig.update_layout(scene_camera_eye=relayoutData["scene.camera"]["eye"])

    return fig


@app.callback(
    [
        Output("download_place", "children"),
        Output("generate_button", "n_clicks_timestamp"),
    ],
    [
        Input("generate_button", "n_clicks"),
        Input("graph", "figure"),
        Input("graph", "relayoutData"),
    ],
)
def generate_plot(n_clicks, figure, relayoutData):

    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if input_id == "generate_button":
        fmt = "pdf"
        mimetype = "application/pdf"

        data = base64.b64encode(to_image(figure, format=fmt)).decode("utf-8")
        pdf_string = f"data:{mimetype};base64,{data}"

        return (
            html.A(
                dbc.Button("Download Plot", size="lg", color="success", block=True),
                download="pyrodash_figure.pdf",
                href=pdf_string,
            ),
            0,
        )
    else:
        return (
            dbc.Button(
                "Download Plot",
                size="lg",
                color="success",
                block=True,
                outline=True,
                disabled=True,
            ),
            0,
        )


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port="8050")
