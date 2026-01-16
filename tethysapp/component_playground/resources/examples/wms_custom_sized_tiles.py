from pyproj import CRS, Transformer
import math
from tethysapp.component_playground.app import App


def get_resolutions():
    resolutions = []
    crs_3857 = CRS("EPSG:3857")
    geographic_bounds = crs_3857.area_of_use.bounds
    transformer = Transformer.from_crs(crs_3857.geodetic_crs, crs_3857, always_xy=True)
    proj_extent = transformer.transform_bounds(*geographic_bounds)
    start_resolution = (proj_extent[2] - proj_extent[0]) / 256
    for i in range(22):
        resolutions.append(start_resolution / math.pow(2, i))
    return resolutions


@App.page
def wms_custom_sized_tiles(lib):
    get_resolutions()
    return lib.tethys.Display(
        lib.tethys.Map(
            lib.ol.layer.Tile(
                lib.ol.source.TileWMS(
                    options=lib.Props(
                        url="https://ahocevar.com/geoserver/wms",
                        params=lib.Props(LAYERS=["topp:states"], TILED=True),
                        serverType="mapserver",
                        tileGrid=lib.Props(
                            extent=[-13884991, 2870341, -7455066, 6338219],
                            resolutions=get_resolutions(),
                            tileSize=[512, 256],
                        ),
                    )
                )
            )
        )
    )
