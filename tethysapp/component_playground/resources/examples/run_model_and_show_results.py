from tethysapp.component_playground.app import App
from tethys_sdk.components.utils import event
from tethysapp.component_playground.utils import my_fancy_demo_model

@App.page
def run_model_and_show_results(lib):
    model_results, set_model_results = lib.hooks.use_state(None)
    loading, set_loading = lib.hooks.use_state(False)
    return lib.tethys.Display(
        lib.lo.LoadingOverlay(active=loading, spinner=True)(
            lib.bs.Form(
                onSubmit=event(
                    lambda e: (
                        set_loading(True),
                        lib.utils.background_execute(
                            lambda: set_model_results(
                                my_fancy_demo_model(*[e["value"] for e in e["target"]["elements"]])
                            ),
                            callback=lambda _: set_loading(False)
                        )
                    ), 
                    prevent_default=True, 
                    stop_propagation=True
                )
            )(
                lib.bs.FormGroup(className="mb-3", controlId="Input1")(
                    lib.bs.FormLabel("Input 1"),
                    lib.bs.FormControl(type="text", placeholder="Enter input 1 here"),
                ),
                lib.bs.FormGroup(className="mb-3", controlId="Input2")(
                    lib.bs.FormLabel("Input 2"),
                    lib.bs.FormControl(type="file"),
                ),
                lib.bs.FormGroup(className="mb-3", controlId="Input3")(
                    lib.bs.FormLabel("Input 3"),
                    lib.bs.FormControl(type="color", default="#ff0000"),
                ),
                lib.html.div(
                    lib.bs.FormCheck(type="radio", name="input4", label="Option 1", id="input4option1"),
                    lib.bs.FormCheck(type="radio", name="input4", label="Option 2", id="input4option2"),
                    lib.bs.FormCheck(type="radio", name="input4", label="Option 3", id="input4option3"),
                    lib.bs.FormCheck(type="radio", name="input4", label="Option 4", id="input4option4"),
                ),
                lib.bs.FormCheck(type="checkbox", name="input5", label="Input 5", id="input5"),
                lib.bs.Button(type="submit", variant="primary")("Run Model"),
            ),
        ),
        lib.bs.Alert(variant="success", className="mt-3", show=model_results is not None)(
            lib.bs.AlertHeading("Model Results"),
            lib.html.hr(),
            lib.html.pre(model_results) if model_results else lib.html.div("Running model..."),
        ) if model_results else None,
    )
