import math
import numpy as np
from simplepycons import all_icons
from tethysapp.component_playground.app import App


@App.page
def mapping_with_simplepycons(lib):
    icon_size = 16
    icon_names = [x.split("_")[1] for x in dir(all_icons) if x.startswith("get_")][
        :100
    ]  # Limit to 100 unique icons
    num_icons = len(icon_names)
    num_rows = num_cols = int(math.sqrt(num_icons))
    x_min, x_max, x_spacing = -180, 180, 360 / num_rows
    y_min, y_max, y_spacing = -90, 90, 180 / num_rows

    x_coords = np.arange(x_min, x_max + x_spacing, x_spacing)
    y_coords = np.arange(y_min, y_max + y_spacing, y_spacing)

    X, Y = np.meshgrid(x_coords, y_coords)

    X_flat = X.ravel()
    Y_flat = Y.ravel()

    combinations_xy = np.vstack((X_flat, Y_flat)).T

    features = [
        lib.Props(
            geometry=lib.ol.geom.Point([int(x), int(y)]),
            style=lib.ol.Style(
                image=lib.ol.style.Icon(
                    anchor=[0, 0],
                    anchorXUnits="fraction",
                    anchorYUnits="pixels",
                    width=icon_size,
                    height=icon_size,
                    src=all_icons[icon_names[i]].customize_svg_as_data_url(
                        fill="blue", width=str(icon_size), height=str(icon_size)
                    ),
                )
            ),
        )
        for i, (x, y) in enumerate(combinations_xy)
        if i < num_icons
    ]

    return lib.tethys.Display(
        lib.tethys.Map(projection="EPSG:4326")(
            lib.ol.layer.Vector(
                lib.ol.source.Vector(features=features, format="olFeature")
            )
        )
    )
