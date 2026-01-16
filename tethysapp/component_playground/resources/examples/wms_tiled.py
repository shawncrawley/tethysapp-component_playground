from tethysapp.component_playground.app import App


@App.page
def wms_tiled(lib):
    return lib.tethys.Display(
        lib.tethys.Map(
            lib.ol.layer.WebGLTile(
                lib.ol.source.TileWMS(
                    options=lib.Props(
                        url="https://ahocevar.com/geoserver/wms",
                        params=lib.Props(LAYERS="topp:states", TILED=True),
                        serverType="geoserver",
                        # Countries have transparency, so do not fade tiles:
                        transition=0,
                    )
                )
            )
        )
    )
