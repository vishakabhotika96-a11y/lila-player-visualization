# Lila Player Visualization

## What the Tool Does

This is a Streamlit web application for gaming analytics that visualizes player journeys from PUBG-like game data. It loads player movement data from parquet files, displays minimaps, plots player positions, distinguishes between human and bot players, and provides interactive filters and heatmaps for analyzing gameplay events.

## How to Run It

1. Ensure you have Python 3.8+ installed.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
4. Open your browser and navigate to the local URL (usually `http://localhost:8501`).

## Tech Stack Used

- **Python**: Core programming language
- **Streamlit**: Web app framework for building interactive dashboards
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive plotting and visualization
- **Matplotlib & Seaborn**: Additional plotting libraries
- **PIL (Pillow)**: Image processing for minimap display
- **NumPy**: Numerical computations

## Deployment Link

The app is currently deployed locally. For production deployment, consider using Streamlit Cloud, Heroku, or AWS. [Deployment Link Placeholder]

## Features

- Loads all parquet files from the `player_data/` directory
- Interactive map and match filters
- Displays minimap images for selected maps
- Plots player movement using x and z coordinates
- Distinguishes between human players (UUID user_id) and bots (numeric user_id)
- Shows event markers for Kill, Killed, BotKill, BotKilled, Loot, and KilledByStorm
- Includes a heatmap for movement, deaths, and kills
- Simple timeline slider for filtering data by time range
