from tethysapp.component_playground.app import App


@App.page
def esri_mapserver_as_image_layer(lib):
    return lib.tethys.Display(
        lib.tethys.Map(center=[-10997148, 4569099], zoom=4)(
            lib.ol.layer.Image(
                lib.ol.source.ImageArcGISRest(
                    options=lib.Props(
                        ratio=1,
                        params={},
                        url="https://sampleserver6.arcgisonline.com/ArcGIS/rest/services/USA/MapServer",
                    )
                )
            )
        )
    )
