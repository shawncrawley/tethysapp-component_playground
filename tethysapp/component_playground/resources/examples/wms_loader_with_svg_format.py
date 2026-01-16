from tethysapp.component_playground.app import App


@App.page
def wms_loader_with_svg_format(lib):
    return lib.tethys.Display(
        lib.tethys.Map(
            lib.ol.layer.Image(
                lib.ol.source.Image(
                    options=lib.Props(
                        loader=lib.Props(
                            url="https://ahocevar.com/geoserver/wms",
                            params=lib.Props(
                                LAYERS=["topp:states"], FORMAT="image/svg+xml"
                            ),
                            ratio=1,
                            load=True,
                        )
                    )
                )
            )
        )
    )
