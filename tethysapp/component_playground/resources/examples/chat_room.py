from tethysapp.component_playground.app import App
import asyncio

@App.page
def chat_room(lib):
    user = lib.hooks.use_user()
    messages, set_messages = lib.hooks.use_state([])
    input_text, set_input_text = lib.hooks.use_state("")
    
    async def receive_message(message):
        set_messages(lambda _messages: _messages + [(message["user"], message["text"])])

    def send_message(e):
        if e["key"] == "Enter":
            set_input_text("")
            asyncio.create_task(
                sender(
                    lib.Props(
                        text=e["target"]["value"],
                        user=user,
                    )
                )
            )
            
    sender = lib.hooks.use_channel_layer(group_name="my-channel-name", receiver=receive_message)
    
    return lib.html.div(
        *[lib.html.div(lib.html.b(u), ": ", m) for u, m in messages],
        lib.html.br(),
        "Send: ",
        lib.html.input(
            key="input",  # Ensures the input is not recreated each time, since its rendering order will change based on the numebr of messages above
            type="text", 
            value=input_text, 
            onKeyDown=send_message,
            onChange=lambda e: set_input_text(e.target.value)
        ),
    )
