def detect_intent(message: str) -> str:
    """Detect user intent with support for Yoast score and metadata fetching."""
    message = message.lower().strip()

    # ✅ Detect Yoast score fetching explicitly
    # if message.startswith("fetch yoast score for"):
    #     return "fetch_yoast_score"

    # ✅ Detect Yoast metadata fetching (separate from score)
    if message.startswith("fetch yoast for"):
        return "yoast_metadata"
    
    elif message.startswith("get plugin list"):
        return "plugin_list"
    
    elif message.startswith("export category list"):
        return "export_categories"    

    # ✅ Broader keyword checks for other intents
    site_metadata_keywords = ["site information", "site metadata", "site info", "website details"]
    post_metadata_keywords = ["post metadata", "post info", "post details"]
    yoast_score_keywords = ["fetch yoast score for", "yoast score", "what is yoast score"]
    create_post_keywords = ["create a post"]

    if any(keyword in message for keyword in site_metadata_keywords):
        return "fetch_site_metadata"
    
    elif any(keyword in message for keyword in post_metadata_keywords):
        return "fetch_post_metadata"
    
    elif any(keyword in message for keyword in yoast_score_keywords):
        return "fetch_yoast_score"
    
    elif any(keyword in message for keyword in create_post_keywords):
        return "create_post"    

    # ✅ Default fallback for unmatched intents
    return "general"