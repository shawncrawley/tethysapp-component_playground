import base64
import math
import numpy as np
from io import BytesIO
from pytablericons import TablerIcons, FilledIcon, OutlineIcon
from tethysapp.component_playground.app import App


def get_icon_data_url(icon, size=32, color="black"):
    icon_img = TablerIcons.load(icon, size=size, color=color)
    buffered = BytesIO()
    icon_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    data_url = f"data:image/png;base64,{img_str}"
    return data_url


@App.page
def mapping_with_pytablericons(lib):
    icon_size = 16
    icons = list(FilledIcon)
    num_icons = len(icons)
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
                    src=get_icon_data_url(icons[i], size=icon_size),
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
