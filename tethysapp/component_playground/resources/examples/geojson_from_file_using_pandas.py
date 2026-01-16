import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from tethys_sdk.components.utils import transform_coordinate
from tethysapp.component_playground.app import App


def csv_to_geojson(csv_path):
    df = pd.read_csv(csv_path)
    geometry = [
        Point(transform_coordinate(xy, "EPSG:4326", "EPSG:3857"))
        for xy in zip(df["lat"], df["lon"])
    ]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:3857")
    return gdf.to_json()


@App.page
def geojson_from_file_using_pandas(lib):
    resources = lib.hooks.use_resources()
    geojson = csv_to_geojson(resources.path / "points.csv")
    return lib.tethys.Display(
        lib.tethys.Map(
            lib.ol.layer.Vector(
                lib.ol.source.Vector(
                    options=lib.Props(features=geojson, format="GeoJSON")
                )
            )
        )
    )
