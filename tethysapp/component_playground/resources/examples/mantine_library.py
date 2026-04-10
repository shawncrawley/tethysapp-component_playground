from tethysapp.component_playground.app import App


@App.page
def mantine_library(lib):
    value, onChange = lib.hooks.use_state('rgba(47, 119, 150, 0.7)');
    active, setActive = lib.hooks.use_state(0)

    return lib.tethys.Display(
        # Color picker
        lib.m.ColorPicker(format="rgba", value=value, onChange=onChange),
        lib.m.Text(value),

        # Stepper
        lib.m.Stepper(active=active, onStepClick=setActive)(
            lib.m.StepperStep(label="First step", description="Create an account")(
                "Step 1 content: Create an account"
            ),
            lib.m.StepperStep(label="Second step", description="Verify email")(
                "Step 2 content: Verify email"
            ),
            lib.m.StepperStep(label="Final step", description="Get full access")(
                "Step 3 content: Get full access"
            ),
            lib.m.StepperCompleted(
                "Completed, click back button to get to previous step"
            )
        ),
        lib.m.Group(justify="center", mt="xl")(
            lib.m.Button(variant="default", onClick=lambda e: setActive(lambda current: current - 1 if current > 0 else current))(
                "Back"
            ),
            lib.m.Button(onClick=lambda e: setActive(lambda current: current + 1 if current < 3 else current))(
                "Next step"
            )
        ),

        # Pills
        lib.m.InputBase(component="div")(
            lib.m.PillGroup(
                *[
                    lib.m.Pill(key=item, withRemoveButton=True)(
                        f"Item {item}"
                    ) for item in range(10)
                ]
            )
        ),

        # Checkbox
        lib.m.Checkbox(label="I agree to sell my privacy"),

        # Range slider
        lib.m.RangeSlider(
            color="blue",
            defaultValue=[20, 60], 
            marks=[
                lib.Props(value=20, label="20%"), 
                lib.Props(value=50, label="50%"), 
                lib.Props(value=80, label="80%")
            ],
            mb="lg",
        ),

        lib.m.Slider(
            color="blue",
            defaultValue=40,
            marks=[
                lib.Props(value=20, label="20%"), 
                lib.Props(value=50, label="50%"), 
                lib.Props(value=80, label="80%")
            ], 
        )
    )
