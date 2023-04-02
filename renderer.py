"""renders infos into text or images"""
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio


def write_points_table_to_png(
    df: pd.DataFrame, filename: str, headers: list[str] | None = None
):

    if headers is None:
        headers = list(df.columns)

    # specify some layout stuff
    layout = go.Layout(
        margin=go.layout.Margin(
            l=3,  # left margin
            r=3,  # right margin
            b=3,  # bottom margin
            t=3,  # top margin
        ),
        # and the font
        font=dict(family="Calibri"),
    )
    fig = go.Figure(
        data=[
            go.Table(
                columnwidth=[30, 145, 90, 175, 175, 175],
                header=dict(
                    values=headers,
                    fill_color="paleturquoise",
                    align="center",
                    font_size=19,
                    height=33,
                ),
                cells=dict(
                    values=df.transpose().values.tolist(),
                    fill_color="lavender",
                    align="center",
                    font_size=19,
                    height=33,
                ),
            )
        ],
        layout=layout,
    )
    pio.write_image(
        fig,
        file=filename,
        format="png",
        scale=2,
        width=700,
        height=202,
    )
