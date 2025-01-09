import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

WP_SITE_URL = os.getenv("WP_SITE_URL")
USERNAME = os.getenv("USERNAME")
APP_PASSWORD = os.getenv("APP_PASSWORD")
auth = HTTPBasicAuth(USERNAME, APP_PASSWORD)

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
            "Home URL": metadata.get('home', 'N/A')
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

# First commit!s
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
    
# @TODO - Get Plugin List: Fetch the list of all plugin in the website.