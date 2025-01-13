import gradio as gr
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

if __name__ == "__main__":
    build_interface().launch()