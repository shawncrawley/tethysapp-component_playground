from tethysapp.component_playground.app import App
from time import sleep

@App.page
def geolocation(lib):
    lib.register("geolocation.js", "geo", host="/static/component_playground/js", default_export="Geolocation")
    lib.bs.Toast  # Pre-load the Toast, since it loads conditionally
    error, set_error = lib.hooks.use_state(None)
    return lib.tethys.Display(
        lib.geo.Geolocation(
            trackingOptions=lib.Props(enableHighAccuracy=True),
            tracking=True,
            projection="EPSG:3857",
            onError=lambda e: set_error(e.message),
            onChange=lambda e: print(f"Change event: {e}"),
        ),
        lib.bs.Toast(
            style=lib.Style(position="absolute", top="70px", right="10px", zIndex="1000"),
            className="d-inline-block m-1",
            bg="danger",
            onClose=lambda _: set_error(None),
            show=error is not None,
        )(
            lib.bs.ToastHeader(lib.html.strong(className="me-auto")("Geolocation Error")),
            lib.bs.ToastBody(
                "Access was denied or is not available."
            )
        ) if error else None,
        lib.tethys.Map(key="map"),
    )
