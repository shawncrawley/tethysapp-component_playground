from tethysapp.component_playground.app import App


@App.page
def reactive_table(lib):
    row_data, set_row_data = lib.hooks.use_state(
        [
            {"make": "Tesla", "model": "Model Y", "price": 64950, "electric": True},
            {"make": "Ford", "model": "F-Series", "price": 33850, "electric": True},
            {"make": "Toyota", "model": "Corolla", "price": 29600, "electric": True},
            {"make": "Mercedes", "model": "EQA", "price": 48890, "electric": True},
            {"make": "Fiat", "model": "500", "price": 15774, "electric": True},
            {"make": "Nissan", "model": "Juke", "price": 20675, "electric": True},
        ]
    )

    # Column Definitions: Defines & controls grid columns.
    col_defs, set_col_defs = lib.hooks.use_state(
        [
            {"field": "make"},
            {"field": "model"},
            {"field": "price"},
            {"field": "electric"},
        ]
    )

    default_col_def = lib.Props(flex=1)

    # Container: Defines the grid's theme & dimensions.
    return lib.html.div(style=lib.Style(height="500px"))(
        lib.ag.AgGridReact(
            rowData=row_data,
            columnDefs=col_defs,
            defaultColDef=default_col_def,
        )
    )
