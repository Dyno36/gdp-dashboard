import streamlit as st
import numpy as np

# Function to project player props
def project_player_props(season_avg, recent_avg, opp_defense, line):
    projected_points = (season_avg * 0.4) + (recent_avg * 0.3) + (opp_defense * 0.3)
    edge = ((projected_points - line) / line) * 100
    
    return projected_points, edge

# Streamlit app setup
st.title("NBA Player Prop Finder")

st.header("Enter Player Stats & Betting Line")

season_avg = st.number_input("Season Average", min_value=0.0, step=0.1)
recent_avg = st.number_input("Recent 5-Game Average", min_value=0.0, step=0.1)
opp_defense = st.number_input("Opponent Defense (Points Allowed to Position)", min_value=0.0, step=0.1)
line = st.number_input("Sportsbook Line", min_value=0.0, step=0.1)

if st.button("Find Best Prop Bet"):
    if season_avg and recent_avg and opp_defense and line:
        projected_points, edge = project_player_props(season_avg, recent_avg, opp_defense, line)
        st.write(f"### Projected Points: {projected_points:.2f}")
        st.write(f"### Edge vs Line: {edge:.2f}%")
        
        if edge > 10:
            st.success("✅ Strong Over Bet Opportunity")
        elif edge < -10:
            st.error("❌ Strong Under Bet Opportunity")
        else:
            st.warning("⚠️ Line is Efficient — No Clear Bet")
    else:
        st.warning("Please fill in all stats to calculate the projection.")
