from tethysapp.component_playground.app import App


@App.page
def wms_without_projection(lib):
    return lib.tethys.Display(
        lib.ol.Map(
            lib.ol.View(
                options=lib.Props(
                    projection=lib.Props(code="EPSG:21781", units="m"),
                ),
                center=[660000, 190000],
                zoom=9,
            ),
            lib.ol.layer.Group(options=lib.Props(title="Overlays", fold="open"))(
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
                            params=lib.Props(
                                LAYERS="ch.bafu.hydroweb-warnkarte_national"
                            ),
                            serverType="mapserver",
                            url="https://wms.geo.admin.ch/",
                        )
                    )
                ),
            ),
            lib.ol.control.ScaleLine(),
            lib.tethys.LayerPanel(),
        )
    )
