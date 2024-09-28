from flask import Flask, render_template, request, jsonify, url_for
from googleapiclient.discovery import build
import re
import os
import matplotlib.pyplot as plt
from textblob import TextBlob  # Ensure you have this library for sentiment analysis

app = Flask(__name__)

API_KEY = 'AIzaSyD8g7vvAJQ0KCgVM4tjzxDWSXMVVRPT5Ec'
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Ensure static folder exists
if not os.path.exists('static'):
    os.makedirs('static')

channels_data = {}

def get_channel_id(url):
    try:
        if 'youtube.com/channel/' in url:
            match = re.search(r'channel/([^/?&]+)', url)
            return match.group(1) if match else None
        elif 'youtube.com/c/' in url or 'youtube.com/user/' in url:
            match = re.search(r'/(c|user)/([^/?&]+)', url)
            if match:
                username = match.group(2)
                response = youtube.channels().list(forUsername=username, part='id').execute()
                return response['items'][0]['id'] if 'items' in response and len(response['items']) > 0 else None
        elif 'youtube.com/@' in url:
            match = re.search(r'@([^/?&]+)', url)
            if match:
                handle_name = match.group(1)
                response = youtube.search().list(part='snippet', q=handle_name, type='channel').execute()
                return response['items'][0]['id']['channelId'] if 'items' in response and len(response['items']) > 0 else None
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
                'subscribers': int(channel_info['statistics'].get('subscriberCount', 0)),
                'total_views': int(channel_info['statistics'].get('viewCount', 0)),
                'total_videos': int(channel_info['statistics'].get('videoCount', 0))
            }
            channels_data[channel_id] = details
            return details
    except Exception as e:
        print(f"Error in get_channel_details: {e}")
    return None

def get_recent_videos(channel_id):
    try:
        request = youtube.channels().list(part="contentDetails", id=channel_id)
        response = request.execute()
        uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        video_request = youtube.playlistItems().list(part="snippet", playlistId=uploads_playlist_id, maxResults=50)
        video_response = video_request.execute()

        videos = []
        for item in video_response['items']:
            video_details = {
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'published_at': item['snippet']['publishedAt'],
                'video_id': item['snippet']['resourceId']['videoId'],
            }
            video_stats = youtube.videos().list(part='statistics', id=video_details['video_id']).execute()
            video_details['views'] = int(video_stats['items'][0]['statistics'].get('viewCount', 0))
            video_details['likes'] = int(video_stats['items'][0]['statistics'].get('likeCount', 0))

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
                'views': int(item['statistics']['viewCount']),
                'video_id': item['id']
            }
            trending_videos.append(video_details)

        return trending_videos
    except Exception as e:
        print(f"Error in get_trending_videos: {e}")
    return []

def analyze_comments(video_id):
    try:
        comments = []
        next_page_token = None
        
        while True:
            comment_request = youtube.commentThreads().list(part='snippet', videoId=video_id, textFormat='plainText', pageToken=next_page_token).execute()
            for item in comment_request['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
            next_page_token = comment_request.get('nextPageToken')
            if not next_page_token:
                break

        sentiment_data = {'positive': 0, 'negative': 0, 'neutral': 0}
        for comment in comments:
            analysis = TextBlob(comment)
            if analysis.sentiment.polarity > 0:
                sentiment_data['positive'] += 1
            elif analysis.sentiment.polarity < 0:
                sentiment_data['negative'] += 1
            else:
                sentiment_data['neutral'] += 1

        # Create a pie chart for sentiment analysis
        create_sentiment_chart(sentiment_data)

        return sentiment_data
    except Exception as e:
        print(f"Error in analyze_comments: {e}")
    return {'positive': 0, 'negative': 0, 'neutral': 0}

def create_sentiment_chart(sentiment_data):
    labels = list(sentiment_data.keys())
    sizes = list(sentiment_data.values())
    
    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the figure
    plt.title('Sentiment Analysis of Comments')
    image_path = os.path.join('static', 'sentiment_chart.png')  # Ensure this path exists
    plt.savefig('static/sentiment_chart.png')
    plt.close()
    
    print(f"Chart saved at: {image_path}")  # Debugging line

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    platform = request.form.get('platform')
    video_link = request.form.get('video_link')

    if platform == 'youtube':
        video_id = extract_video_id(video_link)
        if video_id:
            sentiment_data = analyze_comments(video_id)

            return jsonify({
                'sentiment_data': sentiment_data,
                'sentiment_chart_url': url_for('static', filename='sentiment_chart.png')
            })
        else:
            return jsonify({'error': 'Invalid YouTube video URL'}), 400

    return jsonify({'error': 'Invalid platform selected'}), 400

def extract_video_id(video_url):
    match = re.search(r'(?<=v=)[^&]+', video_url)
    return match.group(0) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    details = None
    videos = []
    trending_videos = []
    most_viewed_video = None
    most_liked_video = None
    error = None

    if request.method == 'POST':
        youtube_url = request.form.get('youtube_url')

        if youtube_url:
            channel_id = get_channel_id(youtube_url)
            if channel_id:
                details = get_channel_details(channel_id)
                if details:
                    videos = get_recent_videos(channel_id)
                    trending_videos = get_trending_videos()

                    if videos:
                        most_viewed_video = max(videos, key=lambda v: v['views'])
                        most_liked_video = max(videos, key=lambda v: v['likes'])

                else:
                    error = "Unable to fetch channel details."
            else:
                error = "Invalid YouTube URL."

    trending_videos = get_trending_videos()
    return render_template('index.html', details=details, videos=videos, trending_videos=trending_videos, most_viewed_video=most_viewed_video, most_liked_video=most_liked_video, error=error)

if __name__ == '__main__':
    app.run(debug=True)
