from tethysapp.component_playground.app import App


@App.page
def esri_mapserver_as_tile_layer(lib):
    return lib.tethys.Display(
        lib.tethys.Map(center=[-10997148, 4569099], zoom=4)(
            lib.ol.layer.Tile(extent=[-13884991, 2870341, -7455066, 6338219])(
                lib.ol.source.TileArcGISRest(
                    url="https://sampleserver6.arcgisonline.com/ArcGIS/rest/services/USA/MapServer"
                )
            )
        )
    )
