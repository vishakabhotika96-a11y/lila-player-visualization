import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import glob
from PIL import Image

# Set page config
st.set_page_config(page_title="Gaming Analytics Dashboard", layout="wide")

# Cache data loading
@st.cache_data
def load_data():
    """Load all parquet files from player_data directory"""
    data_path = Path("player_data")
    all_files = list(data_path.rglob("*.nakama-0"))

    dfs = []
    for file in all_files:
        try:
            df = pd.read_parquet(file)
            dfs.append(df)
        except Exception as e:
            st.warning(f"Error loading {file}: {e}")
            continue

    if not dfs:
        st.error("No data files found!")
        return pd.DataFrame()

    combined_df = pd.concat(dfs, ignore_index=True)

    # Decode event bytes
    combined_df['event'] = combined_df['event'].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

    # Add player type
    combined_df['player_type'] = combined_df['user_id'].apply(lambda x: 'Human' if '-' in str(x) else 'Bot')

    # Sort by timestamp
    combined_df = combined_df.sort_values('ts')

    return combined_df

# Load data
df = load_data()

if df.empty:
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

# Map filter
available_maps = sorted(df['map_id'].unique())
selected_map = st.sidebar.selectbox("Select Map", available_maps)

# Match filter
map_data = df[df['map_id'] == selected_map]
available_matches = sorted(map_data['match_id'].unique())
selected_match = st.sidebar.selectbox("Select Match", available_matches)

# Filter data
filtered_data = map_data[map_data['match_id'] == selected_match]

# Timeline slider
if not filtered_data.empty:
    min_time = filtered_data['ts'].min()
    max_time = filtered_data['ts'].max()
    time_range = st.sidebar.slider(
        "Time Range",
        min_value=min_time.to_pydatetime(),
        max_value=max_time.to_pydatetime(),
        value=(min_time.to_pydatetime(), max_time.to_pydatetime())
    )

    # Filter by time
    filtered_data = filtered_data[
        (filtered_data['ts'] >= time_range[0]) &
        (filtered_data['ts'] <= time_range[1])
    ]

# Main content
st.title("Gaming Analytics Dashboard")

# Display minimap
st.header("Minimap")
minimap_path_png = f"minimaps/{selected_map}_Minimap.png"
minimap_path_jpg = f"minimaps/{selected_map}_Minimap.jpg"
if Path(minimap_path_png).exists():
    minimap_image = Image.open(minimap_path_png)
    st.image(minimap_image, caption=f"{selected_map} Minimap", width='stretch')
elif Path(minimap_path_jpg).exists():
    minimap_image = Image.open(minimap_path_jpg)
    st.image(minimap_image, caption=f"{selected_map} Minimap", width='stretch')
else:
    st.warning("Minimap image not found")

# Player movement plot
st.header("Player Movement")

if not filtered_data.empty:
    # Create scatter plot with plotly for interactivity
    fig = px.scatter(
        filtered_data,
        x='x',
        y='z',
        color='player_type',
        color_discrete_map={'Human': 'blue', 'Bot': 'red'},
        title="Player Positions",
        labels={'x': 'X Coordinate', 'z': 'Z Coordinate'},
        hover_data=['user_id', 'event', 'ts']
    )

    # Add event markers
    event_colors = {
        'Kill': 'red',
        'Killed': 'darkred',
        'BotKill': 'orange',
        'BotKilled': 'darkorange',
        'Loot': 'green',
        'KilledByStorm': 'purple'
    }

    for event_type, color in event_colors.items():
        event_data = filtered_data[filtered_data['event'] == event_type]
        if not event_data.empty:
            fig.add_trace(go.Scatter(
                x=event_data['x'],
                y=event_data['z'],
                mode='markers',
                marker=dict(color=color, size=10, symbol='x'),
                name=event_type,
                hovertemplate=f'{event_type}<br>X: %{{x}}<br>Z: %{{y}}<br>User: %{{customdata}}',
                customdata=event_data['user_id']
            ))

    fig.update_layout(
        xaxis_title="X Coordinate",
        yaxis_title="Z Coordinate",
        height=600
    )

    st.plotly_chart(fig, width='stretch')

    # Heatmap
    st.header("Movement Heatmap")

    # Create heatmap using seaborn
    fig, ax = plt.subplots(figsize=(10, 8))

    # Combine data for easier plotting
    plot_data = filtered_data.copy()

    # Create KDE plot with hue
    sns.kdeplot(data=plot_data, x='x', y='z', hue='player_type', fill=True, alpha=0.6, ax=ax, palette={'Human': 'blue', 'Bot': 'red'})

    ax.set_title("Player Movement Density")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Z Coordinate")

    st.pyplot(fig)

    # Statistics
    st.header("Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Players", len(filtered_data['user_id'].unique()))

    with col2:
        human_count = len(filtered_data[filtered_data['player_type'] == 'Human']['user_id'].unique())
        st.metric("Human Players", human_count)

    with col3:
        bot_count = len(filtered_data[filtered_data['player_type'] == 'Bot']['user_id'].unique())
        st.metric("Bot Players", bot_count)

    # Event summary
    st.subheader("Event Summary")
    event_counts = filtered_data['event'].value_counts()
    st.bar_chart(event_counts)

else:
    st.warning("No data available for the selected filters")
