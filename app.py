from flask import Flask, render_template, request
from googleapiclient.discovery import build
import re
import csv
from datetime import datetime
import os

app = Flask(__name__)

API_KEY ='AIzaSyD8g7vvAJQ0KCgVM4tjzxDWSXMVVRPT5Ec'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_id(url):
    try:
        channel_id = None
        if 'youtube.com/channel/' in url:
            match = re.search(r'channel/([^/?&]+)', url)
            if match:
                channel_id = match.group(1)
        elif 'youtube.com/c/' in url or 'youtube.com/user/' in url:
            match = re.search(r'/(c|user)/([^/?&]+)', url)
            if match:
                username = match.group(2)
                response = youtube.channels().list(forUsername=username, part='id').execute()
                if 'items' in response and len(response['items']) > 0:
                    channel_id = response['items'][0]['id']
        elif 'youtube.com/@' in url:
            match = re.search(r'@([^/?&]+)', url)
            if match:
                handle_name = match.group(1)
                response = youtube.search().list(part='snippet', q=handle_name, type='channel').execute()
                if 'items' in response and len(response['items']) > 0:
                    channel_id = response['items'][0]['id']['channelId']
        
        return channel_id
    except Exception as e:
        print(f"Error in get_channel_id: {e}")
        return None

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

def get_recent_videos(channel_id):
    try:
        request = youtube.channels().list(part="contentDetails", id=channel_id)
        response = request.execute()
        uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        video_request = youtube.playlistItems().list(part="snippet", playlistId=uploads_playlist_id, maxResults=5)
        video_response = video_request.execute()

        videos = []
        for item in video_response['items']:
            video_details = {
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'published_at': item['snippet']['publishedAt'],
                'video_id': item['snippet']['resourceId']['videoId']
            }
            videos.append(video_details)

        return videos
    except Exception as e:
        print(f"Error in get_recent_videos: {e}")
        return []

def get_trending_videos(country='US'):
    try:
        request = youtube.videos().list(part="snippet,statistics", chart="mostPopular", regionCode=country, maxResults=5)
        response = request.execute()

        trending_videos = []
        for item in response['items']:
            video_details = {
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'views': item['statistics']['viewCount'],
                'video_id': item['id']
            }
            trending_videos.append(video_details)

        return trending_videos
    except Exception as e:
        print(f"Error in get_trending_videos: {e}")
        return []

def save_channel_stats_as_csv(details):
    csv_filename = 'channel_stats.csv'
    try:
        file_exists = os.path.isfile(csv_filename)
        with open(csv_filename, mode='a', newline='') as csv_file:
            fieldnames = ['title', 'description', 'profile_image', 'subscribers', 'total_views', 'total_videos', 'creation_date', 'country', 'date_recorded']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()
            
            details['date_recorded'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(details)
        return csv_filename
    except Exception as e:
        print(f"Error saving CSV: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form.get('youtube_url')

        if youtube_url:
            channel_id = get_channel_id(youtube_url)
            if channel_id:
                details = get_channel_details(channel_id)
                if details:
                    videos = get_recent_videos(channel_id)
                    trending_videos = get_trending_videos()
                    csv_file = save_channel_stats_as_csv(details)
                    return render_template('index.html', details=details, videos=videos, trending_videos=trending_videos, csv_file=csv_file)
                else:
                    return render_template('index.html', error="Unable to fetch channel details.")
            else:
                return render_template('index.html', error="Invalid YouTube URL.")
    trending_videos = get_trending_videos()
    return render_template('index.html', trending_videos=trending_videos)

if __name__ == "__main__":
    app.run(debug=True)
