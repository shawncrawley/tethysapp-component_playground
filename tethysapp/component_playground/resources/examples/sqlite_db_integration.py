import pandas as pd
import sqlite3
from uuid import uuid4
from pathlib import Path

from tethys_sdk.components.utils import event
from tethysapp.component_playground.app import App

def data_to_sqlite(db_fpath, data):
    # Convert to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Create a SQLite database and a table in memory or a file
    # Use ':memory:' for an in-memory database (deleted when the connection closes)
    # Or specify a file path (e.g., 'my_database.db') for a persistent database
    conn = sqlite3.connect(db_fpath) # or 'my_database.db'

    # Use the to_sql method to write records to a SQL database
    # if_exists='replace' will drop the table if it already exists and create a new one
    # if_exists='append' will add the data to the existing table without dropping it
    # index=False prevents pandas from writing the DataFrame index as a column
    df.to_sql('example', conn, if_exists='replace', index=False)

    # Optional: Verify the data was loaded correctly
    print("Data loaded into SQLite database 'example' table.")
    print("Querying the table:")
    query_df = pd.read_sql_query("SELECT * FROM example", conn)
    print(query_df)

    # Close the connection
    conn.close()

def data_from_sqlite(db_fpath):
    # Connect to the SQLite database
    with sqlite3.connect(db_fpath) as conn:
        # Query the data from the 'example' table
        query_df = pd.read_sql_query("SELECT * FROM example", conn)

    # Convert the DataFrame back to a list of dictionaries
    data = query_df.to_dict(orient='records')

    return data

@App.page
def sqlite_db_integration(lib):
    lib.register('react-tabs', 'tabs', styles=['https://esm.sh/react-tabs@6.1.0/style/react-tabs.css'])
    # The use_workspace hook provides access to the app's workspace, which is a Tethys-managed directory on the server 
    # where you can read/write files. We'll use this location to store our sqlite database file.
    displayed_data, set_displayed_data = lib.hooks.use_state([])
    submit_success, set_submit_success = lib.hooks.use_state(None)
    formKey, setFormKey = lib.hooks.use_state(str(uuid4())) # This is used to reset the form after submission by changing the key
    app_workspace = lib.hooks.use_workspace()

    if app_workspace.checking_quota:
        return lib.html.h1("Checking workspace quota...")
    elif app_workspace.quota_exceeded:
        return lib.html.h1("Workspace quota exceeded.")

    # Reaching this point means that the workspace is ready to use, so we can proceed with 
    # reading/writing the sqlite database file.
    db_fpath = Path(app_workspace.path) / "my_database.sqlite"

    def handle_submit(e):
        form_data = e["formData"] # This is the form data as a JSON string
        data_to_sqlite(db_fpath, [form_data]) # Load the form data into the SQLite database
        set_submit_success(True) # Show success message
        setFormKey(str(uuid4())) # Reset the form by changing its key, which forces it to remount
        lib.utils.background_execute(lambda: set_submit_success(None), delay_seconds=3) # Hide success message after 3 seconds

    return lib.tethys.Display(
        lib.tabs.Tabs(
            lib.tabs.TabList(
                lib.tabs.Tab("Add Data"),
                lib.tabs.Tab("View Data"),
            ),
            lib.tabs.TabPanel(
                lib.bs.Form(key=formKey, onSubmit=event(handle_submit, prevent_default=True, stop_propagation=True))(
                    lib.bs.FormGroup(className="mb-3")(
                        lib.bs.FormLabel("Name"),
                        lib.bs.FormControl(type="text", name="name", placeholder="Enter name here"),
                    ),
                    lib.bs.FormGroup(className="mb-3")(
                        lib.bs.FormLabel("Age"),
                        lib.bs.FormControl(type="number", name="age", placeholder="Enter age here"),
                    ),
                    lib.bs.FormGroup(className="mb-3")(
                        lib.bs.FormLabel("Image"),
                        lib.bs.FormControl(type="file", name="image", accept="image/*", capture="environment"),
                    ),
                    lib.bs.Button(type="submit", variant="primary")("Add"),
                    lib.bs.Alert(variant="success")("Form submitted successfully!") if submit_success else None,
                )
            ),
            lib.tabs.TabPanel(
                lib.bs.Button(disabled=not db_fpath.exists(), onClick=lambda _: set_displayed_data(data_from_sqlite(db_fpath)))(f"{'Load' if not displayed_data else 'Reload'} Data from SQLite Database"),
                lib.html.div(
                    lib.html.pre(str(displayed_data)) if displayed_data else None,
                ) if displayed_data else lib.html.div("No data to display. Please add some data in the 'Add Data' tab and submit the form.")
            )
        )
    )
