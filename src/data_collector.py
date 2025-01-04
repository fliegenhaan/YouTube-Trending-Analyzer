# src/data_collector.py
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd

class YouTubeDataCollector:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
    def get_category_names(self):
        try:
            request = self.youtube.videoCategories().list(
                part='snippet',
                regionCode='ID'
            )
            response = request.execute()
            return {item['id']: item['snippet']['title'] 
                   for item in response['items']}
        except Exception as e:
            print(f"Error fetching categories: {str(e)}")
            return {}

    def collect_trending_videos(self, days=14):
        # Collect trending videos for specified number of days
        all_data = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        categories = self.get_category_names()
        
        current_date = start_date
        while current_date <= end_date:
            try:
                videos = self._get_daily_trending(categories)
                if videos:
                    df = pd.DataFrame(videos)
                    df['collection_date'] = current_date.date()
                    all_data.append(df)
            except Exception as e:
                print(f"Error collecting data for {current_date.date()}: {str(e)}")
            current_date += timedelta(days=1)
            
        return pd.concat(all_data, ignore_index=True) if all_data else None

    def _get_daily_trending(self, categories, max_results=50):
        request = self.youtube.videos().list(
            part='snippet,statistics,contentDetails',
            chart='mostPopular',
            regionCode='ID',
            maxResults=max_results
        )
        response = request.execute()
        
        return [{
            'video_id': item['id'],
            'title': item['snippet']['title'],
            'channel_id': item['snippet']['channelId'],
            'channel_title': item['snippet']['channelTitle'],
            'category_id': item['snippet']['categoryId'],
            'category_name': categories.get(item['snippet']['categoryId'], 'Unknown'),
            'view_count': int(item['statistics']['viewCount']),
            'like_count': int(item['statistics'].get('likeCount', 0)),
            'comment_count': int(item['statistics'].get('commentCount', 0)),
            'publish_time': item['snippet']['publishedAt']
        } for item in response['items']]