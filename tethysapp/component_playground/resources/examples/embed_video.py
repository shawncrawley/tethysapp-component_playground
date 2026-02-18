from tethysapp.component_playground.app import App


@App.page
def embed_video(lib):
    return lib.tethys.Display(
        # See https://www.npmjs.com/package/react-player for API that can be Pythonified here
        lib.rp.ReactPlayer(
            src="https://www.youtube.com/watch?v=RCeC_zQo2u4",
            height="100%",
            width="100%",
            onReady=lambda: print(
                "Check your server console for this message indicating that your video is ready to play."
            ),
        )
    )
