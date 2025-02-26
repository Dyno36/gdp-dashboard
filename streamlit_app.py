import streamlit as st
import numpy as np
import optuna

# Function to project player props
def project_player_props(season_avg, recent_avg, opp_defense, line, usage_rate, weights):
    w_season, w_recent, w_defense, w_usage = weights
    projected_points = (
        (season_avg * w_season) + 
        (recent_avg * w_recent) + 
        (opp_defense * w_defense) + 
        (usage_rate * w_usage)
    )
    edge = ((projected_points - line) / line) * 100
    return projected_points, edge

# Function to calculate MAPE
def calculate_mape(actual, predicted):
    return np.mean(np.abs((actual - predicted) / actual)) * 100

# Optimization function for Optuna
def objective(trial):
    # Suggest weights for each factor
    w_season = trial.suggest_float("w_season", 0, 1)
    w_recent = trial.suggest_float("w_recent", 0, 1)
    w_defense = trial.suggest_float("w_defense", 0, 1)
    w_usage = trial.suggest_float("w_usage", 0, 1)

    # Normalize weights so they sum to 1
    total_weight = w_season + w_recent + w_defense + w_usage
    weights = [w / total_weight for w in [w_season, w_recent, w_defense, w_usage]]

    # Example test data (you’d replace this with real game results)
    season_avg, recent_avg, opp_defense, usage_rate, actual_points = 25, 20, 22, 28, 26
    line = 24.5

    # Get projected points
    projected_points, _ = project_player_props(season_avg, recent_avg, opp_defense, line, usage_rate, weights)
    
    # Calculate MAPE
    mape = calculate_mape(actual_points, projected_points)
    return mape

# Streamlit app setup
st.title("NBA Player Prop Finder (with Optimization)")

st.header("Enter Player Stats & Betting Line")

season_avg = st.number_input("Season Average", min_value=0.0, step=0.1)
recent_avg = st.number_input("Recent 5-Game Average", min_value=0.0, step=0.1)
opp_defense = st.number_input("Opponent Defense (Points Allowed to Position)", min_value=0.0, step=0.1)
usage_rate = st.number_input("Player Usage Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
line = st.number_input("Sportsbook Line", min_value=0.0, step=0.1)
actual_points = st.number_input("Actual Points Scored (Optional for Accuracy Check)", min_value=0.0, step=0.1)

if st.button("Optimize & Find Best Prop Bet"):
    if season_avg and recent_avg and opp_defense and line and usage_rate and actual_points:
        # Run Optuna optimization
        study = optuna.create_study(direction="minimize")
        study.optimize(objective, n_trials=100)

        # Get the best weights
        best_weights = study.best_params
        total_weight = sum(best_weights.values())
        weights = [w / total_weight for w in best_weights.values()]

        # Use optimized weights for projection
        projected_points, edge = project_player_props(season_avg, recent_avg, opp_defense, line, usage_rate, weights)

        # Show results
        st.write(f"### Optimized Projected Points: {projected_points:.2f}")
        st.write(f"### Edge vs Line: {edge:.2f}%")
        st.write(f"### Best Weights: {best_weights}")

        # Calculate MAPE with optimized weights
        model_mape = calculate_mape(actual_points, projected_points)
        st.write(f"### Optimized MAPE (Model Accuracy vs Actual): {model_mape:.2f}%")

        if edge > 10:
            st.success("✅ Strong Over Bet Opportunity")
        elif edge < -10:
            st.error("❌ Strong Under Bet Opportunity")
        else:
            st.warning("⚠️ Line is Efficient — No Clear Bet")
    else:
        st.warning("Please fill in all stats to calculate the projection.")