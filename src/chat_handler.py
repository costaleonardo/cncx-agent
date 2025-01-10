import openai
import urllib.parse

from api_handler import (
    get_site_metadata, 
    get_single_post_metadata, 
    get_yoast_metadata_by_title,
    get_yoast_scores,
    get_all_plugins,
    update_plugin,
    export_category_list
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
        post_title = extract_title("fetch yoast score for", message)
        response = get_yoast_scores(post_title) if post_title else "Error: Please specify a valid post title."

    elif intent == "yoast_metadata":
        post_title = extract_title("fetch yoast for", message)
        response = get_yoast_metadata_by_title(post_title) if post_title else "Error: Please specify a valid post title."

    elif intent == "plugin_list":
        response = get_all_plugins()

    elif intent == "export_categories":
        response = export_category_list()

    else:
        try:
            openai_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful WordPress assistant."},
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