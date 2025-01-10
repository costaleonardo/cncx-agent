import gradio as gr
from chat_handler import chat_response, clear_chat

def build_interface():
    with gr.Blocks() as iface:
        gr.Markdown("## CNCX Marketing Agent")
        chatbot = gr.Chatbot(label="Chat with CNXC Agent", type="messages")
        msg = gr.Textbox(placeholder="Type your message here...")
        state = gr.State([])

        # Bind Chat Interaction
        msg.submit(chat_response, [msg, state], [chatbot, state])
        gr.Button("Clear Chat").click(clear_chat, inputs=[], outputs=[chatbot, state])

    return iface

if __name__ == "__main__":
    build_interface().launch()