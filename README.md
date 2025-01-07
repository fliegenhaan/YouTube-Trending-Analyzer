# YouTube Trending Analyzer

This project analyzes YouTube trending videos in Indonesia using a graph theory approach. The analysis includes content relationships, category distribution, and temporal patterns.

## Prerequisites

- **Python** 3.9+
- **Google Cloud** account with YouTube Data API v3 enabled
- **Gephi** 0.10.1

## Required Python Libraries

Install the required libraries using the following command:

```bash
pip install google-api-python-client pandas networkx numpy pyyaml
```
## Project Structure
```bash
youtube_trending_analysis/
├── src/
│   ├── data_collector.py    # YouTube data collection
│   ├── graph_builder.py     # Graph construction
│   └── analyzer.py          # Analysis implementation
├── data/
│   └── raw/                 # Raw collected data
├── output/
│   ├── graphs/              # Generated graph files
│   └── reports/             # Analysis reports
├── config/
│   └── config.yaml          # Configuration file
└── main.py                  # Main execution script
```
## Setup
1. Create a Google Cloud Project and enable YouTube Data API v3.
2. Create API credentials (API key).
3. Add your API key to the config/config.yaml file:
```bash
api_key: "YOUR_API_KEY_HERE"
```
## Running the Analysis
Execute the main script:
```bash
python main.py
```
Check output files:
* Raw data: data/raw/trending_data.csv
* Analysis report: output/reports/analysis_report_[timestamp].txt
* Network visualization: output/graphs/network_[timestamp].gexf
## Visualization in Gephi
1. Import the .gexf file into Gephi.
2. Apply the **ForceAtlas 2** layout with the following settings:
  - **Scaling**: 2.0
  - **Gravity**: 5.0
  - Enable **LinLog mode** and **Prevent Overlap**.
3. Configure node and edge appearances:
  - **Node Size**: By degree (Min: 10, Max: 30)
  - **Node Color**: By category.
  - **Edge Weight**: 0.1 - 1.0 with curved edges.
4. Generate visualizations and export.
## Analysis Reports
The analysis generates the following insights:
- **Network statistics**: Node degree, clustering coefficient, etc.
- **Content category distribution**: Insights into trending video categories.
- **Channel performance metrics**: Identification of high-performing channels.
- **Community detection results**: Grouping of related content.
- **Temporal patterns**: Trends over time.
