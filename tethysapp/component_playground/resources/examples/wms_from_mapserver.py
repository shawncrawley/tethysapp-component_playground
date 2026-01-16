from tethysapp.component_playground.app import App


@App.page
def wms_from_mapserver(lib):
    return lib.tethys.Display(
        lib.tethys.Map(projection="EPSG:4326")(
            lib.ol.layer.Image(
                lib.ol.source.Image(
                    options=lib.Props(
                        loader=lib.Props(
                            url="https://demo.mapserver.org/cgi-bin/wms?",
                            params=lib.Props(
                                LAYERS=["bluemarble,country_bounds,cities"],
                                VERSION="1.3.0",
                                FORMAT="image/png",
                            ),
                            projection="EPSG:4326",
                            # note: serverType only needs to be set when hidpi is True
                            hidpi=True,
                            serverType="mapserver",
                        )
                    )
                )
            )
        )
    )
