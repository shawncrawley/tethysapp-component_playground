import base64
from io import BytesIO
from pytablericons import TablerIcons, FilledIcon
from tethysapp.component_playground.app import App


def get_icon_data_url(icon, size=32, color="black"):
    icon_img = TablerIcons.load(icon, size=size, color=color)
    buffered = BytesIO()
    icon_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    data_url = f"data:image/png;base64,{img_str}"
    return data_url


@App.page
def mapping_with_dynamic_pytablericon(lib):
    icon_index, set_icon_index = lib.hooks.use_state(0)
    icon_size = 16
    icons = list(FilledIcon)
    num_icons = len(icons)

    features = [
        lib.ol.Feature(
            geometry=lib.ol.geom.Point([0, 0]),
            style=lib.ol.Style(
                image=lib.ol.style.Icon(
                    anchor=[0, 0],
                    anchorXUnits="fraction",
                    anchorYUnits="pixels",
                    width=icon_size,
                    height=icon_size,
                    src=get_icon_data_url(icons[icon_index], size=icon_size),
                )
            ),
        )
    ]

    return lib.tethys.Display(
        lib.bs.Button(
            style=lib.Style(position="absolute", right="20px", zIndex=1),
            onClick=lambda _: set_icon_index(
                icon_index + 1 if icon_index + 1 < num_icons else 0
            ),
        )("Swap Icon"),
        lib.tethys.Map(
            lib.ol.layer.Vector(
                lib.ol.source.Vector(features=features, format="olFeature")
            )
        ),
    )
