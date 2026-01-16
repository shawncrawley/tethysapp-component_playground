from tethysapp.component_playground.app import App


@App.page
def map_with_popup(lib):
    position, set_position = lib.hooks.use_state(None)

    return lib.tethys.Display(
        lib.html.div(
            id="dynamic",  # id_ is essential, as it's referenced in the associated "element" attribute below
            style=lib.Style(
                position="relative",
            ),
            hidden=position is None,
        )(
            lib.html.div(
                style=lib.Style(
                    position="absolute",
                    left="-6px",
                    width=0,
                    height=0,
                    border_left="6px solid transparent",  # Controls the width of the triangle
                    border_right="6px solid transparent",  # Controls the width of the triangle
                    border_bottom="6px solid #ff0000",
                )
            ),
            lib.html.div(
                style=lib.Style(
                    position="absolute",
                    left="-6px",
                    top="6px",
                    width="200px",
                    background_color="lightblue",
                    padding="1em",
                    border="1px black solid",
                )
            )(
                lib.icons.XCircle(
                    style=lib.Style(
                        position="absolute", right="10px", top="5px", font_weight="bold"
                    ),
                    onClick=lambda _: set_position(None),
                ),
                (
                    lib.html.div(f"You clicked at: {", ".join(map(str, position))}")
                    if position
                    else None
                ),
            ),
        ),
        lib.tethys.Map(onClick=lambda e: set_position(e.coordinate))(
            lib.ol.Overlay(
                position=position or [0, 0],
                element="dynamic",  # The id_ of the above component to be used for this Overlay
            )
        ),
    )
