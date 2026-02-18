from pathlib import Path
from reactpy import component
from tethys_sdk.components import ComponentBase
from .utils import generate_title, import_from_path
from uuid import uuid4


class App(ComponentBase):
    """
    Tethys app class for Component Playground.
    """

    name = "Component Playground"
    description = "Playground for Tethys Component App development."
    package = "component_playground"  # WARNING: Do not change this value
    index = "home"
    icon = f"{package}/images/icon.png"
    root_url = "component-playground"
    color = "#748b7b"
    tags = ""
    enable_feedback = False
    feedback_emails = []
    exit_url = "/apps/"
    default_layout = "NavHeader"
    nav_links = "auto"

    def example_links(self):
        return [
            {
                "href": f"/apps/{self.root_url}/example/{p.stem}/",
                "title": generate_title(p.stem),
            }
            for p in (self.resources_path.path / "examples").iterdir()
            if not p.stem.startswith("__") and p.stem != "welcome"
        ]

    @property
    def navigation_links(self):
        return super().navigation_links + self.example_links()

@App.page(title="Welcome")
def home(lib):
    return EditorAndPreview(lib, "welcome")

# @App.page(url="preview/{script_name}", index=-1, preload=[App().resources_path.path / "examples"])
@App.page(url="preview/{script_name}", index=-1)
def preview(lib, script_name):
    user = lib.hooks.use_user()
    user_workspace = lib.hooks.use_workspace(user)
    return Preview(lib, user_workspace, script_name)

# @App.page(url="example/{script_name}", index=-1, preload=[App().resources_path.path / "examples"])
@App.page(url="example/{script_name}", index=-1)
def examples(lib, script_name):
    return EditorAndPreview(lib, script_name)


def EditorAndPreview(lib, script_name):
    lib.register("editor.js", "e", default_export="Editor", host="/static/component_playground/js")
    lib.register(
        "react-bootstrap-toggle",
        "bst",
        styles=[
            "https://gitcdn.github.io/bootstrap-toggle/2.2.2/css/bootstrap-toggle.min.css",
        ],
        default_export="Toggle",
    )
    user = lib.hooks.use_user()
    auto_update, set_auto_update = lib.hooks.use_state(True)
    user_workspace = lib.hooks.use_workspace(user)
    examples_path = lib.hooks.use_resources().path / "examples"
    editor_code, set_editor_code = lib.hooks.use_state("")
    _, set_force_update = lib.hooks.use_state(True)
    render_id, set_render_id = lib.hooks.use_state(str(uuid4()))

    def initialize_code():
        if user_workspace.checking_quota:
            return
        elif user_workspace.quota_exceeded:
            return

        example_fpath = examples_path / f"{script_name}.py"
        if not example_fpath.exists():
            init_code = None
        else:
            init_code = example_fpath.read_text()

        set_editor_code(init_code)
        if init_code:
            update_preview(init_code.replace("@App.page", ""))

    def update_preview(code=None):
        code_fpath = Path(user_workspace.path) / f"{script_name}.py"
        code_fpath.write_text(code)
        set_force_update(lambda current: not current)
        set_render_id(str(uuid4()))

    lib.hooks.use_effect(initialize_code, [user_workspace])

    return lib.tethys.Display(
        lib.bs.Row(lib.html.h3(generate_title(script_name))),
        lib.bs.Row(
            lib.html.span(
                "Update Mode: ",
                lib.html.style(".toggle-handle{background: white;}"),
                lib.bst.Toggle(
                    size="sm",
                    width="200px",
                    onstyle="primary",
                    offstyle="secondary",
                    on="Auto",
                    off="On Click \u2193",
                    active=auto_update,
                    onClick=lambda *_: set_auto_update(not auto_update),
                ),
            ),
            lib.bs.Button(
                size="sm",
                on_click=lambda _: update_preview(editor_code.replace("@App.page", "")),
                disabled=auto_update,
            )("Render"),
        ),
        lib.bs.Row(
            lib.bs.Col(
                (
                    lib.e.Editor(
                        height="80vh",
                        defaultLanguage="python",
                        value=editor_code,
                        onChange=lambda v, _: (
                            set_editor_code(v),
                            (
                                update_preview(v.replace("@App.page", ""))
                                if auto_update
                                else None
                            ),
                        ),
                    )
                    if editor_code
                    else f'Example "{script_name}" does not exist.'
                ),
            ),
            lib.bs.Col(style=lib.Style(height="80vh", overflow="scroll"))(
                lib.html.div(key=render_id, style=lib.Style(height="100%", width="100%"))(
                    Preview(lib, user_workspace, script_name)
                )
            ),
        ),
    )


@component
def Preview(lib, user_workspace, script_name):
    if user_workspace.checking_quota:
        return lib.html.h2("Loading...")
    elif user_workspace.quota_exceeded:
        return lib.html.p("Your user quota has been exceeded.")
    try:
        code_fpath = Path(user_workspace.path) / f"{script_name}.py"
        module = import_from_path(script_name, code_fpath)
        return component(getattr(module, script_name))(lib)
    except Exception as e:
        return lib.html.p(str(e))
