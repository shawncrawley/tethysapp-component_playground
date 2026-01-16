from tethysapp.component_playground.app import App


@App.page
def map_with_text_link_overlay(lib):
    static_position = lib.utils.transform_coordinate(
        [48.208889, 16.3725], "EPSG:4326", "EPSG:3857"
    )

    return lib.tethys.Display(
        lib.html.a(
            id="vienna",  # id_ is essential, as it's referenced in the associated "element" attribute below
            className="overlay",
            target="_blank",
            href="https://en.wikipedia.org/wiki/Vienna",
            style=lib.Style(
                text_decoration=None,
                color="white",
                font_size="11pt",
                font_weight="bold",
                text_shadow="black 0.1em 0.1em 0.2em",
            ),
        )("Vienna"),
        lib.tethys.Map(
            lib.ol.Overlay(
                options=lib.Props(stopEvent=False),
                position=static_position,
                element="vienna",  # The id_ of the above component to be used for this Overlay
            ),
        ),
    )
