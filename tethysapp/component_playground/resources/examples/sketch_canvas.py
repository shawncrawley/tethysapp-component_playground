from tethysapp.component_playground.app import App


@App.page
def sketch_canvas(lib):
    lib.register("sketch_canvas.js", "sc", host="/static/component_playground/js", default_export="SketchCanvas")
    color, set_color = lib.hooks.use_state("#000000")
    return lib.tethys.Display(
        lib.html.input(type="color", value=color, onChange=lambda e: set_color(e.target.value)),
        lib.sc.SketchCanvas(
            style=lib.Style(border="0.0625rem solid #9c9c9c", borderRadius="0.25rem"),
            width="500px",
            height="500px",
            strokeWidth=2,
            strokeColor=color,
            backgroundImage="/static/component_playground/images/graph_paper.svg",
        )
    )
