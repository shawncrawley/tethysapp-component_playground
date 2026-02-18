from simplepycons import all_icons
from tethysapp.component_playground.app import App


@App.page
def mapping_with_dynamic_simplepycon(lib):
    icon_index, set_icon_index = lib.hooks.use_state(0)
    icon_size = 16
    icon_names = [x.split("_")[1] for x in dir(all_icons) if x.startswith("get_")]
    num_icons = len(icon_names)

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
                    src=all_icons[icon_names[icon_index]].customize_svg_as_data_url(
                        fill="black", width=str(icon_size), height=str(icon_size)
                    ),
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
