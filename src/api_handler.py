import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import logging
import openai
import pandas as pd
from urllib.parse import quote

load_dotenv()
logging.basicConfig(level=logging.INFO)

WP_SITE_URL = os.getenv("WP_SITE_URL")
USERNAME = os.getenv("USERNAME")
APP_PASSWORD = os.getenv("APP_PASSWORD")
auth = HTTPBasicAuth(USERNAME, APP_PASSWORD)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Get the site's metadata like title and excerpt
def get_site_metadata() -> str:
    """Retrieve site metadata."""
    try:
        response = requests.get(f"{WP_SITE_URL}/wp-json/", auth=auth)
        response.raise_for_status()
        metadata = response.json()
        site_info = {
            "Name": metadata.get('name', 'N/A'),
            "Description": metadata.get('description', 'N/A'),
            "URL": metadata.get('url', 'N/A'),
            "Home URL": metadata.get('home', 'N/A'),
            "GMT Offset": metadata.get('gmt_offset', 'N/A'),
            "Timezone": metadata.get('timezone_string', 'N/A'),
            "Authentication": metadata.get('authentication', 'N/A'),
            "Site Icon": metadata.get('site_icon', 'N/A'),
            "Site Icon URL": metadata.get('site_icon_url', 'N/A')
        }
        return "\n".join([f"{key}: {value}" for key, value in site_info.items()])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return f"Error fetching site metadata: {e}"

# Get the metadata for a single post
def get_single_post_metadata(post_title: str) -> str:
    """Retrieve metadata for a specific WordPress post."""
    try:
        response = requests.get(f"{WP_SITE_URL}/wp-json/wp/v2/posts?search={post_title}", auth=auth)
        response.raise_for_status()
        posts = response.json()
        if not posts:
            return f"No post found with the title '{post_title}'."

        post = posts[0]
        return f"Title: {post['title']['rendered']}\nExcerpt: {post['excerpt']['rendered']}"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return f"Error fetching post metadata: {e}"
    
# Get the metadata for a single page
def get_single_page_metadata(page_title: str) -> str:
    """Retrieve metadata for a specific WordPress page."""
    try:
        response = requests.get(f"{WP_SITE_URL}/wp-json/wp/v2/pages?search={page_title}", auth=auth)
        response.raise_for_status()
        pages = response.json()
        if not pages:
            return f"No page found with the title '{page_title}'."

        page = pages[0]
        return f"Title: {page['title']['rendered']}\nExcerpt: {page['excerpt']['rendered']}"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return f"Error fetching page metadata: {e}"

def get_post_id_by_title(post_title: str) -> int:
    """Retrieve a post ID by title."""
    endpoint = f"{WP_SITE_URL}/wp-json/wp/v2/posts?search={post_title}"
    response = requests.get(endpoint, auth=auth)
    response.raise_for_status()
    posts = response.json()
    if not posts:
        raise ValueError(f"No post found with the title '{post_title}'.")
    return posts[0]['id']

def get_yoast_metadata_by_title(post_title: str) -> dict:
    """Fetch Yoast SEO metadata for a post using the title."""
    try:
        post_id = get_post_id_by_title(post_title)
        endpoint = f"{WP_SITE_URL}/wp-json/wp/v2/posts/{post_id}"
        response = requests.get(endpoint, auth=auth)
        response.raise_for_status()
        post_data = response.json()
        return post_data.get('yoast_head_json', {})
    except Exception as e:
        return f"Error fetching Yoast metadata: {str(e)}"
    

def get_yoast_scores(post_title: str) -> str:
    """Fetch Yoast SEO and Readability scores for a given post."""
    try:
        post_id = get_post_id_by_title(post_title)
        endpoint = f"{WP_SITE_URL}/wp-json/wp/v2/posts/{post_id}"
        response = requests.get(endpoint, auth=auth)
        response.raise_for_status()
        post_data = response.json()

        # ✅ Confirming meta fields are included
        seo_score = post_data.get('meta', {}).get('_yoast_wpseo_linkdex', 'N/A')
        readability_score = post_data.get('meta', {}).get('_yoast_wpseo_content_score', 'N/A')
        
        return f"✅ **Yoast SEO Score:** {seo_score}\n✅ **Readability Score:** {readability_score}"
    except Exception as e:
        return f"Error fetching Yoast scores: {str(e)}"
    
def get_all_plugins() -> str:
    """Fetch the list of all plugins in the website."""
    try:
        endpoint = f"{WP_SITE_URL}/wp-json/wp/v2/plugins"
        response = requests.get(endpoint, auth=auth)
        response.raise_for_status()
        plugins = response.json()
        if not plugins:
            return "No plugins found."

        plugin_list = [f"Name: {plugin['name']}, Status: {plugin['status']}" for plugin in plugins]
        return "\n".join(plugin_list)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return f"Error fetching plugins: {e}"
    
def update_plugin(plugin_slug: str) -> str:
    """Update a specific plugin by slug."""
    try:
        endpoint = f"{WP_SITE_URL}/wp-json/wp/v2/plugins/{plugin_slug}"
        response = requests.post(endpoint, auth=auth)
        response.raise_for_status()
        return f"Plugin '{plugin_slug}' updated successfully."
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return f"Error updating plugin '{plugin_slug}': {e}"
    
def export_category_list() -> str:
    """List up to 10 site categories."""
    api_url = f"{WP_SITE_URL}/wp-json/wp/v2/categories"
    per_page = 10  # Limit to 10 categories

    try:
        response = requests.get(api_url, params={'per_page': per_page}, auth=auth)
        response.raise_for_status()
        categories = response.json()

        # Create a list of category names
        category_list = [f"ID: {category['id']}, Name: {category['name']}" for category in categories]
        return "\n".join(category_list)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return f"Error fetching categories: {e}"
    except requests.exceptions.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        return f"JSON decode error: {e}"