import streamlit as st

def show_player_stats(player_stats):
    st.header("Player Statistics")
    bb_size = 100

    for name, stats in player_stats.items():
        hands = stats["hands"]
        winnings = stats["winnings"]
        vpip = (stats["vpip"] / hands * 100) if hands else 0
        pfr = (stats["pfr"] / hands * 100) if hands else 0
        bb_per_100 = (winnings / (hands * bb_size) * 100) if hands else 0

        # FLOP percentages
        cbet_flop = (stats["cbet_flop"] / stats["saw_flop_pfr"] * 100) if stats["saw_flop_pfr"] else 0
        fold_to_cbet_flop = (stats["fold_to_cbet_flop"] / stats["faced_cbet_flop"] * 100) if stats["faced_cbet_flop"] else 0
        x_r_flop = (stats["x_r_flop"] / stats["saw_flop_pfc"] * 100) if stats["saw_flop_pfc"] else 0
        donk_flop = (stats["donk_flop"] / stats["saw_flop_pfc"] * 100) if stats["saw_flop_pfc"] else 0

        # TURN percentages
        cbet_turn = (stats["turn_cbet"] / stats["saw_turn_pfr"] * 100) if stats["saw_turn_pfr"] else 0
        fold_to_cbet_turn = (stats["fold_to_cbet_turn"] / stats["faced_turn_cbet"] * 100) if stats["faced_turn_cbet"] else 0
        x_r_turn = (stats["x_r_turn"] / stats["saw_turn_pfc"] * 100) if stats["saw_turn_pfc"] else 0
        donk_turn = (stats["donk_turn"] / stats["saw_turn_pfc"] * 100) if stats["saw_turn_pfc"] else 0
        probe_turn = (stats["probe_turn"] / stats["saw_turn_pfc"] * 100) if stats["saw_turn_pfc"] else 0

        st.subheader(name)
        st.markdown("**BASIC STATS**")
        st.write(f"Hands: {hands}")
        st.write(f"Winnings: {winnings}")
        st.write(f"BB/100: {bb_per_100:.2f}")
        st.write(f"VPIP: {vpip:.2f}%")
        st.write(f"PFR: {pfr:.2f}%")

        st.markdown("**FLOP STATS**")
        st.write(f"Flop CBet%: {cbet_flop:.2f}%")
        st.write(f"Flop Fold to CBet%: {fold_to_cbet_flop:.2f}%")
        st.write(f"Flop X/R%: {x_r_flop:.2f}%")
        st.write(f"Flop Donk%: {donk_flop:.2f}%")

        st.markdown("**TURN STATS**")
        st.write(f"Turn CBet%: {cbet_turn:.2f}%")
        st.write(f"Turn Fold to CBet%: {fold_to_cbet_turn:.2f}%")
        st.write(f"Turn X/R%: {x_r_turn:.2f}%")
        st.write(f"Turn Donk%: {donk_turn:.2f}%")
        st.write(f"Turn Probe%: {probe_turn:.2f}%")
