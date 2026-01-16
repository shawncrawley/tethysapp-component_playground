from tethysapp.component_playground.app import App

CUSTOM_PRJ = (
    "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 "
    + "+x_0=600000 +y_0=200000 +ellps=bessel "
    + "+towgs84=660.077,13.551,369.344,2.484,1.783,2.939,5.66 +units=m +no_defs"
)


@App.page
def wms_image_with_custom_projection(lib):
    return lib.tethys.Display(
        lib.tethys.Map(
            projection=lib.Props(
                code="EPSG:21781",
                extent=[485869.5728, 76443.1884, 837076.5648, 299941.7864],
                definition=CUSTOM_PRJ,
            ),
            zoom=2,
            center=lib.utils.transform_coordinate(
                [8.23, 46.86], "EPSG:4326", CUSTOM_PRJ
            ),
        )(
            lib.ol.layer.Tile(options=lib.Props(title="Custom Projection Basemap"))(
                lib.ol.source.TileWMS(
                    options=lib.Props(
                        attributions=(
                            '\u00a9 <a href="https://shop.swisstopo.admin.ch/en/products/maps/national/lk1000"'
                            + 'target="_blank">Pixelmap 1:1000000 / geo.admin.ch</a>'
                        ),
                        crossOrigin="anonymous",
                        params=lib.Props(
                            LAYERS="ch.swisstopo.pixelkarte-farbe-pk1000.noscale",
                            FORMAT="image/jpeg",
                        ),
                        url="https://wms.geo.admin.ch/",
                    ),
                )
            ),
            lib.ol.layer.Image(options=lib.Props(title="Flood Alert"))(
                lib.ol.source.ImageWMS(
                    options=lib.Props(
                        attributions=(
                            '\u00a9 <a href="https://www.hydrodaten.admin.ch/en/notes-on-the-flood-alert-maps.html"'
                            + 'target="_blank">Flood Alert / geo.admin.ch</a>'
                        ),
                        crossOrigin="anonymous",
                        params=lib.Props(LAYERS="ch.bafu.hydroweb-warnkarte_national"),
                        serverType="mapserver",
                        url="https://wms.geo.admin.ch/",
                    )
                )
            ),
        )
    )
