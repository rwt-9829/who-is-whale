import streamlit as st

def show_player_stats(player_stats):
    st.header("Player Statistics")

    if not player_stats:
        st.write("No player stats available.")
        return

    # Dropdown to select player
    selected_player = st.selectbox("Select a player", list(player_stats.keys()))
    stats = player_stats[selected_player]
    hands = stats["hands"]
    winnings = stats["winnings"]
    bb_size = 100

    # Basic
    vpip = round((stats["vpip"] / hands * 100), 2) if hands else 0
    pfr = round((stats["pfr"] / hands * 100), 2) if hands else 0
    bb_per_100 = round((winnings / (hands * bb_size) * 100), 2) if hands else 0

    # Flop
    cbet_flop = round((stats["cbet_flop"] / stats["saw_flop_pfr"] * 100), 2) if stats["saw_flop_pfr"] else 0
    fold_to_cbet = round((stats["fold_to_cbet_flop"] / stats["faced_cbet_flop"] * 100), 2) if stats["faced_cbet_flop"] else 0
    x_r_flop = round((stats["x_r_flop"] / stats["saw_flop_pfc"] * 100), 2) if stats["saw_flop_pfc"] else 0
    donk_flop = round((stats["donk_flop"] / stats["saw_flop_pfc"] * 100), 2) if stats["saw_flop_pfc"] else 0

    # Turn
    turn_cbet = round((stats["turn_cbet"] / stats["saw_turn_fa"] * 100), 2) if stats["saw_turn_fa"] else 0
    turn_delay_cbet = round((stats["turn_delay_cbet"] / stats["saw_turn_xx"] * 100), 2) if stats["saw_turn_xx"] else 0
    probe_turn = round((stats["probe_turn"] / stats["saw_turn_xx"] * 100), 2) if stats["saw_turn_xx"] else 0
    donk_turn = round((stats["donk_turn"] / stats["saw_turn_fc"] * 100), 2) if stats["saw_turn_fc"] else 0
    r_turn = round((stats["r_turn"] / stats["faced_turn_bet"] * 100), 2) if stats["faced_turn_bet"] else 0
    fold_to_bet_turn = round((stats["fold_to_bet_turn"] / stats["faced_turn_bet"] * 100), 2) if stats["faced_turn_bet"] else 0

    # River
    river_cbet = round((stats["river_cbet"] / stats["saw_river_fa"] * 100), 2) if stats["saw_river_fa"] else 0
    river_delay_cbet = round((stats["river_delay_cbet"] / stats["saw_river_xx"] * 100), 2) if stats["saw_river_xx"] else 0
    probe_river = round((stats["probe_river"] / stats["saw_river_xx"] * 100), 2) if stats["saw_river_xx"] else 0
    donk_river = round((stats["donk_river"] / stats["saw_river_fc"] * 100), 2) if stats["saw_river_fc"] else 0
    r_river = round((stats["r_river"] / stats["faced_river_bet"] * 100), 2) if stats["faced_river_bet"] else 0
    fold_to_bet_river = round((stats["fold_to_bet_river"] / stats["faced_river_bet"] * 100), 2) if stats["faced_river_bet"] else 0

    st.subheader(selected_player)

    # BASIC TABLE
    st.markdown("**Basic Stats**")
    st.table({
        "Stat": ["Hands", "Winnings", "BB/100", "VPIP %", "PFR %"],
        "Value": [hands, winnings, f"{bb_per_100:.2f}", f"{vpip:.2f}", f"{pfr:.2f}"]
    })

    # FLOP TABLE
    st.markdown("**Flop Stats**")
    st.table({
        "Stat": ["Flop CBet %", "Fold to Flop CBet %", "Flop X/R %", "Flop Donk %"],
        "Value": [f"{cbet_flop:.2f}", f"{fold_to_cbet:.2f}", f"{x_r_flop:.2f}", f"{donk_flop:.2f}"]
    })

    # TURN TABLE
    st.markdown("**Turn Stats**")
    st.table({
        "Stat": [
            "Turn CBet %", "Delayed Turn CBet %", "Turn Probe %", "Turn Donk %",
            "Turn Raise %", "Fold to Turn Bet %"
        ],
        "Value": [
            f"{turn_cbet:.2f}", f"{turn_delay_cbet:.2f}", f"{probe_turn:.2f}",
            f"{donk_turn:.2f}", f"{r_turn:.2f}", f"{fold_to_bet_turn:.2f}"
        ]
    })

    # RIVER TABLE
    st.markdown("**River Stats**")
    st.table({
        "Stat": [
            "River CBet %", "Delayed River CBet %", "River Probe %", "River Donk %",
            "River Raise %", "Fold to River Bet %"
        ],
        "Value": [
            f"{river_cbet:.2f}", f"{river_delay_cbet:.2f}", f"{probe_river:.2f}",
            f"{donk_river:.2f}", f"{r_river:.2f}", f"{fold_to_bet_river:.2f}"
        ]
    })
