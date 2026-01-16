import datetime as dt
from tethysapp.component_playground.app import App


def three_hours_ago():
    now = dt.datetime.now()
    return (now - dt.timedelta(hours=3)).replace(
        minute=int(now.minute / 15) * 15, second=0, microsecond=0
    )


@App.page
def wms_time_enabled_layer(lib):
    frame_rate = 0.5  # frames per second
    wms_time, set_wms_time = lib.hooks.use_state(lambda: three_hours_ago())
    timer, set_timer = lib.hooks.use_state(None)

    return lib.tethys.Display(style=lib.Style(position="relative"))(
        lib.html.div(
            style=lib.Style(zIndex=1, position="absolute", top="5px", right="20px")
        )(
            lib.html.div(style=lib.Style(display="flex", justify_content="center"))(
                lib.html.button(
                    on_click=lambda _: set_timer(
                        lib.utils.background_execute(
                            lambda: set_wms_time(
                                lambda old: (
                                    three_hours_ago()
                                    if old + dt.timedelta(minutes=15)
                                    > dt.datetime.now()
                                    else old + dt.timedelta(minutes=15)
                                )
                            ),
                            repeat_seconds=1 / frame_rate,
                        )
                    ),
                    disabled=timer is not None,
                )("Play"),
                lib.html.button(
                    on_click=lambda _: (
                        timer.cancel() if timer else None,
                        set_timer(None),
                    ),
                    disabled=timer is None,
                )("Stop"),
            ),
            lib.html.div(f"Time: {wms_time.isoformat()}"),
        ),
        lib.tethys.Map(
            lib.ol.layer.Tile(
                lib.ol.source.TileWMS(
                    options=lib.Props(
                        url="https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r-t.cgi"
                    ),
                    params=lib.Props(
                        LAYERS=["nexrad-n0r-wmst"], TIME=wms_time.isoformat()
                    ),
                )
            )
        ),
    )
