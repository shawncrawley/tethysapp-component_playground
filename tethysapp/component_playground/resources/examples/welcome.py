from tethysapp.component_playground.app import App


@App.page
def welcome(lib):
    return lib.tethys.Display(
        lib.html.h1(f"Welcome!"),
        lib.html.p(
            "Use the code editor on the left to edit the rendered page you see here on the right. Do the same with one of our many examples, found both below and in the top left navigation menu."
        ),
        lib.html.h2("Examples:"),
        *[
            lib.html.div(lib.html.a(href=l["href"])(l["title"]))
            for l in App().example_links()
        ],
    )
