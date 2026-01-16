from tethysapp.component_playground.app import App


@App.page
def geojson_from_url(lib):
    return lib.tethys.Display(
        lib.tethys.Map(
            lib.ol.layer.Vector(
                lib.ol.source.Vector(
                    options=lib.Props(
                        url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson",
                        format="GeoJSON",
                    )
                )
            )
        )
    )
