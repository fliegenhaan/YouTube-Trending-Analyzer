import networkx as nx
import pandas as pd
import os
from datetime import datetime
from collections import defaultdict

class TrendingAnalyzer:
    def __init__(self, graph, data):
        self.G = graph
        self.data = data
        
    def analyze_network(self):
        """Perform network analysis"""
        metrics = {
            'num_nodes': self.G.number_of_nodes(),
            'num_edges': self.G.number_of_edges(),
            'density': nx.density(self.G),
            'avg_clustering': nx.average_clustering(self.G),
            'degree_centrality': nx.degree_centrality(self.G),
            'betweenness_centrality': nx.betweenness_centrality(self.G)
        }
        
        # Find communities
        metrics['communities'] = list(nx.community.greedy_modularity_communities(self.G))
        
        return metrics
    
    def analyze_content_patterns(self):
        """Analyze content and category patterns"""
        patterns = {
            'category_distribution': self.data['category_name'].value_counts().to_dict(),
            'channel_videos': self.data['channel_title'].value_counts().to_dict(),
            'daily_trends': self.data.groupby('collection_date').size().to_dict()
        }
        
        return patterns
        
    def generate_report(self, metrics, patterns, output_dir='output/reports'):
        """Generate comprehensive analysis report"""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate report timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(output_dir, f'analysis_report_{timestamp}.txt')

        with open(report_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write("YouTube Trending Analysis Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Network metrics
            f.write("Network Statistics\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total nodes (videos): {metrics['num_nodes']}\n")
            f.write(f"Total edges (relationships): {metrics['num_edges']}\n")
            f.write(f"Graph density: {metrics['density']:.4f}\n")
            f.write(f"Average clustering coefficient: {metrics['avg_clustering']:.4f}\n\n")

            # Most central videos
            f.write("Most Influential Videos (by Degree Centrality)\n")
            f.write("-" * 30 + "\n")
            top_videos = sorted(metrics['degree_centrality'].items(), 
                              key=lambda x: x[1], reverse=True)[:10]
            for video_id, centrality in top_videos:
                video_data = self.data[self.data['video_id'] == video_id].iloc[0]
                f.write(f"Title: {video_data['title']}\n")
                f.write(f"Channel: {video_data['channel_title']}\n")
                f.write(f"Centrality: {centrality:.4f}\n")
                f.write(f"Views: {video_data['view_count']:,}\n\n")

            # Category distribution
            f.write("Category Distribution\n")
            f.write("-" * 30 + "\n")
            for category, count in patterns['category_distribution'].items():
                percentage = (count / sum(patterns['category_distribution'].values())) * 100
                f.write(f"{category}: {count} videos ({percentage:.1f}%)\n")
            f.write("\n")

            # Top channels
            f.write("Most Active Channels\n")
            f.write("-" * 30 + "\n")
            top_channels = sorted(patterns['channel_videos'].items(), 
                                key=lambda x: x[1], reverse=True)[:10]
            for channel, count in top_channels:
                f.write(f"{channel}: {count} videos\n")
            f.write("\n")

            # Daily trends
            f.write("Daily Trending Video Counts\n")
            f.write("-" * 30 + "\n")
            for date, count in sorted(patterns['daily_trends'].items()):
                f.write(f"{date}: {count} videos\n")

            # Community detection results
            f.write("\nCommunity Detection Results\n")
            f.write("-" * 30 + "\n")
            for i, community in enumerate(metrics['communities'], 1):
                f.write(f"Community {i}: {len(community)} videos\n")

        print(f"\nReport generated: {report_file}")

        # Optionally generate additional files for network visualization
        # Save graph data for visualization
        nx.write_gexf(self.G, os.path.join(output_dir, f'network_{timestamp}.gexf'))