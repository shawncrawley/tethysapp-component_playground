from tethysapp.component_playground.app import App


@App.page
def wms_single_image(lib):
    return lib.tethys.Display(
        lib.tethys.Map(
            lib.ol.layer.Image(
                lib.ol.source.ImageWMS(
                    options=lib.Props(
                        url="https://ahocevar.com/geoserver/wms",
                        params=lib.Props(LAYERS="topp:states"),
                        ratio=1,
                        serverType="geoserver",
                    )
                )
            )
        )
    )
