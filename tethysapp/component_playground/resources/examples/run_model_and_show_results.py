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
                        print(e['formData']),
                        lib.utils.background_execute(
                            lambda: set_model_results(
                                my_fancy_demo_model(**e['formData'])
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
                    lib.bs.FormControl(type="text", name="input1", placeholder="Enter input 1 here"),
                ),
                lib.bs.FormGroup(className="mb-3", controlId="Input2")(
                    lib.bs.FormLabel("Input 2"),
                    lib.bs.FormControl(type="file", name="input2"),
                ),
                lib.bs.FormGroup(className="mb-3", controlId="Input3")(
                    lib.bs.FormLabel("Input 3"),
                    lib.bs.FormControl(type="color", name="input3", default="#ff0000"),
                ),
                lib.html.div(
                    lib.bs.FormCheck(type="radio", name="input4", label="Option 1", value="option1"),
                    lib.bs.FormCheck(type="radio", name="input4", label="Option 2", value="option2"),
                    lib.bs.FormCheck(type="radio", name="input4", label="Option 3", value="option3"),
                    lib.bs.FormCheck(type="radio", name="input4", label="Option 4", value="option4"),
                ),
                lib.bs.FormCheck(type="checkbox", name="input5", label="Input 5"),
                lib.bs.Button(type="submit", variant="primary")("Run Model"),
            ),
        ),
        lib.html.div("Running model...") if loading else None,
        lib.bs.Alert(variant="success", className="mt-3", show=model_results is not None)(
            lib.bs.AlertHeading("Model Results"),
            lib.html.hr(),
            lib.html.div(
                lib.html.pre(model_results),
            )
        ) if model_results else None
    )
