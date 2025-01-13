from fastapi import FastAPI
import gradio as gr
import time
from gradio.routes import mount_gradio_app
from chat_handler import chat_response, clear_chat

def build_interface():
    with gr.Blocks() as iface:
        gr.Markdown("## CNCX Marketing Agent")
        chatbot = gr.Chatbot(label="Chat with CNXC Agent", type="messages")
        msg = gr.Textbox(placeholder="Type your message here...")
        state = gr.State([])

        # Bind Chat Interaction
        def chat_response_and_clear(message, state):
            response, new_state = chat_response(message, state)
            return response, new_state, gr.update(value='')

        msg.submit(chat_response_and_clear, [msg, state], [chatbot, state, msg])
        gr.Button("Clear Chat").click(clear_chat, inputs=[], outputs=[chatbot, state])

    return iface

demo = build_interface()
demo.queue(max_size=5)  # Enable queue for handling multiple requests

web_app = FastAPI()
app = mount_gradio_app(
    app=web_app,
    blocks=demo,
    path="/",
)

if __name__ == "__main__":
    import argparse
    import uvicorn
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str)
    parser.add_argument("--port", type=int)
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)