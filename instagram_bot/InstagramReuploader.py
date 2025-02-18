import instaloader
import os
import requests
import time

# --- Configuration ---
USERNAME = "your_instagram_username"
PASSWORD = "your_instagram_password"  # Optional: Can be manually entered during first login
SESSION_FILE = f"{USERNAME}_session"

TARGET_USERNAME = "target_instagram_account"  # Account whose posts you want to download
ACCESS_TOKEN = "your_instagram_api_access_token"  # Required for reuploading
INSTAGRAM_ACCOUNT_ID = "your_instagram_business_account_id"  # Needed for uploads


# --- Step 1: Authenticate & Load Session ---
def login_with_session():
    L = instaloader.Instaloader()

    # Try loading session
    try:
        L.load_session_from_file(USERNAME, SESSION_FILE)
        print("✅ Loaded session successfully!")
    except FileNotFoundError:
        print("🔄 Session not found. Logging in...")
        L.login(USERNAME, PASSWORD)
        L.save_session_to_file(SESSION_FILE)  # Save session for future logins
        print("✅ Session saved!")

    return L


# --- Step 2: Download Latest Post ---
def download_latest_post(L):
    profile = instaloader.Profile.from_username(L.context, TARGET_USERNAME)
    
    for post in profile.get_posts():
        L.download_post(post, target="latest_post")
        return post  # Stop after the first (latest) post
    
    return None


# --- Step 3: Extract Caption & File Path ---
def get_latest_post_details():
    files = os.listdir("latest_post")
    media_files = sorted([f for f in files if f.endswith((".jpg", ".mp4"))])
    txt_files = [f for f in files if f.endswith(".txt")]

    if not media_files or not txt_files:
        return None, None

    media_file = os.path.join("latest_post", media_files[0])

    # Extract caption
    with open(os.path.join("latest_post", txt_files[0]), "r", encoding="utf-8") as file:
        caption = file.read().split("\n")[0]  # First line as caption

    return media_file, caption


# --- Step 4: Upload to Instagram ---
def upload_to_instagram(media_file, caption):
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
    media_type = "IMAGE" if media_file.endswith(".jpg") else "VIDEO"

    files = {'file': open(media_file, 'rb')}
    data = {
        'access_token': ACCESS_TOKEN,
        'caption': caption,
        'media_type': media_type
    }

    response = requests.post(url, files=files, data=data)
    response_data = response.json()
    
    if "id" in response_data:
        print("✅ Media Uploaded Successfully:", response_data)
        
        # Publish the media
        publish_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
        publish_data = {'access_token': ACCESS_TOKEN, 'creation_id': response_data["id"]}
        publish_response = requests.post(publish_url, data=publish_data)
        
        print("📢 Publish Response:", publish_response.json())
    else:
        print("❌ Upload Failed:", response_data)


# --- Step 5: Automate the Full Process ---
def run_bot():
    L = login_with_session()
    print("🔄 Downloading latest post...")
    
    latest_post = download_latest_post(L)
    if latest_post:
        print("✅ Downloaded:", latest_post.url)
        
        media_file, caption = get_latest_post_details()
        if media_file:
            print("📤 Uploading to Instagram...")
            upload_to_instagram(media_file, caption)
        else:
            print("❌ No valid media file found!")
    else:
        print("❌ No posts found!")


if __name__ == "__main__":
    run_bot()
