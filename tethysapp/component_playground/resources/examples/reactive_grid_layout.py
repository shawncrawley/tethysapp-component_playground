# This relies on a bugfix
import math
import random
from tethysapp.component_playground.app import App


def generate_layout(lib):
    layout = []
    for i in range(25):
        y = math.ceil(random.random() * 4) + 1
        layout.append(
            lib.Props(
                x=round(random.random() * 5) * 2,
                y=math.floor(i / 6) * y,
                w=2,
                h=y,
                i=str(i),
                static=random.random() < 0.05,
            )
        )
    return layout


@App.page
def reactive_grid_layout(lib):
    layout, set_layout = lib.hooks.use_state(generate_layout(lib))
    lib.register(
        "react-grid-layout@2.2.3",
        "rgl",
        default_export="RGL",
        styles=[
            "https://esm.sh/react-resizable@4.0.2/css/styles.css",
            "https://esm.sh/react-grid-layout@2.2.3/css/styles.css",
        ],
    )

    return lib.tethys.Display(
        lib.html.style(
            """
        .my-container {
            outline: 2px solid black;
        }
        """
        ),
        lib.bs.Button(onClick=lambda _: set_layout(generate_layout(lib)))(
            "Generate New Layout"
        ),
        lib.rgl.RGL(
            width=800,
            layout=layout,
            gridConfig=lib.Props(
                cols=12,
                rowHeight=30,
            )
        )(
            *[
                lib.html.div(
                    key=f"{i}",
                    className="my-container " + ("static" if l.static else ""),
                )(
                    lib.html.span(
                        className="text",
                        title="This item is static and cannot be removed or resized.",
                    )(f"{i} - Static")
                    if l.static
                    else lib.html.span(className="text")(f"{i} - Move, or resize me.")
                )
                for i, l in enumerate(layout)
            ]
        ),
    )
