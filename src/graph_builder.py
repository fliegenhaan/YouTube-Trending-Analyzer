import networkx as nx
from collections import defaultdict

class GraphBuilder:
    def __init__(self, data):
        self.data = data
        self.G = nx.Graph()
        
    def build_video_graph(self):
        """Build graph with videos as nodes and relationships as edges"""
        # Add nodes
        for _, video in self.data.iterrows():
            self.G.add_node(video['video_id'],
                           title=video['title'],
                           channel=video['channel_title'],
                           category=video['category_name'],
                           views=video['view_count'])
        
        # Add edges based on relationships
        self._add_channel_relationships()
        self._add_category_relationships()
        self._add_temporal_relationships()
        
        return self.G
    
    def _add_channel_relationships(self):
        """Add edges between videos from same channel"""
        channel_videos = defaultdict(list)
        for _, video in self.data.iterrows():
            channel_videos[video['channel_id']].append(video['video_id'])
            
        for videos in channel_videos.values():
            for i in range(len(videos)):
                for j in range(i + 1, len(videos)):
                    self.G.add_edge(videos[i], videos[j], 
                                  weight=1.0, 
                                  relationship='same_channel')
    
    def _add_category_relationships(self):
        """Add edges between videos in same category"""
        category_videos = defaultdict(list)
        for _, video in self.data.iterrows():
            category_videos[video['category_id']].append(video['video_id'])
            
        for videos in category_videos.values():
            for i in range(len(videos)):
                for j in range(i + 1, len(videos)):
                    self.G.add_edge(videos[i], videos[j],
                                  weight=0.7,
                                  relationship='same_category')
                                  
    def _add_temporal_relationships(self):
        """Add edges between videos trending on same day"""
        date_videos = defaultdict(list)
        for _, video in self.data.iterrows():
            date_videos[video['collection_date']].append(video['video_id'])
            
        for videos in date_videos.values():
            for i in range(len(videos)):
                for j in range(i + 1, len(videos)):
                    self.G.add_edge(videos[i], videos[j],
                                  weight=0.5,
                                  relationship='same_date')