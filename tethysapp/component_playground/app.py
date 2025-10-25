from tethys_sdk.components import ComponentBase
from uuid import uuid4
import importlib
from reactpy import component
from django.views.decorators.clickjacking import xframe_options_sameorigin
from tethys_apps.base.page_handler import global_page_controller


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


@xframe_options_sameorigin
def handler(*args, **kwargs):
    return global_page_controller(*args, **kwargs)


@App.page
def home(lib):
    lib.register('@monaco-editor/react', 'me', default_export="Editor")
    user = lib.hooks.use_user()
    default_code_path = lib.hooks.use_resources().path / "default_code.py"
    default_code = lib.hooks.use_memo(lambda: default_code_path.read_text(), [])
    user_code, set_user_code = lib.hooks.use_state("")
    uuid, set_uuid = lib.hooks.use_state(str(uuid4()))
    render_code = ""

    def update_preview():
        code = user_code.replace('@App.page', '')
        (user_workspace.path / "code.py").write_text(code)
        set_uuid(str(uuid4()))
    
    user_workspace = lib.hooks.use_workspace(user)
    if user_workspace.checking_quota:
        pass
    elif user_workspace.quota_exceeded:
        pass
    else:
        if user_code:
            render_code = user_code
        elif (user_workspace.path / "code.py").exists():
            _code = (user_workspace.path / "code.py").read_text()
            render_code = _code
            set_user_code(_code)
        else:
            render_code = default_code

    return lib.tethys.Display(
        lib.bs.Row(
            lib.bs.Button(
                on_click=lambda _: update_preview(),
            )(
                "Render"
            )
        ),
        lib.bs.Row(
            lib.bs.Col(
                lib.me.Editor(
                    height="70vh",
                    defaultLanguage="python",
                    defaultValue=render_code,
                    onChange=lambda v, _: set_user_code(v),
                ),
            ),
            lib.bs.Col(
                lib.html.iframe(src=f"/apps/component-playground/preview?uuid={uuid}", style=lib.Style(width="100%", height="85vh")),
            )
        )
    )

@App.page(
    layout=None,
    handler=handler,
)
def preview(lib):
    user = lib.hooks.use_user()
    default_code_path = lib.hooks.use_resources().path / "default_code.py"
    user_workspace = lib.hooks.use_workspace(user)
    if user_workspace.checking_quota:
        return lib.html.h1("Loading...")
    elif user_workspace.quota_exceeded:
        return lib.html.h1("Quota Exceeded. Cannot render preview.")
    else:
        user_code_fpath = (user_workspace.path / "code.py")
        code_path = user_code_fpath if user_code_fpath.exists() else default_code_path
        spec = importlib.util.spec_from_file_location('playground_code', code_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return lib.html.div(style=lib.Style(height="100vh"))(
            component(module.test)(lib)
        )
