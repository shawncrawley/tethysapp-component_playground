from tethysapp.component_playground.app import App


@App.page
def map_with_marker_overlay(lib):
    static_position = lib.utils.transform_coordinate(
        [48.208889, 16.3725], "EPSG:4326", "EPSG:3857"
    )

    return lib.tethys.Display(
        lib.html.div(
            id="marker",  # id_ is essential, as it's referenced in the associated "element" attribute below
            style=lib.Style(
                width="20px",
                height="20px",
                border="1px solid #088",
                border_radius="10px",
                background_color="#0FF",
                opacity="0.5",
            ),
        ),
        lib.tethys.Map(
            lib.ol.Overlay(
                options=lib.Props(stopEvent=False),
                position=static_position,
                positioning="center-center",
                element="marker",  # The id_ of the above component to be used for this Overlay
            ),
        ),
    )
