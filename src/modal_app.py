import modal
import pathlib
import shlex
import subprocess

GRADIO_PORT = 8000

app = modal.App("gradio-app")

image = modal.Image.debian_slim(python_version="3.11").pip_install("gradio")

fname = "gradio_app.py"
chat_handler_fname = "chat_handler.py"
gradio_script_local_path = pathlib.Path(__file__).parent / fname
chat_handler_local_path = pathlib.Path(__file__).parent / chat_handler_fname
gradio_script_remote_path = pathlib.Path("/root") / fname
chat_handler_remote_path = pathlib.Path("/root") / chat_handler_fname

if not gradio_script_local_path.exists():
    raise RuntimeError(f"{fname} not found! Place the script with your gradio app in the same directory.")
if not chat_handler_local_path.exists():
    raise RuntimeError(f"{chat_handler_fname} not found! Place the script with your gradio app in the same directory.")

image = image.add_local_file(str(gradio_script_local_path), str(gradio_script_remote_path))
image = image.add_local_file(str(chat_handler_local_path), str(chat_handler_remote_path))

@app.function(
    image=image,
    allow_concurrent_inputs=100,  # Ensure we can handle multiple requests
    concurrency_limit=1,  # Ensure all requests end up on the same container
)
@modal.web_server(GRADIO_PORT, startup_timeout=60)
def web_app():
    target = shlex.quote(str(gradio_script_remote_path))
    cmd = f"python {target} --host 0.0.0.0 --port {GRADIO_PORT}"
    subprocess.Popen(cmd, shell=True)

# Run with: modal serve modal_app.py
# Or deploy with: modal deploy modal_app.py