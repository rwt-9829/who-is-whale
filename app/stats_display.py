import streamlit as st

def show_player_stats(player_stats):
    st.header("Player Statistics")
    bb_size = 100

    for name, stats in player_stats.items():
        hands = stats["hands"]
        winnings = stats["winnings"]

        # General percentages
        vpip = (stats["vpip"] / hands * 100) if hands else 0
        pfr = (stats["pfr"] / hands * 100) if hands else 0
        bb_per_100 = (winnings / (hands * bb_size) * 100) if hands else 0

        # Flop stats
        cbet_flop = (stats["cbet_flop"] / stats["saw_flop_pfr"] * 100) if stats["saw_flop_pfr"] else 0
        fold_to_cbet_flop = (stats["fold_to_cbet_flop"] / stats["faced_cbet_flop"] * 100) if stats["faced_cbet_flop"] else 0
        x_r_flop = (stats["x_r_flop"] / stats["saw_flop_pfc"] * 100) if stats["saw_flop_pfc"] else 0
        donk_flop = (stats["donk_flop"] / stats["saw_flop_pfc"] * 100) if stats["saw_flop_pfc"] else 0

        # Turn stats
        cbet_turn = (stats["cbet_turn"] / stats["saw_turn_pfr"] * 100) if stats["saw_turn_pfr"] else 0
        fold_to_cbet_turn = (stats["fold_to_cbet_turn"] / stats["faced_cbet_turn"] * 100) if stats["faced_cbet_turn"] else 0
        donk_turn = (stats["donk_turn"] / stats["saw_turn_pfc"] * 100) if stats["saw_turn_pfc"] else 0
        probe_turn = (stats["probe_turn"] / stats["saw_turn_pfc"] * 100) if stats["saw_turn_pfc"] else 0
        r_turn = (stats["r_turn"] / stats["saw_turn_pfc"] * 100) if stats["saw_turn_pfc"] else 0

        # Output
        st.subheader(f"Player: {name}")
        st.write(f"Hands Played: {hands}")
        st.write(f"Winnings: {winnings}")
        st.write(f"BB/100: {bb_per_100:.2f}")
        st.write(f"VPIP: {vpip:.2f}%")
        st.write(f"PFR: {pfr:.2f}%")

        st.markdown("### Flop Stats")
        st.write(f"C-bet Flop: {cbet_flop:.2f}%")
        st.write(f"Fold to Flop C-bet: {fold_to_cbet_flop:.2f}%")
        st.write(f"Check-Raise Flop: {x_r_flop:.2f}%")
        st.write(f"Donk Bet Flop: {donk_flop:.2f}%")

        st.markdown("### Turn Stats")
        st.write(f"C-bet Turn: {cbet_turn:.2f}%")
        st.write(f"Fold to Turn C-bet: {fold_to_cbet_turn:.2f}%")
        st.write(f"Donk Bet Turn: {donk_turn:.2f}%")
        st.write(f"Probe Bet Turn: {probe_turn:.2f}%")
        st.write(f"Raise Turn: {r_turn:.2f}%")
