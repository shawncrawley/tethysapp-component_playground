from tethysapp.component_playground.app import App


@App.page
def wms_getfeatureinfo_image_layer(lib):
    props, set_props = lib.hooks.use_state(None)

    wms_source = lib.ol.source.ImageWMS(
        options=lib.Props(
            url="https://ahocevar.com/geoserver/wms",
            params=lib.Props(LAYERS="ne:ne"),
            serverType="geoserver",
            crossOrigin="anonymous",
        )
    )

    return lib.tethys.Display(
        lib.html.div(style=lib.Style(height="85vh"))(
            lib.tethys.Map(
                default_basemap=None,
                on_click=lambda e: (
                    set_props(
                        lib.utils.fetch(
                            wms_source.get_feature_info_url(
                                e.coordinate,
                                e.target.frameState_.viewState.resolution,
                                e.target.values_.view.projection_.code_,
                                "EPSG:3857",
                                {"INFO_FORMAT": "text/html"},
                            )
                        )
                    )
                ),
            )(lib.ol.layer.Image(wms_source))
        ),
        lib.html.div(style=lib.Style(height="15vh", width="95vw"))(
            lib.html.iframe(width="100%", srcdoc=props)
            if props
            else lib.html.h1("Click Map For Feature Info")
        ),
    )
