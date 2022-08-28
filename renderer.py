"""renders infos into text or images"""

from time import sleep
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio


def df_to_png(df: pd.DataFrame, filename: str):
    layout = go.Layout(
        margin=go.layout.Margin(
            l=3,  # left margin
            r=3,  # right margin
            b=3,  # bottom margin
            t=3,  # top margin
        ),
        font=dict(family="Calibri"),
    )

    fig = go.Figure(
        data=[
            go.Table(
                # columnorder = [1,2],
                columnwidth=[30, 150, 130, 160, 160, 160],
                header=dict(
                    values=list(df.columns),
                    fill_color="paleturquoise",
                    align="center",
                    font_size=22,
                    height=33,
                ),
                cells=dict(
                    values=df.transpose().values.tolist(),
                    fill_color="lavender",
                    align="center",
                    # family="Arial Black",
                    font_size=22,
                    height=33,
                ),
            )
        ],
        layout=layout,
    )

    # fig.update_layout(width=500, height=300)

    pio.write_image(fig, file="table.png", format="png", scale=2, width=700, height=202)


if __name__ == "__main__":
    columns = [
        "",
        "",
        "Total",
        "1. Bundesliga",
        "2. Bundesliga",
        "3. Bundesliga",
    ]
    data = [
        [1, "Michel", 31, 9, 10, 12],
        [2, "Per", 27, 10, 6, 11],
        [3, "Alex", 26, 8, 6, 12],
        [4, "Dominik", 20, 8, 2, 10],
        [5, "Hannes", 19, 10, 3, 6],
    ]

    df = pd.DataFrame(data=data, columns=columns)

    df_to_png(df, "test.png")
    print("ENDE")
