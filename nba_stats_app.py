import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import PlayerCareerStats

def get_player_stats(player_name):
    # Search for player
    player = players.find_players_by_full_name(player_name)
    if not player:
        return None, "Player not found. Check the name and try again."
    
    player_id = player[0]['id']
    
    # Fetch career stats
    career_stats = PlayerCareerStats(player_id=player_id)
    stats_df = career_stats.get_data_frames()[0]
    
    # Get the latest season stats
    latest_season_stats = stats_df.iloc[-1]

    # Extract points, rebounds, and assists per game
    stats = {
        "Points per Game": latest_season_stats['PTS'],
        "Rebounds per Game": latest_season_stats['REB'],
        "Assists per Game": latest_season_stats['AST']
    }
    
    return stats, None

# Streamlit app setup
st.title("NBA Player Stats Viewer")
st.header("Get Points, Rebounds, and Assists per Game")

# Player input
player_name = st.text_input("Enter the player's full name (e.g., LeBron James)")

if st.button("Get Stats"):
    if player_name.strip():
        stats, error = get_player_stats(player_name)
        
        if error:
            st.error(error)
        else:
            st.success(f"Stats for {player_name}:")
            st.write(stats)
    else:
        st.warning("Please enter a player name.")