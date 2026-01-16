from tethysapp.component_playground.app import App


@App.page
def geojson_with_dynamic_style(lib):
    fill_color, set_fill_color = lib.hooks.use_state("#ff0000")
    stroke_color, set_stroke_color = lib.hooks.use_state("#000000")

    return lib.tethys.Display(style=lib.Style(position="relative"))(
        lib.html.div(style=lib.Style(position="absolute", top=10, right=20, zIndex=1))(
            lib.bs.FormLabel(htmlFor="fill-color")("Fill Color"),
            lib.bs.FormControl(
                id="fill-color",
                type="color",
                value=fill_color[:7],  # The [:7] is only added here in case you use the color picker built into the Component Playground editor to modify the value, since that uses an 8-digit hex to include transparency, but this requires a 6-digit hex
                onChange=lambda e: set_fill_color(e.target.value),
            ),
            lib.bs.FormLabel(htmlFor="stroke-color")("Stroke Color"),
            lib.bs.FormControl(
                id="stroke-color",
                type="color",
                value=stroke_color[:7],  # The [:7] is only added here in case you use the color picker built into the Component Playground editor to modify the value, since that uses an 8-digit hex to include transparency, but this requires a 6-digit hex
                onChange=lambda e: set_stroke_color(e.target.value),
            ),
        ),
        lib.tethys.Map(
            lib.ol.layer.Vector(
                style=lib.ol.style.Style(
                    stroke=lib.ol.style.Stroke(color=stroke_color, width=1),
                    fill=lib.ol.style.Fill(color=fill_color),
                )
            )(
                lib.ol.source.Vector(
                    options=lib.Props(
                        url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson",
                        format="GeoJSON",
                    )
                )
            )
        ),
    )
