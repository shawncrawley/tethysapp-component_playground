from tethysapp.component_playground.app import App


@App.page
def esri_xyz(lib):
    return lib.tethys.Display(
        lib.tethys.Map(default_basemap=None)(
            lib.ol.layer.WebGLTile(
                lib.ol.source.ImageTile(
                    options=lib.Props(
                        attributions=(
                            'Tiles \u00a9 <a href="https://services.arcgisonline.com/ArcGIS/'
                            + 'rest/services/World_Topo_Map/MapServer">ArcGIS</a>'
                        ),
                        url=(
                            "https://server.arcgisonline.com/ArcGIS/rest/services/"
                            + "World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
                        ),
                    )
                )
            )
        )
    )
