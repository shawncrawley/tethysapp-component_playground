from tethysapp.component_playground.app import App


@App.page
def wms_with_legend(lib):
    legend_url, set_legend_url = lib.hooks.use_state("")

    wms_source = lib.ol.source.ImageWMS(
        options=lib.Props(
            url="https://ahocevar.com/geoserver/wms",
            params=lib.Props(LAYERS="topp:states"),
            ratio=1,
            serverType="geoserver",
        )
    )

    def update_legend_url(event=None):
        resolution = event.target.values_.resolution if event else None
        lib.utils.background_execute(
            lambda: set_legend_url(wms_source.get_legend_url(resolution)),
            delay_seconds=1,
        )

    lib.hooks.use_effect(lambda: update_legend_url(), dependencies=[])

    return lib.tethys.Display(style=lib.Style(position="relative"))(
        lib.html.div(
            style=lib.Style(position="absolute", top="5px", right="20px", zIndex=1)
        )(lib.html.img(src=legend_url) if legend_url else None),
        lib.ol.Map(
            lib.ol.View(
                onChange=update_legend_url,
                center=[-10997148, 4569099],
                zoom=4,
            ),
            lib.ol.layer.Tile(lib.ol.source.OSM()),
            lib.ol.layer.Image(wms_source),
        ),
    )
