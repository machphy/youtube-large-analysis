from flask import Flask, render_template, request
from googleapiclient.discovery import build
import re

app = Flask(__name__)

API_KEY = 'AIzaSyD8g7vvAJQ0KCgVM4tjzxDWSXMVVRPT5Ec'  # Replace with your actual API key

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Function to extract channel ID or username from a YouTube URL
def get_channel_id(url):
    try:
        print(f"Processing YouTube URL: {url}")
        channel_id = None

        # Check if the URL contains a channel ID
        if 'youtube.com/channel/' in url:
            match = re.search(r'channel/([^/?&]+)', url)
            if match:
                channel_id = match.group(1)

        # Check if it's a custom URL with username or handle
        elif 'youtube.com/c/' in url or 'youtube.com/user/' in url:
            match = re.search(r'/(c|user)/([^/?&]+)', url)
            if match:
                username = match.group(2)
                print(f"Extracted username: {username}")

                # Fetch the channel ID via username
                response = youtube.channels().list(forUsername=username, part='id').execute()
                if 'items' in response and len(response['items']) > 0:
                    channel_id = response['items'][0]['id']
                else:
                    print("No channel found for the given username.")
        
        # Check for @username handle URLs
        elif 'youtube.com/@' in url:
            match = re.search(r'@([^/?&]+)', url)
            if match:
                handle_name = match.group(1)
                print(f"Extracted handle name: {handle_name}")

                # Search for the channel by handle name using `search.list`
                response = youtube.search().list(part='snippet', q=handle_name, type='channel').execute()
                if 'items' in response and len(response['items']) > 0:
                    channel_id = response['items'][0]['id']['channelId']
                    print(f"Found channel ID from handle: {channel_id}")
                else:
                    print("No channel found for the given handle. Attempting a direct query.")
                    # Fallback to directly querying with the username in the handle
                    channel_response = youtube.channels().list(forUsername=handle_name, part='id').execute()
                    if 'items' in channel_response and len(channel_response['items']) > 0:
                        channel_id = channel_response['items'][0]['id']
                        print(f"Fallback found channel ID: {channel_id}")
                    else:
                        print("Still no channel found for the handle.")
        
        if channel_id:
            print(f"Extracted Channel ID: {channel_id}")
        else:
            print("No valid channel ID or username found.")
        
        return channel_id

    except Exception as e:
        print(f"Error in get_channel_id: {e}")
        return None

# Function to fetch channel details using channel ID
def get_channel_details(channel_id):
    try:
        request = youtube.channels().list(part="snippet,statistics,contentDetails,brandingSettings", id=channel_id)
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            channel_info = response['items'][0]
            details = {
                'title': channel_info['snippet']['title'],
                'description': channel_info['snippet']['description'],
                'profile_image': channel_info['snippet']['thumbnails']['high']['url'],
                'creation_date': channel_info['snippet']['publishedAt'],
                'country': channel_info['snippet'].get('country', 'N/A'),
                'subscribers': channel_info['statistics'].get('subscriberCount', 'N/A'),
                'total_views': channel_info['statistics'].get('viewCount', 'N/A'),
                'total_videos': channel_info['statistics'].get('videoCount', 'N/A')
            }
            return details
        return None
    except Exception as e:
        print(f"Error in get_channel_details: {e}")
        return None

# Route to handle the main page and form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form.get('youtube_url')

        if youtube_url:
            channel_id = get_channel_id(youtube_url)

            if channel_id:
                details = get_channel_details(channel_id)
                if details:
                    return render_template('index.html', details=details)
                else:
                    return render_template('index.html', error="Unable to fetch channel details.")
            else:
                return render_template('index.html', error="Invalid YouTube URL.")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
