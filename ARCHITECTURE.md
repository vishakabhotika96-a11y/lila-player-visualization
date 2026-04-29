# Architecture

```
Raw parquet files
↓
Python reads them
↓
Events are decoded
↓
Coordinates are converted to pixels
↓
Streamlit shows them on minimap
```

## Flow Explanation

1. **Raw Parquet Files**: These are compressed, columnar data files containing player journey data from the game, including user IDs, match IDs, map IDs, coordinates (x, y, z), timestamps, and events stored as bytes.

2. **Python Reads Them**: Using the Pandas library in Python, the application loads all parquet files from the `player_data/` directory, concatenates them into a single DataFrame for efficient data manipulation and analysis.

3. **Events Are Decoded**: The 'event' column, stored as bytes, is decoded into readable strings (e.g., 'Kill', 'Loot') to allow for proper filtering and visualization of gameplay events.

4. **Coordinates Are Converted to Pixels**: The in-game world coordinates (x, z) are transformed into pixel coordinates that correspond to the minimap image dimensions, ensuring accurate positioning of player movements and events on the visual map.

5. **Streamlit Shows Them on Minimap**: The Streamlit web framework renders an interactive dashboard displaying the minimap image with overlaid player positions, movement paths, event markers, and heatmaps, providing an intuitive interface for gaming analytics.
