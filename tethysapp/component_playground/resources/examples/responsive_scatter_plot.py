from tethysapp.component_playground.app import App
import json

@App.page
def responsive_scatter_plot(lib):
    lib.register("@nivo/scatterplot", "ns")
    return lib.tethys.Display(
        lib.ns.ResponsiveScatterPlot(
            data=json.loads((lib.hooks.use_resources().path / "data" / "scatter_data.json").read_text()),
            margin=lib.Props(top=60, right=140, bottom=70, left=90),
            axisBottom=lib.Props(legend='weight', legendOffset=46),
            axisLeft=lib.Props(legend='size', legendOffset=-60),
            legends=[
                lib.Props(
                    anchor='bottom-right',
                    direction='column',
                    translateX=130,
                    itemWidth=100,
                    itemHeight=16,
                    itemsSpacing=3,
                    symbolShape='circle'
                )
            ]
        ),
    )
