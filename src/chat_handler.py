import openai
import urllib.parse
from agent_details import agent_details

from api_handler import (
    get_site_metadata, 
    get_single_post_metadata, 
    get_yoast_metadata_by_title,
    get_yoast_scores,
    get_all_plugins,
    update_plugin,
    create_post
)
from intent_detection import detect_intent

def chat_response(message: str, history: list):
    """Chat Handling with Correct Post Title Extraction for Yoast SEO and Scores."""
    intent = detect_intent(message)

    # ✅ Standardize Post Title Cleaning Using a Helper Function
    def extract_title(intent_key, message):
        return message.lower().replace(intent_key, "").strip()

    if intent == "fetch_site_metadata":
        response = get_site_metadata()

    elif intent == "fetch_post_metadata":
        response = "Please provide the post title to fetch post metadata."

    elif intent == "fetch_yoast_score":
        post_title = extract_title("what is the yoast score for", message)
        response = get_yoast_scores(post_title) if post_title else "Error: Please specify a valid post title."

    elif intent == "yoast_metadata":
        post_title = extract_title("fetch yoast for", message)
        response = get_yoast_metadata_by_title(post_title) if post_title else "Error: Please specify a valid post title."

    elif intent == "plugin_list":
        response = get_all_plugins()

    elif intent == "create_post":
        post_title = extract_title("create a post titled", message)
        post_content = message.split("with content", 1)[-1].strip() if "with content" in message else ""
        
        if post_title and post_content:
            response = create_post(post_title, post_content)
        else:
            response = "Error: Please specify both a valid post title and content."
        response = create_post(post_title, post_content, status="draft");        

    else:
        try:
            openai_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": agent_details
                    },
                    {"role": "user", "content": message}
                ]
            )
            response = openai_response['choices'][0]['message']['content'].strip()
        except Exception as e:
            response = f"Error with OpenAI API: {str(e)}"

    # ✅ Update Chat History
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})
    return history, history

def clear_chat():
    """Clear the chat history."""
    return [], []