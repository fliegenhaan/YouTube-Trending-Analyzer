from src.data_collector import YouTubeDataCollector
from src.graph_builder import GraphBuilder
from src.analyzer import TrendingAnalyzer
import yaml
import os

def load_config():
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def main():
    # Load configuration
    config = load_config()
    
    # Initialize collector and get data
    collector = YouTubeDataCollector(config['api_key'])
    data = collector.collect_trending_videos(days=14)
    
    if data is not None:
        # Save raw data
        os.makedirs('data/raw', exist_ok=True)
        data.to_csv('data/raw/trending_data.csv', index=False)
        
        # Build graph
        builder = GraphBuilder(data)
        G = builder.build_video_graph()
        
        # Analyze
        analyzer = TrendingAnalyzer(G, data)
        metrics = analyzer.analyze_network()
        patterns = analyzer.analyze_content_patterns()
        
        # Generate report
        analyzer.generate_report(metrics, patterns)
        
if __name__ == "__main__":
    main()